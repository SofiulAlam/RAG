from fastapi import APIRouter
from app.api.endpoints import projects, chat, prompts, files, auth, diff, templates, deployment

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(projects.router, prefix="/projects", tags=["projects"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])
router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
router.include_router(files.router, prefix="/files", tags=["files"])
router.include_router(diff.router, prefix="/diff", tags=["diff"])
router.include_router(templates.router, prefix="/templates", tags=["templates"])
router.include_router(deployment.router, prefix="/deployment", tags=["deployment"])
