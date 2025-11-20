from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.chat_message import ChatMessage
from app.models.project import Project
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


@router.get("/{project_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get all chat messages for a project"""
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.project_id == project_id)
        .order_by(ChatMessage.created_at)
    )
    messages = result.scalars().all()

    return messages


@router.post("/{project_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    project_id: UUID,
    message: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
):
    """Send a chat message and get AI response"""
    # Verify project exists
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Save user message
    user_message = ChatMessage(
        project_id=project_id,
        role="user",
        content=message.content,
    )
    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)

    # Get conversation history
    history_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.project_id == project_id)
        .order_by(ChatMessage.created_at)
    )
    history = history_result.scalars().all()

    # Generate AI response
    try:
        ai_response = await ai_service.generate_response(
            prompt=message.content,
            project_prompt=project.project_prompt,
            conversation_history=history,
        )

        # Save AI response
        assistant_message = ChatMessage(
            project_id=project_id,
            role="assistant",
            content=ai_response,
        )
        db.add(assistant_message)
        await db.commit()
        await db.refresh(assistant_message)

        return assistant_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_id}/summarize")
async def summarize_and_reset(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Summarize conversation and clear history"""
    # Get project
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get all messages
    messages_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.project_id == project_id)
        .order_by(ChatMessage.created_at)
    )
    messages = messages_result.scalars().all()

    # Generate summary
    summary = await ai_service.summarize_conversation(messages)

    # Update project prompt with summary
    if project.project_prompt:
        project.project_prompt += f"\n\n## Previous Session Summary\n{summary}"
    else:
        project.project_prompt = f"## Previous Session Summary\n{summary}"

    # Delete old messages
    for message in messages:
        await db.delete(message)

    await db.commit()

    return {"summary": summary, "message": "Conversation summarized and cleared"}
