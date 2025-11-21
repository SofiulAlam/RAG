from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
import httpx
import os

from app.db.session import get_db
from app.models.project import Project
from app.models.project_file import ProjectFile
from app.models.user import User
from app.core.security import get_current_active_user

router = APIRouter()


class DeploymentRequest(BaseModel):
    project_name: str
    environment_variables: dict = {}


class DeploymentStatus(BaseModel):
    status: str
    url: Optional[str] = None
    build_id: Optional[str] = None
    logs: Optional[str] = None


@router.post("/{project_id}/deploy")
async def deploy_to_vercel(
    project_id: UUID,
    request: DeploymentRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> DeploymentStatus:
    """
    Deploy project to Vercel
    Requires VERCEL_TOKEN environment variable
    """
    # Check if Vercel token is configured
    vercel_token = os.getenv("VERCEL_TOKEN")
    if not vercel_token:
        raise HTTPException(
            status_code=503,
            detail="Vercel deployment not configured. Please set VERCEL_TOKEN environment variable."
        )

    # Get project
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id
        )
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get all project files
    files_result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id)
    )
    files = files_result.scalars().all()

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Project has no files to deploy"
        )

    # Prepare files for Vercel deployment
    file_dict = {}
    for file in files:
        file_dict[file.path] = {
            "file": file.content
        }

    # Prepare deployment payload
    deployment_payload = {
        "name": request.project_name,
        "files": file_dict,
        "projectSettings": {
            "framework": project.framework.lower() if project.framework else "nextjs",
        },
    }

    # Add environment variables if provided
    if request.environment_variables:
        deployment_payload["env"] = request.environment_variables

    # Call Vercel API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.vercel.com/v13/deployments",
                json=deployment_payload,
                headers={
                    "Authorization": f"Bearer {vercel_token}",
                    "Content-Type": "application/json",
                },
                timeout=60.0,
            )

            if response.status_code != 200:
                error_detail = response.json().get("error", {}).get("message", "Deployment failed")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Vercel deployment failed: {error_detail}"
                )

            deployment_data = response.json()

            # Update project with deployment URL
            deployment_url = f"https://{deployment_data.get('url', '')}"
            project.deployment_url = deployment_url
            await db.commit()

            return DeploymentStatus(
                status="success",
                url=deployment_url,
                build_id=deployment_data.get("id"),
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Deployment request timed out"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to connect to Vercel API: {str(e)}"
        )


@router.get("/{project_id}/deployment-status")
async def get_deployment_status(
    project_id: UUID,
    build_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> DeploymentStatus:
    """Get deployment status from Vercel"""
    vercel_token = os.getenv("VERCEL_TOKEN")
    if not vercel_token:
        raise HTTPException(
            status_code=503,
            detail="Vercel deployment not configured"
        )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.vercel.com/v13/deployments/{build_id}",
                headers={"Authorization": f"Bearer {vercel_token}"},
                timeout=30.0,
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to get deployment status"
                )

            data = response.json()

            return DeploymentStatus(
                status=data.get("readyState", "UNKNOWN"),
                url=f"https://{data.get('url', '')}",
                build_id=build_id,
            )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to connect to Vercel API: {str(e)}"
        )


@router.post("/{project_id}/export")
async def export_project(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Export project as a zip file"""
    import io
    import zipfile
    from fastapi.responses import StreamingResponse

    # Get project
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id
        )
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get all files
    files_result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id)
    )
    files = files_result.scalars().all()

    # Create zip file in memory
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            zip_file.writestr(file.path, file.content)

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={project.name}.zip"
        }
    )
