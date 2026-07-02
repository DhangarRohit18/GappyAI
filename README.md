# 🚀 OrbitOS — The Autonomous Operating System for Startups

> **"One AI Employee. Infinite Productivity."**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Built with Lemma SDK](https://img.shields.io/badge/Built%20with-Lemma%20SDK-6366f1.svg)](https://lemma.work)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)](https://fastapi.tiangolo.com)
[![Powered by Gemini](https://img.shields.io/badge/AI-Gemini%20%7C%20GPT--4-orange)](https://ai.google.dev)
[![Hackathon: Gappy AI](https://img.shields.io/badge/Hackathon-Gappy%20AI%20%E2%9C%A8-purple)](https://discord.gg/6dVR7zTvy)

---

## 🎯 What is OrbitOS?

OrbitOS is the world's first **Autonomous AI Startup Operating System** — a multi-agent platform that acts as your company's COO, running on the **Lemma SDK** as its orchestration brain.

Instead of founders spending 10+ hours/day on operational work, OrbitOS understands your business goals and **autonomously coordinates an entire team of specialized AI agents** to plan, delegate, execute, and report — all without human micromanagement.

```
Founder: "Launch our AI Resume Builder in two weeks."

OrbitOS: ✅ Plan created → GitHub analyzed → Jira issues created →
         Meetings scheduled → Budget estimated → Dashboard ready.
         Done in 47 seconds.
```

---

## 🏆 Hackathon: Ship to Get Hired — Gappy AI

- **Theme:** Build a real AI Product using the Lemma SDK
- **Product:** OrbitOS — Autonomous Startup Operating System
- **Lemma Usage:** Deep, native integration — NOT an API wrapper

### Why Lemma is Essential (Not Optional)

| Capability | Without Lemma | With Lemma SDK |
|-----------|--------------|----------------|
| Agent Memory | Manual DB calls | `lemma.tables` — structured, persistent |
| Agent Communication | Custom message queues | Native `Pod` messaging + `Workflows` |
| Tool Orchestration | Hand-coded routing | `Connectors` + `Functions` |
| Human-in-the-loop | Complex webhook logic | Built-in `Approvals` |
| Multi-Agent Coordination | Distributed system nightmare | `Pods` + `Surfaces` natively |
| Scheduling | Cron + Redis + Celery | `lemma.schedules` built-in |
| Data Persistence | Custom ORM | `lemma.tables` with schema |

---

## 🤖 AI Agent Fleet

| Agent | Role | Lemma Integration |
|-------|------|------------------|
| 🧠 **CEO Agent** | Goal decomposition, delegation | Lemma Workflow orchestrator |
| 📋 **PM Agent** | Milestones, roadmaps, sprints | Lemma Tables + Jira Connector |
| 💻 **Developer Agent** | GitHub monitoring, PR analysis | GitHub Connector + Lemma Functions |
| ⚙️ **Operations Agent** | Notion, Jira, documentation | Multi-Connector Workflow |
| 📧 **Comms Agent** | Email, Slack, meetings | Gmail + Slack Connectors |
| 👥 **HR Agent** | Onboarding, scheduling, leave | Calendar + Drive Connectors |
| 💰 **Finance Agent** | Budget, invoices, expenses | Lemma Tables + Drive Connector |
| 📊 **Analytics Agent** | Dashboards, reports, KPIs | Lemma Tables + visualization |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OrbitOS Frontend                      │
│            Next.js 14 + TailwindCSS + ShadCN            │
└─────────────────────┬───────────────────────────────────┘
                      │ WebSocket + REST
┌─────────────────────▼───────────────────────────────────┐
│                  FastAPI Backend                          │
│         (Python + Lemma SDK + Redis + Celery)           │
└──────┬──────────────┬──────────────┬────────────────────┘
       │              │              │
┌──────▼──────┐ ┌─────▼──────┐ ┌────▼───────────────────┐
│ Lemma Pod   │ │  Lemma     │ │  Lemma Connectors       │
│ (Workspace) │ │  Agents    │ │  GitHub, Slack, Gmail,  │
│  + Tables   │ │ (8 agents) │ │  Jira, Notion, Calendar │
└─────────────┘ └────────────┘ └────────────────────────┘
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Lemma CLI (`pip install lemma-python`)
- API Keys: Gemini / OpenAI, GitHub, Slack, Gmail, Jira

### 1. Clone & Setup
```bash
git clone https://github.com/your-org/orbitos
cd orbitos

# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env  # Fill in your API keys

# Frontend
cd ../frontend
npm install
cp .env.local.example .env.local
```

### 2. Initialize Lemma Pod
```bash
cd backend
lemma auth login
lemma pod init orbitos-startup-pod
lemma pod use orbitos-startup-pod
```

### 3. Deploy Agents to Lemma
```bash
python deploy_agents.py
```

### 4. Start Services
```bash
# Terminal 1 — Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend && npm run dev

# Terminal 3 — Celery Worker
cd backend && celery -A tasks worker --loglevel=info
```

### 5. Open Dashboard
Navigate to `http://localhost:3000`

---

## 📁 Project Structure

```
orbitos/
├── 📂 frontend/                 # Next.js 14 + TypeScript
│   ├── app/
│   │   ├── (dashboard)/
│   │   │   ├── page.tsx         # Main dashboard
│   │   │   ├── agents/          # Agent status panel
│   │   │   ├── projects/        # Project management
│   │   │   ├── analytics/       # Analytics & reports
│   │   │   ├── calendar/        # Smart calendar
│   │   │   ├── emails/          # Email center
│   │   │   └── settings/        # Integrations
│   │   ├── landing/             # Marketing landing page
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/                  # ShadCN components
│   │   ├── agents/              # Agent cards & status
│   │   ├── dashboard/           # Dashboard widgets
│   │   └── orbit/               # OrbitOS-specific components
│   └── lib/
│       ├── lemma.ts             # Lemma SDK client
│       └── api.ts               # API utilities
│
├── 📂 backend/                  # Python + FastAPI + Lemma
│   ├── main.py                  # FastAPI app entry point
│   ├── agents/
│   │   ├── ceo_agent.py         # CEO Agent (Lemma)
│   │   ├── pm_agent.py          # PM Agent (Lemma)
│   │   ├── dev_agent.py         # Developer Agent (Lemma)
│   │   ├── ops_agent.py         # Operations Agent (Lemma)
│   │   ├── comms_agent.py       # Communications Agent (Lemma)
│   │   ├── hr_agent.py          # HR Agent (Lemma)
│   │   ├── finance_agent.py     # Finance Agent (Lemma)
│   │   └── analytics_agent.py   # Analytics Agent (Lemma)
│   ├── lemma/
│   │   ├── pod_setup.py         # Pod initialization
│   │   ├── workflows.py         # Lemma workflow definitions
│   │   ├── tables.py            # Lemma table schemas
│   │   ├── connectors.py        # External tool connectors
│   │   └── surfaces.py          # Lemma surface definitions
│   ├── api/
│   │   ├── goals.py             # Goal submission API
│   │   ├── agents.py            # Agent status API
│   │   ├── projects.py          # Project management API
│   │   └── analytics.py         # Analytics API
│   ├── core/
│   │   ├── memory.py            # Long/short-term memory
│   │   ├── rag.py               # RAG pipeline
│   │   └── planning.py          # Goal planning logic
│   ├── integrations/
│   │   ├── github_client.py
│   │   ├── slack_client.py
│   │   ├── gmail_client.py
│   │   ├── jira_client.py
│   │   └── notion_client.py
│   ├── tasks.py                 # Celery tasks
│   ├── deploy_agents.py         # Agent deployment script
│   └── requirements.txt
│
├── 📂 lemma/                    # Lemma Pod configuration
│   ├── pod.yaml                 # Pod definition
│   ├── agents/                  # Agent YAML definitions
│   ├── workflows/               # Workflow YAML definitions
│   └── connectors/              # Connector configurations
│
└── 📂 docs/                     # Documentation
    ├── architecture.md
    ├── api-reference.md
    ├── deployment.md
    └── demo-script.md
```

---

## 🔌 Integrations

| Tool | Status | Lemma Integration |
|------|--------|------------------|
| GitHub | ✅ Ready | Lemma GitHub Connector |
| Slack | ✅ Ready | Lemma Slack Connector |
| Gmail | ✅ Ready | Lemma Surface (Inbox) |
| Jira | ✅ Ready | Lemma Function + REST |
| Notion | ✅ Ready | Lemma Function + REST |
| Google Calendar | ✅ Ready | Lemma Connector |
| Linear | 🔄 Planned | Lemma Function |
| Zoom | 🔄 Planned | Lemma Connector |

---

## 💡 Key Innovation

**OrbitOS is not a chatbot.** It is an **autonomous operating system** that:

1. **Understands intent** from natural language goals
2. **Plans autonomously** using the CEO Agent + Lemma Workflow
3. **Delegates intelligently** to specialized agents via Lemma Pod messaging
4. **Executes in parallel** using Lemma's async agent runtime
5. **Persists state** in Lemma Tables across sessions
6. **Learns over time** using long-term memory in vector DB
7. **Requires human approval** for high-stakes actions via Lemma Approvals
8. **Reports results** automatically via Lemma Surfaces

---

## 📊 Demo Scenario

**Input:** `"Launch our AI Resume Builder in two weeks"`

**OrbitOS Response (47 seconds):**
```
🧠 CEO Agent: Goal analyzed → 12 objectives identified
📋 PM Agent: 3 sprints created → 47 tasks assigned
💻 Dev Agent: GitHub scanned → 3 blockers found
⚙️ Ops Agent: 47 Jira tickets created → Notion docs updated
📧 Comms Agent: 4 meetings scheduled → Team notified via Slack
👥 HR Agent: Team availability confirmed → 2 contractors needed
💰 Finance Agent: $18,400 budget estimated → Invoice template ready
📊 Analytics Agent: Live dashboard created → Investor update drafted
```

---

## 📄 License

MIT License — Built for the Gappy AI Hackathon 2026

---

## 🙏 Acknowledgments

- [Lemma SDK](https://lemma.work) — The backbone of our multi-agent orchestration
- [Google Gemini](https://ai.google.dev) — Primary AI model
- [Vercel](https://vercel.com) — Frontend deployment
- [FastAPI](https://fastapi.tiangolo.com) — Backend framework
