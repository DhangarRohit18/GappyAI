"""
OrbitOS CEO Agent — The Brain of OrbitOS
Powered by Lemma SDK for orchestration, memory, and agent coordination.

The CEO Agent:
1. Parses natural language goals from founders
2. Breaks goals into structured execution plans
3. Creates task graphs in Lemma Tables
4. Delegates to specialized agents via Lemma Workflows
5. Monitors progress and adapts plans
6. Generates executive summaries
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from loguru import logger

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

from core.config import settings
from core.websocket_manager import websocket_manager
from lemma.pod_setup import get_pod, get_lemma_client

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class CEOAgent:
    """
    The CEO Agent — OrbitOS's strategic brain.
    
    Uses Lemma SDK for:
    - Storing goals and plans in Lemma Tables
    - Triggering downstream agent workflows via Lemma
    - Persistent memory of past goals and outcomes
    - Real-time status streaming via Lemma Surfaces
    """
    
    AGENT_NAME = "CEO Agent"
    AGENT_EMOJI = "🧠"
    
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=self._get_system_prompt(),
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=4096,
            )
        )
        self.pod = get_pod()
        self.lemma = get_lemma_client()
    
    def _get_system_prompt(self) -> str:
        return """You are the CEO Agent of OrbitOS — an Autonomous AI Startup Operating System.

Your role is to act as a world-class COO/CEO who:
1. Deeply understands startup operations and business strategy
2. Breaks complex goals into actionable, time-bound work packages
3. Delegates intelligently to specialized agents
4. Manages risk and anticipates blockers
5. Communicates clearly with founders and stakeholders

When given a goal, you must produce a structured JSON execution plan with:
- Executive summary (2-3 sentences)
- Key objectives (3-7 measurable outcomes)
- Work packages per agent (specific tasks for each of 7 agents)
- Timeline with milestones (week-by-week)
- Risk assessment (top 3 risks + mitigations)
- Budget estimate (rough order of magnitude)
- Success metrics (KPIs to track)

Always respond in valid JSON format."""
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def process_goal(
        self, 
        goal_id: str,
        goal_text: str,
        deadline: Optional[datetime] = None,
        context: Optional[Dict[str, Any]] = None,
        client_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Main goal processing pipeline.
        
        1. Analyze goal using Gemini
        2. Store plan in Lemma Table
        3. Trigger delegation workflows via Lemma
        4. Stream progress to frontend via WebSocket
        """
        
        logger.info(f"{self.AGENT_EMOJI} CEO Agent processing goal: {goal_text[:60]}...")
        
        # Notify frontend — CEO Agent starting
        await self._stream_update(client_id, "started", "Analyzing your goal...")
        
        # Step 1: Generate execution plan with Gemini
        plan = await self._generate_execution_plan(goal_text, deadline, context)
        
        await self._stream_update(client_id, "planning", "Execution plan created")
        
        # Step 2: Store goal + plan in Lemma Table
        await self._persist_to_lemma(goal_id, goal_text, plan)
        
        await self._stream_update(client_id, "delegating", "Delegating to specialized agents...")
        
        # Step 3: Create agent-specific task packages
        agent_packages = await self._create_agent_packages(goal_id, plan)
        
        # Step 4: Trigger all downstream agents via Lemma Workflow
        agent_results = await self._trigger_agent_workflow(
            goal_id, goal_text, plan, agent_packages, client_id
        )
        
        await self._stream_update(client_id, "aggregating", "Aggregating results...")
        
        # Step 5: Compile final executive report
        executive_report = await self._compile_executive_report(
            goal_text, plan, agent_results
        )
        
        await self._stream_update(client_id, "completed", "Mission complete!")
        
        logger.success(f"✅ CEO Agent completed goal: {goal_id}")
        
        return {
            "goal_id": goal_id,
            "status": "completed",
            "plan": plan,
            "agent_results": agent_results,
            "executive_report": executive_report,
            "completed_at": datetime.utcnow().isoformat(),
        }
    
    async def _generate_execution_plan(
        self,
        goal_text: str,
        deadline: Optional[datetime],
        context: Optional[Dict],
    ) -> Dict[str, Any]:
        """Use Gemini to generate a structured execution plan."""
        
        deadline_str = deadline.strftime("%Y-%m-%d") if deadline else "2 weeks from today"
        context_str = json.dumps(context or {}, indent=2)
        
        prompt = f"""Analyze this startup goal and create a complete execution plan:

GOAL: {goal_text}
DEADLINE: {deadline_str}
CONTEXT: {context_str}

Generate a JSON execution plan with this exact structure:
{{
    "executive_summary": "2-3 sentence overview of what will be accomplished",
    "confidence_score": 0.85,
    "estimated_duration_days": 14,
    "objectives": [
        {{"id": "obj-1", "title": "Objective title", "description": "...", "success_metric": "...", "priority": "critical"}}
    ],
    "timeline": [
        {{"week": 1, "focus": "Foundation", "milestones": ["Milestone 1", "Milestone 2"]}},
        {{"week": 2, "focus": "Delivery", "milestones": ["Milestone 3", "Launch"]}}
    ],
    "agent_assignments": {{
        "pm_agent": {{"tasks": ["Create sprint board", "Set up Jira project"], "priority": "immediate"}},
        "developer_agent": {{"tasks": ["Analyze codebase", "Review open PRs"], "priority": "immediate"}},
        "operations_agent": {{"tasks": ["Create Jira tickets", "Update Notion wiki"], "priority": "high"}},
        "communications_agent": {{"tasks": ["Schedule kickoff meeting", "Notify team via Slack"], "priority": "high"}},
        "hr_agent": {{"tasks": ["Check team availability", "Identify skill gaps"], "priority": "medium"}},
        "finance_agent": {{"tasks": ["Estimate project budget", "Identify vendor costs"], "priority": "medium"}},
        "analytics_agent": {{"tasks": ["Set up tracking dashboard", "Define KPIs"], "priority": "medium"}}
    }},
    "risks": [
        {{"risk": "Technical debt blocking velocity", "probability": "medium", "mitigation": "Dedicate 20% of sprint to refactoring"}},
        {{"risk": "Team capacity constraints", "probability": "low", "mitigation": "Pre-identify contractors for overflow work"}},
        {{"risk": "Scope creep", "probability": "high", "mitigation": "Weekly scope reviews with CEO Agent"}}
    ],
    "budget_estimate": {{
        "total_usd": 15000,
        "breakdown": {{"engineering": 10000, "design": 2000, "tools": 1000, "marketing": 2000}},
        "confidence": "rough_order_of_magnitude"
    }},
    "success_metrics": [
        {{"kpi": "Sprint velocity", "target": "80% of tasks completed on time", "tracking": "Jira"}},
        {{"kpi": "Code quality", "target": "Zero P0 bugs at launch", "tracking": "GitHub"}},
        {{"kpi": "Team satisfaction", "target": "No blockers > 24h unresolved", "tracking": "Slack standup"}}
    ]
}}

Return ONLY valid JSON, no markdown, no explanation."""
        
        response = await asyncio.to_thread(self.model.generate_content, prompt)
        
        try:
            # Clean and parse JSON
            raw = response.text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            plan = json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("Failed to parse Gemini JSON, using structured fallback")
            plan = self._generate_fallback_plan(goal_text, deadline)
        
        return plan
    
    def _generate_fallback_plan(self, goal_text: str, deadline: Optional[datetime]) -> Dict:
        """Fallback plan if LLM output can't be parsed."""
        return {
            "executive_summary": f"Executing goal: {goal_text[:100]}. Full team mobilized across all departments.",
            "confidence_score": 0.75,
            "estimated_duration_days": 14,
            "objectives": [
                {"id": "obj-1", "title": "Planning & Setup", "priority": "critical"},
                {"id": "obj-2", "title": "Development & Execution", "priority": "high"},
                {"id": "obj-3", "title": "Testing & Launch", "priority": "high"},
            ],
            "timeline": [
                {"week": 1, "focus": "Planning", "milestones": ["Kickoff", "Sprint 1 Start"]},
                {"week": 2, "focus": "Execution", "milestones": ["Mid-point Review", "Launch"]},
            ],
            "agent_assignments": {
                "pm_agent": {"tasks": ["Create project plan", "Set up Jira"], "priority": "immediate"},
                "developer_agent": {"tasks": ["Code review", "GitHub scan"], "priority": "immediate"},
                "operations_agent": {"tasks": ["Create tickets", "Update docs"], "priority": "high"},
                "communications_agent": {"tasks": ["Schedule meetings", "Notify team"], "priority": "high"},
                "hr_agent": {"tasks": ["Check availability"], "priority": "medium"},
                "finance_agent": {"tasks": ["Estimate costs"], "priority": "medium"},
                "analytics_agent": {"tasks": ["Set up dashboard"], "priority": "medium"},
            },
            "risks": [{"risk": "Timeline pressure", "probability": "medium", "mitigation": "Daily standups"}],
            "budget_estimate": {"total_usd": 15000, "breakdown": {}, "confidence": "estimate"},
            "success_metrics": [{"kpi": "On-time delivery", "target": "100%", "tracking": "Jira"}],
        }
    
    async def _persist_to_lemma(
        self, goal_id: str, goal_text: str, plan: Dict
    ) -> None:
        """
        Save goal and plan to Lemma Table for persistent memory.
        This is how OrbitOS remembers goals across sessions.
        """
        if not self.pod:
            logger.debug("No Lemma Pod — skipping persistence (demo mode)")
            return
        
        try:
            goals_table = await self.pod.tables.get("goals")
            await goals_table.insert({
                "id": goal_id,
                "goal_text": goal_text,
                "status": "active",
                "created_at": datetime.utcnow().isoformat(),
                "ceo_plan": json.dumps(plan),
                "progress_pct": 0,
                "assigned_agents": json.dumps(list(plan.get("agent_assignments", {}).keys())),
            })
            logger.info(f"  💾 Goal persisted to Lemma Table: {goal_id}")
        except Exception as e:
            logger.warning(f"  ⚠️  Lemma persistence failed: {e}")
    
    async def _create_agent_packages(
        self, goal_id: str, plan: Dict
    ) -> Dict[str, List[str]]:
        """Extract and structure tasks per agent from the plan."""
        assignments = plan.get("agent_assignments", {})
        packages = {}
        for agent_name, assignment in assignments.items():
            packages[agent_name] = assignment.get("tasks", [])
        return packages
    
    async def _trigger_agent_workflow(
        self,
        goal_id: str,
        goal_text: str,
        plan: Dict,
        agent_packages: Dict[str, List[str]],
        client_id: Optional[str],
    ) -> Dict[str, Any]:
        """
        Trigger all specialized agents via Lemma Workflow.
        
        In production: uses lemma.workflows.trigger() to start the
        goal-execution-workflow which orchestrates all 8 agents.
        
        For demo: runs agents concurrently with simulated results.
        """
        
        # Import agent modules
        from agents.pm_agent import PMAgent
        from agents.dev_agent import DeveloperAgent
        from agents.ops_agent import OperationsAgent
        from agents.comms_agent import CommunicationsAgent
        from agents.hr_agent import HRAgent
        from agents.finance_agent import FinanceAgent
        from agents.analytics_agent import AnalyticsAgent
        
        agents = {
            "pm_agent": PMAgent(),
            "developer_agent": DeveloperAgent(),
            "operations_agent": OperationsAgent(),
            "communications_agent": CommunicationsAgent(),
            "hr_agent": HRAgent(),
            "finance_agent": FinanceAgent(),
            "analytics_agent": AnalyticsAgent(),
        }
        
        # If Lemma Pod available, trigger via workflow
        if self.pod:
            try:
                await self.pod.workflows.trigger(
                    "goal-execution-workflow",
                    payload={
                        "goal_id": goal_id,
                        "goal_text": goal_text,
                        "plan": plan,
                        "agent_packages": agent_packages,
                    }
                )
            except Exception as e:
                logger.warning(f"Lemma workflow trigger failed: {e} — running locally")
        
        # Run all agents concurrently (parallel execution)
        tasks = []
        for agent_key, agent in agents.items():
            agent_tasks = agent_packages.get(agent_key, [])
            tasks.append(
                agent.execute(
                    goal_id=goal_id,
                    goal_text=goal_text,
                    tasks=agent_tasks,
                    plan=plan,
                    client_id=client_id,
                )
            )
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        agent_results = {}
        for i, (agent_key, agent) in enumerate(agents.items()):
            result = results[i]
            if isinstance(result, Exception):
                agent_results[agent_key] = {
                    "status": "error",
                    "error": str(result),
                    "agent": agent.AGENT_NAME,
                }
            else:
                agent_results[agent_key] = result
        
        return agent_results
    
    async def _compile_executive_report(
        self, goal_text: str, plan: Dict, agent_results: Dict
    ) -> str:
        """Generate a final executive summary for the founder."""
        
        successes = [k for k, v in agent_results.items() if v.get("status") != "error"]
        failures = [k for k, v in agent_results.items() if v.get("status") == "error"]
        
        report = f"""
# OrbitOS Execution Report

**Goal:** {goal_text}

## Executive Summary
{plan.get('executive_summary', 'Goal execution complete.')}

## Agent Execution Summary
- ✅ Successful: {len(successes)}/7 agents
- ❌ Failed: {len(failures)}/7 agents

## Key Actions Completed
"""
        for agent_key, result in agent_results.items():
            if result.get("status") != "error":
                summary = result.get("summary", "Tasks completed successfully")
                agent_name = result.get("agent", agent_key)
                report += f"- **{agent_name}:** {summary}\n"
        
        report += f"""
## Next Steps
1. Review the auto-generated Jira sprint board
2. Approve the scheduled meetings in Calendar
3. Review the budget estimate in Finance
4. Monitor GitHub activity via Developer Agent
5. Check your weekly report every Friday at 5 PM

*Generated by OrbitOS CEO Agent at {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC*
"""
        return report
    
    async def _stream_update(
        self, client_id: Optional[str], status: str, message: str
    ) -> None:
        """Stream real-time status updates to the frontend dashboard."""
        if client_id:
            await websocket_manager.send_agent_update(
                client_id=client_id,
                agent_name=self.AGENT_NAME,
                status=status,
                message=message,
            )
