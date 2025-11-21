from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, List, Optional
from pydantic import BaseModel
from uuid import UUID

from app.db.session import get_db
from app.models.project_file import ProjectFile
from app.models.user import User
from app.core.security import get_current_active_user
from app.services.diff_service import DiffService, ChangeSet

router = APIRouter()
diff_service = DiffService()


class GenerateDiffRequest(BaseModel):
    changes: Dict[str, Dict[str, str]]  # {path: {old: str, new: str}}


class ApplyDiffRequest(BaseModel):
    changes: Dict[str, Dict[str, str]]
    selected_files: Optional[List[str]] = None


@router.post("/{project_id}/generate")
async def generate_diff(
    project_id: UUID,
    request: GenerateDiffRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ChangeSet:
    """Generate a diff for proposed changes"""
    # Validate project ownership is handled by file operations
    changeset = diff_service.generate_changeset(request.changes)

    # Get locked files for this project
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.is_locked == True
        )
    )
    locked_files = [f.path for f in result.scalars().all()]

    # Validate no locked files are being modified
    validation = diff_service.validate_locked_files(changeset, locked_files)

    if not validation["valid"]:
        raise HTTPException(
            status_code=403,
            detail=f"Cannot modify locked files: {', '.join(validation['violations'])}"
        )

    return changeset


@router.post("/{project_id}/apply")
async def apply_diff(
    project_id: UUID,
    request: ApplyDiffRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Apply a diff to project files"""
    # Generate and validate changeset
    changeset = diff_service.generate_changeset(request.changes)

    # Get locked files
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.is_locked == True
        )
    )
    locked_files = [f.path for f in result.scalars().all()]

    # Validate
    validation = diff_service.validate_locked_files(changeset, locked_files)
    if not validation["valid"]:
        raise HTTPException(
            status_code=403,
            detail=f"Cannot modify locked files: {', '.join(validation['violations'])}"
        )

    # Apply changeset
    updated_files = diff_service.apply_changeset(
        changeset,
        selected_files=request.selected_files
    )

    # Update files in database
    for path, content in updated_files.items():
        result = await db.execute(
            select(ProjectFile).where(
                ProjectFile.project_id == project_id,
                ProjectFile.path == path
            )
        )
        file = result.scalar_one_or_none()

        if file:
            file.content = content
        else:
            # Create new file
            new_file = ProjectFile(
                project_id=project_id,
                path=path,
                content=content,
            )
            db.add(new_file)

    await db.commit()

    return {
        "message": "Changes applied successfully",
        "files_updated": len(updated_files),
        "summary": changeset.summary,
    }


@router.post("/{project_id}/preview")
async def preview_diff(
    project_id: UUID,
    file_path: str,
    new_content: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Preview diff for a single file"""
    # Get current file content
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.path == file_path
        )
    )
    file = result.scalar_one_or_none()

    old_content = file.content if file else ""

    # Generate diff
    file_diff = diff_service.generate_file_diff(
        path=file_path,
        old_content=old_content,
        new_content=new_content,
    )

    return file_diff
