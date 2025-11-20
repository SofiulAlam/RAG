from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter()


@router.post("", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new project"""
    # TODO: Get user_id from authentication
    user_id = "00000000-0000-0000-0000-000000000000"

    db_project = Project(
        user_id=user_id,
        **project.model_dump(),
    )
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)

    return db_project


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    db: AsyncSession = Depends(get_db),
):
    """List all projects for the current user"""
    # TODO: Get user_id from authentication
    user_id = "00000000-0000-0000-0000-000000000000"

    result = await db.execute(
        select(Project).where(Project.user_id == user_id)
    )
    projects = result.scalars().all()

    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific project"""
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_update: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a project"""
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await db.commit()
    await db.refresh(project)

    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a project"""
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project)
    await db.commit()

    return {"message": "Project deleted successfully"}


@router.put("/{project_id}/prompt")
async def update_project_prompt(
    project_id: UUID,
    prompt: str,
    db: AsyncSession = Depends(get_db),
):
    """Update project-specific prompt"""
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.project_prompt = prompt
    await db.commit()

    return {"message": "Project prompt updated successfully"}
