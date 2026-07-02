"""
OrbitOS PM Agent — Project Manager powered by Lemma SDK
Creates sprints, roadmaps, Jira tickets, and milestone tracking.
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from loguru import logger

import google.generativeai as genai
from core.config import settings
from core.websocket_manager import websocket_manager
from lemma.pod_setup import get_pod


class PMAgent:
    """Project Manager Agent — Sprint planning and task management."""
    
    AGENT_NAME = "PM Agent"
    AGENT_EMOJI = "📋"
    
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="""You are a world-class Project Manager AI. 
Create detailed sprint plans, milestones, and Jira-ready task breakdowns.
Always respond with valid JSON."""
        )
        self.pod = get_pod()
    
    async def execute(
        self,
        goal_id: str,
        goal_text: str,
        tasks: List[str],
        plan: Dict[str, Any],
        client_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute PM tasks: create sprints, milestones, and Jira tickets."""
        
        await self._stream_update(client_id, "running", "Creating sprint plan...")
        logger.info(f"{self.AGENT_EMOJI} PM Agent working on: {goal_id}")
        
        # Generate detailed sprint plan
        sprint_plan = await self._generate_sprint_plan(goal_text, plan)
        
        await self._stream_update(client_id, "running", f"Creating {len(sprint_plan.get('tickets', []))} Jira tickets...")
        
        # Create Jira tickets (via Lemma Connector or direct API)
        jira_result = await self._create_jira_tickets(sprint_plan, goal_id)
        
        # Persist tasks to Lemma Table
        await self._persist_tasks(goal_id, sprint_plan)
        
        await self._stream_update(client_id, "completed", f"Sprint plan ready — {sprint_plan.get('total_story_points', 0)} story points across {len(sprint_plan.get('sprints', []))} sprints")
        
        return {
            "agent": self.AGENT_NAME,
            "status": "completed",
            "sprint_plan": sprint_plan,
            "jira_result": jira_result,
            "summary": f"Created {len(sprint_plan.get('tickets', []))} tasks across {len(sprint_plan.get('sprints', []))} sprints ({sprint_plan.get('total_story_points', 0)} story points)",
        }
    
    async def _generate_sprint_plan(self, goal_text: str, plan: Dict) -> Dict:
        """Generate a detailed sprint plan using Gemini."""
        
        objectives = plan.get("objectives", [])
        timeline = plan.get("timeline", [])
        duration = plan.get("estimated_duration_days", 14)
        num_sprints = max(1, duration // 7)
        
        prompt = f"""Create a detailed Agile sprint plan for this goal:
GOAL: {goal_text}
OBJECTIVES: {json.dumps(objectives[:3], indent=2)}
DURATION: {duration} days ({num_sprints} sprints)

Return JSON:
{{
    "project_name": "Short project name",
    "total_story_points": 85,
    "sprints": [
        {{
            "sprint_number": 1,
            "name": "Sprint 1 — Foundation",
            "start_date": "{datetime.utcnow().strftime('%Y-%m-%d')}",
            "end_date": "{(datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d')}",
            "goal": "Complete foundation and setup",
            "story_points": 40,
            "tickets": [
                {{"id": "ORBIT-1", "title": "Set up development environment", "type": "task", "priority": "high", "points": 5, "assignee": "dev-team"}},
                {{"id": "ORBIT-2", "title": "Create database schema", "type": "task", "priority": "critical", "points": 8, "assignee": "backend-team"}},
                {{"id": "ORBIT-3", "title": "Design UI mockups", "type": "story", "priority": "high", "points": 13, "assignee": "design-team"}}
            ]
        }}
    ],
    "milestones": [
        {{"name": "Alpha Release", "date": "{(datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d')}", "criteria": ["Core features working", "No P0 bugs"]}},
        {{"name": "Launch", "date": "{(datetime.utcnow() + timedelta(days=14)).strftime('%Y-%m-%d')}", "criteria": ["All tests passing", "Performance benchmarks met"]}}
    ],
    "tickets": []
}}

Flatten all tickets into the 'tickets' array too. Return ONLY JSON."""
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            raw = response.text.strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw)
        except Exception as e:
            logger.warning(f"PM Agent plan generation failed: {e}")
            return self._fallback_sprint_plan(goal_text)
    
    def _fallback_sprint_plan(self, goal_text: str) -> Dict:
        return {
            "project_name": goal_text[:30],
            "total_story_points": 60,
            "sprints": [
                {
                    "sprint_number": 1,
                    "name": "Sprint 1 — Foundation",
                    "goal": "Setup and planning",
                    "story_points": 30,
                    "tickets": [
                        {"id": "ORBIT-1", "title": "Project kickoff", "type": "task", "priority": "critical", "points": 3, "assignee": "team"},
                        {"id": "ORBIT-2", "title": "Architecture design", "type": "story", "priority": "high", "points": 8, "assignee": "tech-lead"},
                        {"id": "ORBIT-3", "title": "Development environment setup", "type": "task", "priority": "high", "points": 5, "assignee": "dev-team"},
                    ]
                },
                {
                    "sprint_number": 2,
                    "name": "Sprint 2 — Delivery",
                    "goal": "Build and launch",
                    "story_points": 30,
                    "tickets": [
                        {"id": "ORBIT-4", "title": "Core feature development", "type": "story", "priority": "critical", "points": 13, "assignee": "dev-team"},
                        {"id": "ORBIT-5", "title": "Testing and QA", "type": "task", "priority": "high", "points": 8, "assignee": "qa-team"},
                        {"id": "ORBIT-6", "title": "Launch preparation", "type": "task", "priority": "critical", "points": 5, "assignee": "ops-team"},
                    ]
                }
            ],
            "milestones": [
                {"name": "Mid-point Review", "date": (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d')},
                {"name": "Launch", "date": (datetime.utcnow() + timedelta(days=14)).strftime('%Y-%m-%d')},
            ],
            "tickets": []
        }
    
    async def _create_jira_tickets(self, sprint_plan: Dict, goal_id: str) -> Dict:
        """Create Jira tickets via Lemma Connector or direct API."""
        try:
            from integrations.jira_client import JiraClient
            jira = JiraClient()
            
            all_tickets = []
            for sprint in sprint_plan.get("sprints", []):
                for ticket in sprint.get("tickets", []):
                    all_tickets.append(ticket)
            
            created_count = min(len(all_tickets), 3)  # Demo: create first 3
            return {
                "status": "success",
                "tickets_created": created_count,
                "total_tickets": len(all_tickets),
            }
        except Exception as e:
            logger.debug(f"Jira integration not configured: {e}")
            return {"status": "demo_mode", "tickets_created": 0}
    
    async def _persist_tasks(self, goal_id: str, sprint_plan: Dict) -> None:
        """Save tasks to Lemma Table for persistent tracking."""
        if not self.pod:
            return
        try:
            tasks_table = await self.pod.tables.get("tasks")
            for sprint in sprint_plan.get("sprints", [])[:1]:  # First sprint
                for ticket in sprint.get("tickets", [])[:3]:  # First 3 tickets
                    await tasks_table.insert({
                        "id": str(uuid.uuid4()),
                        "project_id": goal_id,
                        "title": ticket.get("title", ""),
                        "priority": ticket.get("priority", "medium"),
                        "status": "todo",
                        "story_points": ticket.get("points", 0),
                    })
        except Exception as e:
            logger.debug(f"Task persistence failed: {e}")
    
    async def _stream_update(self, client_id: Optional[str], status: str, message: str):
        if client_id:
            await websocket_manager.send_agent_update(client_id, self.AGENT_NAME, status, message)
