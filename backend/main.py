"""
OrbitOS Backend — FastAPI Entry Point
Autonomous AI Startup Operating System powered by Lemma SDK
"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger
import uvicorn

from api.goals import router as goals_router
from api.agents import router as agents_router
from api.projects import router as projects_router
from api.analytics import router as analytics_router
from api.auth import router as auth_router
from api.integrations import router as integrations_router
from core.websocket_manager import websocket_manager
from lemma.pod_setup import initialize_lemma_pod
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan — startup and shutdown events."""
    logger.info("🚀 OrbitOS starting up...")
    
    # Initialize Lemma Pod on startup
    try:
        await initialize_lemma_pod()
        logger.success("✅ Lemma Pod initialized successfully")
    except Exception as e:
        logger.error(f"⚠️  Lemma Pod initialization failed: {e}")
        logger.info("Running in demo mode without live Lemma Pod")
    
    logger.success("🌟 OrbitOS is ready — Autonomous Operations Active")
    
    yield  # App runs here
    
    # Cleanup on shutdown
    logger.info("🛑 OrbitOS shutting down...")
    await websocket_manager.disconnect_all()
    logger.info("✅ Shutdown complete")


# ── FastAPI Application ──────────────────────────────────────────────────────

app = FastAPI(
    title="OrbitOS API",
    description="The Autonomous AI Operating System for Startups — Powered by Lemma SDK",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# ── Middleware ───────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ── Routers ──────────────────────────────────────────────────────────────────

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(goals_router, prefix="/api/goals", tags=["Goals & Planning"])
app.include_router(agents_router, prefix="/api/agents", tags=["AI Agents"])
app.include_router(projects_router, prefix="/api/projects", tags=["Projects"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(integrations_router, prefix="/api/integrations", tags=["Integrations"])


# ── WebSocket Endpoint ───────────────────────────────────────────────────────

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    Real-time WebSocket connection for agent status updates.
    Streams live agent execution events to the dashboard.
    """
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            # Keep connection alive and relay messages
            data = await websocket.receive_text()
            await websocket_manager.handle_message(client_id, data)
    except WebSocketDisconnect:
        await websocket_manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected")


# ── Health Endpoints ─────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    return {
        "product": "OrbitOS",
        "tagline": "The Autonomous Operating System for Startups",
        "version": "1.0.0",
        "status": "operational",
        "powered_by": "Lemma SDK",
        "agents": [
            "CEO Agent", "PM Agent", "Developer Agent", "Operations Agent",
            "Communications Agent", "HR Agent", "Finance Agent", "Analytics Agent"
        ]
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    """System health check including Lemma Pod status."""
    from lemma.pod_setup import get_pod_status
    
    pod_status = await get_pod_status()
    
    return {
        "status": "healthy",
        "lemma_pod": pod_status,
        "agents": {
            "ceo": "active",
            "pm": "active",
            "developer": "active",
            "operations": "active",
            "communications": "active",
            "hr": "active",
            "finance": "active",
            "analytics": "active",
        },
        "integrations": {
            "github": settings.GITHUB_TOKEN is not None,
            "slack": settings.SLACK_BOT_TOKEN is not None,
            "gmail": settings.GMAIL_CREDENTIALS is not None,
            "jira": settings.JIRA_API_TOKEN is not None,
            "notion": settings.NOTION_TOKEN is not None,
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
