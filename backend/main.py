from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from app.core.config import settings
from app.api.routes import router
from app.db.session import engine
from app.db.base import Base

# Create FastAPI app
app = FastAPI(
    title="AI App Builder API",
    description="Backend API for AI-powered application builder",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Socket.IO setup
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.ALLOWED_ORIGINS,
)
socket_app = socketio.ASGIApp(sio, app)


@app.on_event("startup")
async def startup():
    """Initialize database and services on startup"""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    await engine.dispose()


@app.get("/")
async def root():
    return {"message": "AI App Builder API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Socket.IO events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


@sio.event
async def join_project(sid, data):
    """Join a project room for real-time updates"""
    project_id = data.get("project_id")
    if project_id:
        await sio.enter_room(sid, f"project_{project_id}")
        await sio.emit("joined", {"project_id": project_id}, room=sid)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:socket_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
