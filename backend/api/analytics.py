from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get_analytics():
    return {
        "kpis": [
            {"name": "Sprint Velocity", "value": 87, "target": 100},
            {"name": "Code Coverage", "value": 72, "target": 90},
            {"name": "Tasks Automated", "value": 847, "change_pct": 23},
            {"name": "Hours Saved", "value": 124, "change_pct": 15},
        ],
        "productivity_trend": [
            {"day": "Mon", "tasks": 12, "automated": 9},
            {"day": "Tue", "tasks": 18, "automated": 15},
            {"day": "Wed", "tasks": 15, "automated": 13},
            {"day": "Thu", "tasks": 22, "automated": 20},
            {"day": "Fri", "tasks": 28, "automated": 25},
        ]
    }
