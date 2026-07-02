from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_integrations():
    return {
        "integrations": [
            {"id": "github", "name": "GitHub", "status": "connected", "icon": "github"},
            {"id": "slack", "name": "Slack", "status": "not_connected", "icon": "slack"},
            {"id": "gmail", "name": "Gmail", "status": "not_connected", "icon": "gmail"},
            {"id": "jira", "name": "Jira", "status": "not_connected", "icon": "jira"},
            {"id": "notion", "name": "Notion", "status": "not_connected", "icon": "notion"},
        ]
    }
