"""
OrbitOS — Lemma Pod Setup & Management
Initializes and manages the Lemma workspace (Pod) for OrbitOS.

The Pod is the central workspace where all 8 OrbitOS agents live,
store data in Tables, run Workflows, and communicate with each other.
"""

import asyncio
from typing import Optional, Dict, Any
from loguru import logger

try:
    from lemma import Lemma
    from lemma.pod import Pod
    from lemma.tables import Table, Column, ColumnType
    from lemma.workflows import Workflow
    from lemma.agents import Agent
    from lemma.connectors import Connector
    LEMMA_AVAILABLE = True
except ImportError:
    LEMMA_AVAILABLE = False
    logger.warning("Lemma SDK not installed. Running in demo mode.")

from core.config import settings

# Global pod instance
_pod: Optional[Any] = None
_lemma_client: Optional[Any] = None


async def initialize_lemma_pod() -> None:
    """
    Initialize the OrbitOS Lemma Pod.
    
    The Pod is the central workspace that:
    - Stores all agent data in structured Tables
    - Coordinates agent communication
    - Manages workflow execution
    - Provides persistent memory across sessions
    """
    global _pod, _lemma_client
    
    if not LEMMA_AVAILABLE:
        logger.warning("Lemma SDK not available — using mock mode")
        return
    
    try:
        # Initialize Lemma client
        _lemma_client = Lemma(api_key=settings.LEMMA_API_KEY)
        
        # Get or create the OrbitOS Pod
        _pod = await _lemma_client.pods.get_or_create(
            name="orbitos-startup-pod",
            description="OrbitOS — Autonomous AI Startup Operating System",
        )
        
        logger.info(f"📦 Pod connected: {_pod.name} (ID: {_pod.id})")
        
        # Initialize all Tables (persistent data storage for agents)
        await _initialize_tables()
        
        # Register all agent definitions
        await _register_agents()
        
        # Set up workflows
        await _register_workflows()
        
        # Configure connectors
        await _setup_connectors()
        
        logger.success("✅ Lemma Pod fully initialized")
        
    except Exception as e:
        logger.error(f"Failed to initialize Lemma Pod: {e}")
        raise


async def _initialize_tables() -> None:
    """
    Create Lemma Tables for persistent agent data storage.
    
    Tables replace traditional databases — agents read/write structured
    data here, enabling memory across sessions and agent-to-agent sharing.
    """
    if not _pod:
        return
    
    tables_config = [
        {
            "name": "goals",
            "description": "Founder goals and high-level objectives",
            "columns": [
                {"name": "id", "type": "text", "primary": True},
                {"name": "goal_text", "type": "text"},
                {"name": "status", "type": "select", "options": ["pending", "planning", "active", "completed"]},
                {"name": "created_at", "type": "datetime"},
                {"name": "deadline", "type": "datetime"},
                {"name": "assigned_agents", "type": "text"},
                {"name": "progress_pct", "type": "number"},
                {"name": "ceo_plan", "type": "text"},  # JSON blob from CEO agent
            ]
        },
        {
            "name": "projects",
            "description": "Projects derived from founder goals",
            "columns": [
                {"name": "id", "type": "text", "primary": True},
                {"name": "goal_id", "type": "text"},
                {"name": "name", "type": "text"},
                {"name": "description", "type": "text"},
                {"name": "status", "type": "select", "options": ["planning", "active", "blocked", "completed"]},
                {"name": "start_date", "type": "datetime"},
                {"name": "end_date", "type": "datetime"},
                {"name": "budget_estimate", "type": "number"},
                {"name": "team_members", "type": "text"},
                {"name": "github_repo", "type": "text"},
                {"name": "jira_project_key", "type": "text"},
                {"name": "notion_page_id", "type": "text"},
            ]
        },
        {
            "name": "tasks",
            "description": "Granular tasks created by PM Agent, synced to Jira",
            "columns": [
                {"name": "id", "type": "text", "primary": True},
                {"name": "project_id", "type": "text"},
                {"name": "title", "type": "text"},
                {"name": "description", "type": "text"},
                {"name": "assignee", "type": "text"},
                {"name": "priority", "type": "select", "options": ["critical", "high", "medium", "low"]},
                {"name": "status", "type": "select", "options": ["todo", "in_progress", "review", "done"]},
                {"name": "due_date", "type": "datetime"},
                {"name": "jira_ticket_id", "type": "text"},
                {"name": "sprint", "type": "text"},
                {"name": "story_points", "type": "number"},
            ]
        },
        {
            "name": "agent_actions",
            "description": "Log of all agent actions for audit trail and analytics",
            "columns": [
                {"name": "id", "type": "text", "primary": True},
                {"name": "agent_name", "type": "text"},
                {"name": "action_type", "type": "text"},
                {"name": "description", "type": "text"},
                {"name": "input_data", "type": "text"},
                {"name": "output_data", "type": "text"},
                {"name": "status", "type": "select", "options": ["running", "success", "failed", "pending_approval"]},
                {"name": "duration_ms", "type": "number"},
                {"name": "created_at", "type": "datetime"},
                {"name": "goal_id", "type": "text"},
            ]
        },
        {
            "name": "github_activity",
            "description": "GitHub commits, PRs, issues monitored by Developer Agent",
            "columns": [
                {"name": "id", "type": "text", "primary": True},
                {"name": "repo", "type": "text"},
                {"name": "type", "type": "select", "options": ["commit", "pr", "issue", "review", "deployment"]},
                {"name": "title", "type": "text"},
                {"name": "author", "type": "text"},
                {"name": "status", "type": "text"},
                {"name": "url", "type": "text"},
                {"name": "is_blocker", "type": "boolean"},
                {"name": "created_at", "type": "datetime"},
            ]
        },
        {
            "name": "emails",
            "description": "Email threads managed by Communications Agent",
            "columns": [
                {"name": "id", "type": "text", "primary": True},
                {"name": "from_address", "type": "text"},
                {"name": "subject", "type": "text"},
                {"name": "body_summary", "type": "text"},
                {"name": "priority", "type": "select", "options": ["urgent", "high", "normal", "low"]},
                {"name": "category", "type": "select", "options": ["investor", "customer", "team", "vendor", "other"]},
                {"name": "action_required", "type": "boolean"},
                {"name": "draft_reply", "type": "text"},
                {"name": "status", "type": "select", "options": ["unread", "draft_ready", "sent", "archived"]},
                {"name": "received_at", "type": "datetime"},
            ]
        },
        {
            "name": "finance_records",
            "description": "Budget, expenses, invoices managed by Finance Agent",
            "columns": [
                {"name": "id", "type": "text", "primary": True},
                {"name": "type", "type": "select", "options": ["budget", "expense", "invoice", "forecast"]},
                {"name": "description", "type": "text"},
                {"name": "amount", "type": "number"},
                {"name": "currency", "type": "text"},
                {"name": "project_id", "type": "text"},
                {"name": "category", "type": "text"},
                {"name": "vendor", "type": "text"},
                {"name": "status", "type": "select", "options": ["pending", "approved", "paid", "overdue"]},
                {"name": "date", "type": "datetime"},
            ]
        },
        {
            "name": "meetings",
            "description": "Meetings scheduled by Communications & HR Agents",
            "columns": [
                {"name": "id", "type": "text", "primary": True},
                {"name": "title", "type": "text"},
                {"name": "description", "type": "text"},
                {"name": "attendees", "type": "text"},
                {"name": "scheduled_at", "type": "datetime"},
                {"name": "duration_minutes", "type": "number"},
                {"name": "type", "type": "select", "options": ["standup", "sprint_planning", "review", "1on1", "investor"]},
                {"name": "zoom_link", "type": "text"},
                {"name": "agenda", "type": "text"},
                {"name": "notes", "type": "text"},
                {"name": "status", "type": "select", "options": ["scheduled", "completed", "cancelled"]},
            ]
        },
    ]
    
    for table_config in tables_config:
        try:
            await _pod.tables.get_or_create(
                name=table_config["name"],
                description=table_config["description"],
            )
            logger.info(f"  📊 Table ready: {table_config['name']}")
        except Exception as e:
            logger.warning(f"  ⚠️  Table {table_config['name']}: {e}")


async def _register_agents() -> None:
    """Register all OrbitOS agents in the Lemma Pod."""
    if not _pod:
        return
    
    agents_config = [
        {
            "name": "ceo-agent",
            "display_name": "CEO Agent",
            "description": "Understands founder goals, breaks them into objectives, and delegates to specialized agents via Lemma workflows.",
            "model": "gemini-1.5-pro",
            "system_prompt": """You are the CEO Agent of OrbitOS. Your role is to:
1. Deeply understand the founder's goals
2. Break goals into specific, measurable objectives  
3. Create execution plans with timelines
4. Delegate work to specialized agents via Lemma workflows
5. Monitor progress and adapt plans
6. Generate executive summaries and investor updates

Always think strategically. Every decision should align with business growth."""
        },
        {
            "name": "pm-agent", 
            "display_name": "Project Manager Agent",
            "description": "Creates milestones, roadmaps, sprint plans, and manages project execution.",
            "model": "gemini-1.5-pro",
            "system_prompt": """You are the Project Manager Agent of OrbitOS. Your role is to:
1. Create detailed project milestones and roadmaps
2. Break work into sprint-sized tasks (2-week sprints)
3. Assign story points and priorities
4. Create Jira tickets via the Jira connector
5. Track velocity and flag delays
6. Generate sprint reports

Use agile methodology. Be specific with deadlines and deliverables."""
        },
        {
            "name": "developer-agent",
            "display_name": "Developer Agent", 
            "description": "Monitors GitHub, analyzes code quality, tracks PRs, and detects technical blockers.",
            "model": "gemini-1.5-flash",
            "system_prompt": """You are the Developer Agent of OrbitOS. Your role is to:
1. Monitor GitHub repositories for commits, PRs, and issues
2. Identify technical blockers and risks
3. Review code quality metrics
4. Track deployment status
5. Escalate critical bugs or security issues
6. Generate technical progress reports

Be precise about technical details. Never ignore security issues."""
        },
        {
            "name": "operations-agent",
            "display_name": "Operations Agent",
            "description": "Manages Jira, Notion, documentation, and operational workflows.",
            "model": "gemini-1.5-flash",
            "system_prompt": """You are the Operations Agent of OrbitOS. Your role is to:
1. Create and update Jira project boards and tickets
2. Maintain Notion documentation and wikis
3. Set up standard operating procedures
4. Manage operational workflows and checklists
5. Keep company knowledge base up to date
6. Generate operational reports

Be organized and systematic. Documentation is critical for scaling."""
        },
        {
            "name": "communications-agent",
            "display_name": "Communications Agent",
            "description": "Manages Gmail, Slack messaging, and meeting scheduling.",
            "model": "gemini-1.5-pro",
            "system_prompt": """You are the Communications Agent of OrbitOS. Your role is to:
1. Read and categorize incoming emails by priority and type
2. Draft professional email replies for founder review
3. Send Slack messages to relevant team channels
4. Schedule meetings on Google Calendar
5. Create meeting agendas and distribute notes
6. Send weekly status updates to stakeholders

Always be professional and clear. Match the tone to the context."""
        },
        {
            "name": "hr-agent",
            "display_name": "HR Agent",
            "description": "Handles employee onboarding, scheduling, and HR operations.",
            "model": "gemini-1.5-flash",
            "system_prompt": """You are the HR Agent of OrbitOS. Your role is to:
1. Manage employee onboarding processes
2. Schedule interviews and coordinate hiring
3. Process leave requests and approvals
4. Verify team availability for project allocation
5. Create onboarding checklists and documents
6. Generate HR reports and headcount analytics

Be empathetic and compliant with HR best practices."""
        },
        {
            "name": "finance-agent",
            "display_name": "Finance Agent",
            "description": "Tracks expenses, creates invoices, monitors budget, and predicts costs.",
            "model": "gemini-1.5-flash",
            "system_prompt": """You are the Finance Agent of OrbitOS. Your role is to:
1. Track all project expenses and create budget estimates
2. Generate professional invoices for clients
3. Monitor budget burn rate and flag overruns
4. Predict future costs based on project scope
5. Create financial reports for investors
6. Identify cost optimization opportunities

Be accurate and conservative with financial projections."""
        },
        {
            "name": "analytics-agent",
            "display_name": "Analytics Agent",
            "description": "Creates dashboards, weekly reports, and predictive analytics.",
            "model": "gemini-1.5-pro",
            "system_prompt": """You are the Analytics Agent of OrbitOS. Your role is to:
1. Aggregate data from all other agents via Lemma Tables
2. Create real-time dashboards and KPI tracking
3. Generate weekly company health reports
4. Identify productivity trends and risks
5. Build investor-ready metrics and reports
6. Predict project success probability

Use data to tell compelling stories. Numbers without context are useless."""
        },
    ]
    
    for agent_cfg in agents_config:
        try:
            await _pod.agents.register(
                name=agent_cfg["name"],
                display_name=agent_cfg["display_name"],
                description=agent_cfg["description"],
                model=agent_cfg.get("model", "gemini-1.5-pro"),
            )
            logger.info(f"  🤖 Agent registered: {agent_cfg['display_name']}")
        except Exception as e:
            logger.warning(f"  ⚠️  Agent {agent_cfg['name']}: {e}")


async def _register_workflows() -> None:
    """
    Register Lemma Workflows — the orchestration backbone of OrbitOS.
    
    Workflows define how agents chain together to accomplish complex tasks.
    This is where Lemma SDK shines — replacing custom orchestration code
    with declarative, observable, retryable workflow definitions.
    """
    if not _pod:
        return
    
    workflows = [
        {
            "name": "goal-execution-workflow",
            "description": "Main orchestration: CEO plans → PM schedules → Dev/Ops execute → Analytics reports",
            "trigger": "goal_submitted",
        },
        {
            "name": "daily-standup-workflow",
            "description": "Every morning: check GitHub, emails, blockers → send Slack digest",
            "trigger": "schedule:0 9 * * 1-5",  # 9 AM weekdays
        },
        {
            "name": "weekly-report-workflow",
            "description": "Every Friday: compile metrics → generate investor update → send summary",
            "trigger": "schedule:0 17 * * 5",  # 5 PM Friday
        },
        {
            "name": "email-triage-workflow",
            "description": "Process incoming emails: classify → draft replies → escalate urgent items",
            "trigger": "gmail_new_message",
        },
        {
            "name": "github-monitor-workflow",
            "description": "Monitor GitHub activity: detect blockers → notify team → update Jira",
            "trigger": "schedule:*/30 * * * *",  # Every 30 minutes
        },
    ]
    
    for workflow in workflows:
        try:
            await _pod.workflows.register(
                name=workflow["name"],
                description=workflow["description"],
            )
            logger.info(f"  ⚡ Workflow registered: {workflow['name']}")
        except Exception as e:
            logger.warning(f"  ⚠️  Workflow {workflow['name']}: {e}")


async def _setup_connectors() -> None:
    """Configure Lemma Connectors for external tool integrations."""
    if not _pod:
        return
    
    logger.info("  🔌 Connectors configured (activate via Settings → Integrations)")


async def get_pod_status() -> Dict[str, Any]:
    """Get current Lemma Pod status."""
    if not _pod:
        return {"connected": False, "mode": "demo"}
    
    try:
        return {
            "connected": True,
            "pod_id": str(_pod.id),
            "pod_name": _pod.name,
            "mode": "live",
        }
    except Exception:
        return {"connected": False, "mode": "error"}


def get_pod() -> Optional[Any]:
    """Get the initialized Lemma Pod instance."""
    return _pod


def get_lemma_client() -> Optional[Any]:
    """Get the Lemma client instance."""
    return _lemma_client
