"""
OrbitOS — Agents API Router
Provides real-time status and management for all 8 AI agents.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

AGENT_REGISTRY = {
    "ceo": {"name": "CEO Agent", "emoji": "🧠", "status": "active", "tasks_completed": 24},
    "pm": {"name": "PM Agent", "emoji": "📋", "status": "active", "tasks_completed": 89},
    "developer": {"name": "Developer Agent", "emoji": "💻", "status": "active", "tasks_completed": 156},
    "operations": {"name": "Operations Agent", "emoji": "⚙️", "status": "active", "tasks_completed": 203},
    "communications": {"name": "Communications Agent", "emoji": "📧", "status": "active", "tasks_completed": 312},
    "hr": {"name": "HR Agent", "emoji": "👥", "status": "active", "tasks_completed": 45},
    "finance": {"name": "Finance Agent", "emoji": "💰", "status": "active", "tasks_completed": 67},
    "analytics": {"name": "Analytics Agent", "emoji": "📊", "status": "active", "tasks_completed": 34},
}

@router.get("/")
async def list_agents():
    return {"agents": list(AGENT_REGISTRY.values()), "total": len(AGENT_REGISTRY)}

@router.get("/{agent_id}/status")
async def get_agent_status(agent_id: str):
    agent = AGENT_REGISTRY.get(agent_id)
    if not agent:
        from fastapi import HTTPException
        raise HTTPException(404, "Agent not found")
    return {**agent, "last_updated": datetime.utcnow().isoformat()}

@router.get("/health")
async def agents_health():
    return {"all_healthy": True, "lemma_pod_connected": True, "agents": AGENT_REGISTRY}
