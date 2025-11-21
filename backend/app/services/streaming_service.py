from typing import AsyncIterator, Optional
from anthropic import AsyncAnthropic
import asyncio

from app.core.config import settings


class StreamingService:
    """Service for streaming AI-generated code in real-time"""

    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def stream_code_generation(
        self,
        prompt: str,
        system_prompt: str,
        project_prompt: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """
        Stream code generation token by token

        Yields tokens as they're generated
        """
        # Combine prompts
        full_system_prompt = system_prompt
        if project_prompt:
            full_system_prompt += f"\n\n{project_prompt}"

        # Stream response from Claude
        async with self.client.messages.stream(
            model=settings.CLAUDE_MODEL,
            max_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE,
            system=full_system_prompt,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def stream_prompt_enhancement(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        """Stream prompt enhancement token by token"""
        enhancement_system = """You are a prompt enhancement assistant. Transform the user's simple prompt
into a detailed, structured prompt suitable for code generation.

Include:
1. Architecture & Framework: Specify tech stack
2. Features: Break down into clear components
3. Design Guidelines: Styling, responsiveness, aesthetics
4. Code Quality: Best practices, patterns, standards

Preserve the user's core intent while adding necessary structure.
Output only the enhanced prompt, no explanations."""

        async with self.client.messages.stream(
            model=settings.CLAUDE_MODEL,
            max_tokens=2000,
            system=enhancement_system,
            messages=[{
                "role": "user",
                "content": f"Enhance this prompt for building a web application:\n\n{prompt}"
            }],
        ) as stream:
            async for text in stream.text_stream:
                yield text


# Socket.IO event handlers
async def handle_stream_code(sio, sid, data, streaming_service: StreamingService):
    """Handle code streaming via Socket.IO"""
    try:
        project_id = data.get("project_id")
        prompt = data.get("prompt")
        system_prompt = data.get("system_prompt", "")
        project_prompt = data.get("project_prompt")

        # Emit start event
        await sio.emit("stream_start", {"project_id": project_id}, room=sid)

        # Stream tokens
        async for token in streaming_service.stream_code_generation(
            prompt=prompt,
            system_prompt=system_prompt,
            project_prompt=project_prompt,
        ):
            await sio.emit("stream_token", {
                "token": token,
                "project_id": project_id,
            }, room=sid)

            # Small delay to prevent overwhelming the client
            await asyncio.sleep(0.01)

        # Emit end event
        await sio.emit("stream_end", {"project_id": project_id}, room=sid)

    except Exception as e:
        await sio.emit("stream_error", {
            "error": str(e),
            "project_id": data.get("project_id")
        }, room=sid)


async def handle_stream_enhance(sio, sid, data, streaming_service: StreamingService):
    """Handle prompt enhancement streaming via Socket.IO"""
    try:
        prompt = data.get("prompt")

        # Emit start event
        await sio.emit("enhance_start", {}, room=sid)

        # Stream tokens
        async for token in streaming_service.stream_prompt_enhancement(prompt):
            await sio.emit("enhance_token", {"token": token}, room=sid)
            await asyncio.sleep(0.01)

        # Emit end event
        await sio.emit("enhance_end", {}, room=sid)

    except Exception as e:
        await sio.emit("enhance_error", {"error": str(e)}, room=sid)
