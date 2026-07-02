"""OrbitOS Goals API — Submit and track founder goals."""

import uuid
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from loguru import logger

router = APIRouter()


class GoalSubmission(BaseModel):
    goal_text: str = Field(..., min_length=5, max_length=2000, description="Natural language goal")
    deadline_days: Optional[int] = Field(14, ge=1, le=365, description="Days to complete")
    priority: Optional[str] = Field("high", description="Goal priority: critical/high/medium/low")
    context: Optional[dict] = Field(None, description="Additional context")
    client_id: Optional[str] = Field(None, description="WebSocket client ID for streaming")


class GoalResponse(BaseModel):
    goal_id: str
    status: str
    message: str
    estimated_completion_minutes: int


# In-memory store for demo (replace with Lemma Table in production)
_active_goals: dict = {}


@router.post("/submit", response_model=GoalResponse)
async def submit_goal(goal: GoalSubmission, background_tasks: BackgroundTasks):
    """
    Submit a natural language goal for autonomous execution by OrbitOS agents.
    
    Example: "Launch our AI Resume Builder in two weeks"
    
    The CEO Agent will immediately:
    1. Parse and understand the goal
    2. Create an execution plan
    3. Delegate to all 7 specialized agents
    4. Begin autonomous execution
    """
    
    goal_id = f"goal-{uuid.uuid4().hex[:8]}"
    deadline = datetime.utcnow() + timedelta(days=goal.deadline_days or 14)
    
    logger.info(f"📥 New goal submitted: {goal_id} — '{goal.goal_text[:60]}...'")
    
    # Store goal
    _active_goals[goal_id] = {
        "id": goal_id,
        "text": goal.goal_text,
        "status": "processing",
        "created_at": datetime.utcnow().isoformat(),
        "deadline": deadline.isoformat(),
        "client_id": goal.client_id,
    }
    
    # Kick off CEO Agent in background
    background_tasks.add_task(
        _run_goal_pipeline,
        goal_id=goal_id,
        goal_text=goal.goal_text,
        deadline=deadline,
        context=goal.context,
        client_id=goal.client_id,
    )
    
    return GoalResponse(
        goal_id=goal_id,
        status="processing",
        message=f"OrbitOS CEO Agent is now analyzing your goal. All 8 agents are being mobilized.",
        estimated_completion_minutes=2,
    )


@router.get("/{goal_id}/status")
async def get_goal_status(goal_id: str):
    """Get the current status of a goal execution."""
    goal = _active_goals.get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.get("/")
async def list_goals():
    """List all active and completed goals."""
    return {
        "goals": list(_active_goals.values()),
        "total": len(_active_goals),
    }


@router.delete("/{goal_id}")
async def cancel_goal(goal_id: str):
    """Cancel an active goal."""
    if goal_id not in _active_goals:
        raise HTTPException(status_code=404, detail="Goal not found")
    _active_goals[goal_id]["status"] = "cancelled"
    return {"message": f"Goal {goal_id} cancelled"}


async def _run_goal_pipeline(
    goal_id: str,
    goal_text: str,
    deadline: datetime,
    context: Optional[dict],
    client_id: Optional[str],
):
    """Background task: run the full OrbitOS goal execution pipeline."""
    try:
        from agents.ceo_agent import CEOAgent
        
        ceo = CEOAgent()
        result = await ceo.process_goal(
            goal_id=goal_id,
            goal_text=goal_text,
            deadline=deadline,
            context=context,
            client_id=client_id,
        )
        
        _active_goals[goal_id].update({
            "status": "completed",
            "result": result,
            "completed_at": datetime.utcnow().isoformat(),
        })
        
        logger.success(f"✅ Goal pipeline complete: {goal_id}")
        
    except Exception as e:
        logger.error(f"❌ Goal pipeline failed: {goal_id} — {e}")
        _active_goals[goal_id].update({
            "status": "error",
            "error": str(e),
        })
