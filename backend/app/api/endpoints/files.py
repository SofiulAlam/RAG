from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.project_file import ProjectFile
from app.schemas.file import ProjectFileCreate, ProjectFileUpdate, ProjectFileResponse

router = APIRouter()


@router.get("/{project_id}", response_model=List[ProjectFileResponse])
async def list_files(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """List all files for a project"""
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id)
    )
    files = result.scalars().all()

    return files


@router.get("/{project_id}/{file_path:path}", response_model=ProjectFileResponse)
async def get_file(
    project_id: UUID,
    file_path: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific file"""
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.path == file_path,
        )
    )
    file = result.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file


@router.post("/{project_id}", response_model=ProjectFileResponse)
async def create_file(
    project_id: UUID,
    file: ProjectFileCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new file"""
    db_file = ProjectFile(
        project_id=project_id,
        **file.model_dump(),
    )
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)

    return db_file


@router.put("/{project_id}/{file_path:path}", response_model=ProjectFileResponse)
async def update_file(
    project_id: UUID,
    file_path: str,
    file_update: ProjectFileUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a file"""
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.path == file_path,
        )
    )
    file = result.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Check if file is locked
    if file.is_locked and "content" in file_update.model_dump(exclude_unset=True):
        raise HTTPException(status_code=403, detail="File is locked")

    update_data = file_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(file, field, value)

    await db.commit()
    await db.refresh(file)

    return file


@router.delete("/{project_id}/{file_path:path}")
async def delete_file(
    project_id: UUID,
    file_path: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete a file"""
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.path == file_path,
        )
    )
    file = result.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    await db.delete(file)
    await db.commit()

    return {"message": "File deleted successfully"}
