from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from app.db.session import get_db
from app.models.template import Template
from app.models.user import User
from app.core.security import get_current_active_user

router = APIRouter()


class TemplateResponse(BaseModel):
    id: UUID
    name: str
    category: Optional[str]
    description: Optional[str]
    template_prompt: str
    framework: Optional[str]
    preview_image: Optional[str]
    usage_count: int

    class Config:
        from_attributes = True


class UseTemplateRequest(BaseModel):
    project_name: str
    variables: dict = {}


@router.get("", response_model=List[TemplateResponse])
async def list_templates(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all available templates"""
    query = select(Template)

    if category:
        query = query.where(Template.category == category)

    query = query.order_by(Template.usage_count.desc(), Template.name)

    result = await db.execute(query)
    templates = result.scalars().all()

    return templates


@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    """List all template categories"""
    result = await db.execute(
        select(Template.category).distinct()
    )
    categories = [cat for (cat,) in result.all() if cat]

    return {"categories": categories}


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific template"""
    result = await db.execute(
        select(Template).where(Template.id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    return template


@router.post("/{template_id}/use")
async def use_template(
    template_id: UUID,
    request: UseTemplateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Use a template to create a new project
    Returns the filled template prompt
    """
    # Get template
    result = await db.execute(
        select(Template).where(Template.id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Fill in template variables
    prompt = template.template_prompt
    for key, value in request.variables.items():
        prompt = prompt.replace(f"{{{key}}}", value)

    # Increment usage count
    await db.execute(
        update(Template)
        .where(Template.id == template_id)
        .values(usage_count=Template.usage_count + 1)
    )
    await db.commit()

    return {
        "prompt": prompt,
        "project_name": request.project_name,
        "framework": template.framework,
    }
