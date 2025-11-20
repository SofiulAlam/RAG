from typing import List, Optional
from anthropic import AsyncAnthropic
import tiktoken

from app.core.config import settings
from app.models.chat_message import ChatMessage


class AIService:
    """Service for AI interactions using Claude"""

    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text"""
        return len(self.encoding.encode(text))

    async def enhance_prompt(self, user_prompt: str) -> str:
        """Enhance user prompt with AI"""
        enhancement_system_prompt = """You are a prompt enhancement assistant. Transform the user's simple prompt
into a detailed, structured prompt suitable for code generation.

Include:
1. Architecture & Framework: Specify tech stack
2. Features: Break down into clear components
3. Design Guidelines: Styling, responsiveness, aesthetics
4. Code Quality: Best practices, patterns, standards

Preserve the user's core intent while adding necessary structure.
Output only the enhanced prompt, no explanations."""

        message = await self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=enhancement_system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Enhance this prompt for building a web application:\n\n{user_prompt}",
                }
            ],
        )

        return message.content[0].text

    async def generate_response(
        self,
        prompt: str,
        project_prompt: Optional[str] = None,
        conversation_history: Optional[List[ChatMessage]] = None,
    ) -> str:
        """Generate AI response for code generation"""
        system_prompt = self._build_system_prompt(project_prompt)

        # Build conversation history
        messages = []
        if conversation_history:
            for msg in conversation_history[:-1]:  # Exclude the last message (current prompt)
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": prompt})

        message = await self.client.messages.create(
            model=self.model,
            max_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE,
            system=system_prompt,
            messages=messages,
        )

        return message.content[0].text

    async def summarize_conversation(self, messages: List[ChatMessage]) -> str:
        """Summarize conversation history"""
        conversation_text = "\n\n".join(
            [f"{msg.role.upper()}: {msg.content}" for msg in messages]
        )

        summary_prompt = f"""Summarize this project conversation, including:
- Current project state
- Features implemented
- Next steps or pending tasks
- Any important decisions or context

Conversation:
{conversation_text}

Provide a concise but comprehensive summary."""

        message = await self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": summary_prompt}],
        )

        return message.content[0].text

    def _build_system_prompt(self, project_prompt: Optional[str] = None) -> str:
        """Build complete system prompt"""
        base_prompt = """You are an expert full-stack developer assistant. Generate production-ready code with:

✅ Code Quality:
- TypeScript strict mode (no 'any' types)
- Proper error boundaries and error handling
- Loading states for all async operations
- Comprehensive JSDoc comments
- Consistent naming conventions

✅ Accessibility:
- Semantic HTML elements
- ARIA labels for interactive elements
- Keyboard navigation support
- Focus management
- Screen reader friendly

✅ Design:
- Responsive layouts (mobile-first, 320px+)
- Modern, beautiful designs (not cookie cutter)
- Smooth animations (200-300ms)
- High-quality Unsplash images where appropriate
- Tailwind CSS with proper spacing

✅ Best Practices:
- Component composition over prop drilling
- Custom hooks for reusable logic
- Proper TypeScript types
- Error handling with try-catch
- Environment variables for config

❌ Avoid:
- Installing unnecessary packages
- Using deprecated APIs
- Hardcoded values (use constants)
- Inline styles (use Tailwind)
- Lorem ipsum (use realistic content)

For all designs, make them beautiful and production-worthy, not cookie cutter.

By default, use:
- Framework: Next.js with TypeScript
- Styling: Tailwind CSS classes
- Components: shadcn/ui library
- Icons: lucide-react
- State: React hooks

Only change files that are relevant to the user's request."""

        if project_prompt:
            return f"{base_prompt}\n\n## Project-Specific Context\n{project_prompt}"

        return base_prompt

    def check_context_usage(
        self,
        messages: List[ChatMessage],
        system_prompt: str,
        project_prompt: Optional[str] = None,
    ) -> dict:
        """Check token usage for conversation"""
        total_tokens = 0

        # System and project prompts
        total_tokens += self.estimate_tokens(system_prompt)
        if project_prompt:
            total_tokens += self.estimate_tokens(project_prompt)

        # Conversation history
        for msg in messages:
            total_tokens += self.estimate_tokens(msg.content)

        # Calculate usage percentage
        usage_percentage = (total_tokens / settings.CONTEXT_LIMIT_TOKENS) * 100

        return {
            "total_tokens": total_tokens,
            "limit": settings.CONTEXT_LIMIT_TOKENS,
            "usage_percentage": usage_percentage,
            "warning": usage_percentage > (settings.CONTEXT_WARNING_THRESHOLD * 100),
        }
