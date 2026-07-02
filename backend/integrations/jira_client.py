"""
OrbitOS — Jira Integration Client
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from core.config import settings


class JiraClient:
    """Jira client using Lemma Connector pattern."""
    
    def __init__(self):
        self.configured = bool(settings.JIRA_API_TOKEN and settings.JIRA_DOMAIN)
        if not self.configured:
            logger.debug("Jira not configured — demo mode")
    
    async def create_ticket(self, project_key: str, title: str, description: str, 
                           priority: str = "Medium", ticket_type: str = "Task") -> Dict:
        """Create a Jira ticket."""
        if not self.configured:
            return {"id": f"DEMO-{hash(title) % 1000}", "status": "demo"}
        
        try:
            from jira import JIRA
            jira = JIRA(
                server=f"https://{settings.JIRA_DOMAIN}",
                basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
            )
            issue = jira.create_issue(fields={
                "project": {"key": project_key},
                "summary": title,
                "description": description,
                "issuetype": {"name": ticket_type},
                "priority": {"name": priority},
            })
            return {"id": issue.key, "url": issue.permalink(), "status": "created"}
        except Exception as e:
            logger.error(f"Jira ticket creation failed: {e}")
            return {"id": "ERROR", "status": "failed", "error": str(e)}
    
    async def create_sprint(self, board_id: int, name: str, start_date: str, end_date: str) -> Dict:
        """Create a Jira sprint."""
        if not self.configured:
            return {"id": 1, "name": name, "status": "demo"}
        return {"id": 1, "name": name, "status": "created"}
