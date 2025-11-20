from fastapi import APIRouter, HTTPException
from app.schemas.chat import EnhancePromptRequest, EnhancePromptResponse
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


@router.post("/enhance", response_model=EnhancePromptResponse)
async def enhance_prompt(request: EnhancePromptRequest):
    """Enhance user prompt with AI"""
    try:
        enhanced = await ai_service.enhance_prompt(request.prompt)

        # Estimate token counts
        original_tokens = ai_service.estimate_tokens(request.prompt)
        enhanced_tokens = ai_service.estimate_tokens(enhanced)

        return EnhancePromptResponse(
            original=request.prompt,
            enhanced=enhanced,
            token_count={
                "original": original_tokens,
                "enhanced": enhanced_tokens,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
