from typing import List, Optional
from pydantic import BaseModel
from anthropic import AsyncAnthropic

from app.core.config import settings


class ErrorAnalysis(BaseModel):
    """Analysis of a code generation error"""
    error_type: str
    description: str
    suggestions: List[str]
    breakdown_prompts: Optional[List[str]] = None


class TroubleshootingService:
    """Service for error detection and troubleshooting guidance"""

    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    def detect_incomplete_response(self, content: str) -> bool:
        """Detect if AI response is incomplete"""
        # Check for unclosed brackets, braces, parentheses
        open_brackets = content.count('{') - content.count('}')
        open_parens = content.count('(') - content.count(')')
        open_squares = content.count('[') - content.count(']')

        if open_brackets > 2 or open_parens > 2 or open_squares > 2:
            return True

        # Check if ends abruptly (common signs)
        abrupt_endings = [
            '...',  # Truncation indicator
            'function',  # Incomplete function declaration
            'const',  # Incomplete variable declaration
            'import',  # Incomplete import
            '=',  # Incomplete assignment
        ]

        last_line = content.strip().split('\n')[-1] if content.strip() else ""

        for ending in abrupt_endings:
            if last_line.strip().endswith(ending):
                return True

        return False

    def detect_error_patterns(self, content: str, error: Optional[str] = None) -> ErrorAnalysis:
        """Detect common error patterns and provide guidance"""
        if self.detect_incomplete_response(content):
            return ErrorAnalysis(
                error_type="incomplete_response",
                description="The AI response appears to be incomplete or truncated",
                suggestions=[
                    "Break your request into smaller, more specific tasks",
                    "Try asking for one component or feature at a time",
                    "Reduce the scope of what you're requesting",
                    "Use more specific file paths to target changes"
                ],
                breakdown_prompts=self._generate_breakdown_prompts(content)
            )

        if error and "context_length" in error.lower():
            return ErrorAnalysis(
                error_type="context_limit",
                description="The conversation has exceeded the context limit",
                suggestions=[
                    "Use the 'Summarize & Reset' feature to condense chat history",
                    "Start a new project for unrelated features",
                    "Review and clear unnecessary chat messages",
                ],
            )

        if error and ("locked" in error.lower() or "403" in error):
            return ErrorAnalysis(
                error_type="locked_files",
                description="Attempted to modify locked files",
                suggestions=[
                    "Unlock the files you want to modify",
                    "Specify exactly which files should be changed",
                    "Check which files are locked in the file tree",
                ],
            )

        # Generic error
        return ErrorAnalysis(
            error_type="unknown",
            description=error or "An error occurred during code generation",
            suggestions=[
                "Try rephrasing your request more specifically",
                "Break complex requests into smaller steps",
                "Check if any files are locked",
                "Ensure your prompt is clear and detailed",
            ],
        )

    def _generate_breakdown_prompts(self, partial_content: str) -> List[str]:
        """Generate suggested smaller prompts based on partial content"""
        # This is a simplified version - could be enhanced with AI
        suggestions = []

        if "component" in partial_content.lower():
            suggestions.append("Create the basic component structure first")
            suggestions.append("Add state management and props")
            suggestions.append("Add styling and final touches")
        elif "api" in partial_content.lower() or "endpoint" in partial_content.lower():
            suggestions.append("Define the API endpoint signature")
            suggestions.append("Implement the core logic")
            suggestions.append("Add error handling and validation")
        else:
            suggestions.extend([
                "Start with the basic file structure",
                "Add the core functionality",
                "Add error handling and edge cases",
                "Add styling and polish"
            ])

        return suggestions[:3]  # Return top 3 suggestions

    async def analyze_error_with_ai(self, error_message: str, context: str) -> ErrorAnalysis:
        """Use AI to analyze complex errors"""
        analysis_prompt = f"""Analyze this error and provide guidance:

Error: {error_message}

Context: {context}

Provide:
1. Error type (brief classification)
2. Clear explanation of what went wrong
3. 3-5 specific actionable suggestions to fix it
4. If the request is too complex, break it into 2-4 smaller prompts

Format as JSON."""

        message = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": analysis_prompt}],
        )

        # Parse AI response (simplified - should handle JSON properly)
        response_text = message.content[0].text

        return ErrorAnalysis(
            error_type="ai_analyzed",
            description=error_message,
            suggestions=[response_text],  # Simplified
        )

    def get_prompt_quality_feedback(self, prompt: str) -> dict:
        """Analyze prompt quality and provide improvement suggestions"""
        feedback = {
            "quality_score": 0,
            "issues": [],
            "suggestions": [],
        }

        # Check length
        if len(prompt) < 20:
            feedback["issues"].append("Prompt is too short")
            feedback["suggestions"].append("Add more details about what you want to build")
        else:
            feedback["quality_score"] += 25

        # Check for specificity
        vague_words = ["something", "some", "stuff", "thing", "it", "maybe"]
        if any(word in prompt.lower() for word in vague_words):
            feedback["issues"].append("Prompt contains vague language")
            feedback["suggestions"].append("Be more specific about components and features")
        else:
            feedback["quality_score"] += 25

        # Check for technical details
        if any(word in prompt.lower() for word in ["component", "function", "api", "database", "style"]):
            feedback["quality_score"] += 25
        else:
            feedback["suggestions"].append("Include technical details like components or features needed")

        # Check for action words
        action_words = ["create", "build", "add", "implement", "update", "fix", "change"]
        if any(word in prompt.lower() for word in action_words):
            feedback["quality_score"] += 25
        else:
            feedback["suggestions"].append("Start with an action word (create, add, update, etc.)")

        # Overall assessment
        if feedback["quality_score"] >= 75:
            feedback["assessment"] = "Good prompt! Should generate quality results."
        elif feedback["quality_score"] >= 50:
            feedback["assessment"] = "Decent prompt, but could be improved."
        else:
            feedback["assessment"] = "Try enhancing your prompt for better results."

        return feedback
