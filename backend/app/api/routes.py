from fastapi import APIRouter
from app.api.endpoints import projects, chat, prompts, files

router = APIRouter()

router.include_router(projects.router, prefix="/projects", tags=["projects"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])
router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
router.include_router(files.router, prefix="/files", tags=["files"])
