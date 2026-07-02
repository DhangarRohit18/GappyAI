"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Brain, Layers, GitBranch, Settings, Mail, Users, DollarSign, BarChart3,
  Bell, Search, Plus, Rocket, Send, CheckCircle, AlertTriangle, Clock,
  TrendingUp, Activity, Zap, Target, Calendar, MessageSquare, Code,
  ChevronRight, LayoutDashboard, FolderKanban, Terminal, Sparkles,
  ArrowUpRight, MoreHorizontal, RefreshCw, Shield, Star
} from "lucide-react";
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from "recharts";

// ── Types & Data ─────────────────────────────────────────────────────────────

interface Agent {
  id: string;
  name: string;
  icon: any;
  role: string;
  status: "active" | "idle" | "running" | "error";
  currentTask?: string;
  tasksCompleted: number;
  color: string;
  gradient: string;
}

const AGENTS: Agent[] = [
  { id: "ceo", name: "CEO Agent", icon: Brain, role: "Goal Decomposition", status: "idle", tasksCompleted: 24, color: "#6366f1", gradient: "from-indigo-500 to-violet-600" },
  { id: "pm", name: "PM Agent", icon: Layers, role: "Sprint Planning", status: "idle", tasksCompleted: 89, color: "#8b5cf6", gradient: "from-violet-500 to-purple-600" },
  { id: "dev", name: "Developer Agent", icon: Code, role: "GitHub Monitor", status: "idle", tasksCompleted: 156, color: "#06b6d4", gradient: "from-cyan-500 to-blue-600" },
  { id: "ops", name: "Operations Agent", icon: Settings, role: "Jira & Notion", status: "idle", tasksCompleted: 203, color: "#10b981", gradient: "from-emerald-500 to-teal-600" },
  { id: "comms", name: "Comms Agent", icon: Mail, role: "Email & Slack", status: "idle", tasksCompleted: 312, color: "#ec4899", gradient: "from-pink-500 to-rose-600" },
  { id: "hr", name: "HR Agent", icon: Users, role: "Team & Hiring", status: "idle", tasksCompleted: 45, color: "#f59e0b", gradient: "from-orange-500 to-amber-600" },
  { id: "finance", name: "Finance Agent", icon: DollarSign, role: "Budget & Invoices", status: "idle", tasksCompleted: 67, color: "#22c55e", gradient: "from-green-500 to-emerald-600" },
  { id: "analytics", name: "Analytics Agent", icon: BarChart3, role: "Reports & KPIs", status: "idle", tasksCompleted: 34, color: "#3b82f6", gradient: "from-blue-500 to-indigo-600" },
];

const productivityData = [
  { day: "Mon", tasks: 12, automated: 9 },
  { day: "Tue", tasks: 18, automated: 15 },
  { day: "Wed", tasks: 15, automated: 13 },
  { day: "Thu", tasks: 22, automated: 20 },
  { day: "Fri", tasks: 28, automated: 25 },
  { day: "Sat", tasks: 8, automated: 8 },
  { day: "Sun", tasks: 5, automated: 5 },
];

const kpiData = [
  { name: "Sprint Velocity", value: 87, target: 100, color: "#6366f1" },
  { name: "Code Coverage", value: 72, target: 90, color: "#06b6d4" },
  { name: "Emails Resolved", value: 94, target: 100, color: "#ec4899" },
  { name: "Budget Health", value: 91, target: 100, color: "#10b981" },
];

const exampleGoals = [
  "Launch our AI Resume Builder in two weeks",
  "Hire 3 engineers and onboard them in 10 days",
  "Prepare Series A investor deck by Friday",
  "Reduce infrastructure costs by 30% this quarter",
  "Set up automated customer onboarding flow",
];

// ── Sidebar ──────────────────────────────────────────────────────────────────

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", id: "dashboard" },
  { icon: Target, label: "Goals", id: "goals" },
  { icon: FolderKanban, label: "Projects", id: "projects" },
  { icon: Brain, label: "Agents", id: "agents" },
  { icon: BarChart3, label: "Analytics", id: "analytics" },
  { icon: Calendar, label: "Calendar", id: "calendar" },
  { icon: Mail, label: "Emails", id: "emails" },
  { icon: GitBranch, label: "GitHub", id: "github" },
  { icon: Settings, label: "Settings", id: "settings" },
];

function Sidebar({ active, onNav }: { active: string; onNav: (id: string) => void }) {
  return (
    <div className="flex flex-col w-60 h-full border-r border-white/[0.06] bg-black/20 backdrop-blur-xl py-5 px-3">
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-3 mb-8">
        <div className="relative w-8 h-8 flex-shrink-0">
          <div className="absolute inset-0 rounded-full bg-gradient-to-br from-indigo-500 to-violet-600" />
          <div className="absolute inset-1 rounded-full bg-background" />
          <div className="absolute inset-2 rounded-full bg-gradient-to-br from-indigo-400 to-violet-500 opacity-70" />
        </div>
        <div>
          <span className="font-bold text-base text-white">
            Orbit<span className="gradient-text">OS</span>
          </span>
          <div className="flex items-center gap-1 mt-0.5">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-[10px] text-emerald-400 font-medium">8 Agents Active</span>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 space-y-0.5">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onNav(item.id)}
            className={`nav-item w-full text-left ${active === item.id ? "active" : ""}`}
          >
            <item.icon className="w-4 h-4 flex-shrink-0" />
            <span>{item.label}</span>
            {item.id === "emails" && (
              <span className="ml-auto badge-warning text-[10px] px-1.5 py-0.5">3</span>
            )}
          </button>
        ))}
      </nav>

      {/* Lemma SDK status */}
      <div className="mt-4 rounded-xl border border-indigo-500/20 bg-indigo-500/5 p-3">
        <div className="flex items-center gap-2 mb-2">
          <Zap className="w-3.5 h-3.5 text-indigo-400" />
          <span className="text-xs font-semibold text-indigo-300">Lemma SDK</span>
          <div className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
        </div>
        <p className="text-[10px] text-slate-500 leading-relaxed">
          Pod: orbitos-startup<br />
          Tables: 8 active<br />
          Workflows: 5 running
        </p>
      </div>
    </div>
  );
}

// ── Agent Card ───────────────────────────────────────────────────────────────

function AgentCard({ agent }: { agent: Agent }) {
  const statusColor = {
    active: "text-emerald-400",
    idle: "text-slate-500",
    running: "text-indigo-400",
    error: "text-red-400",
  };

  const statusLabel = {
    active: "Active",
    idle: "Standby",
    running: "Running",
    error: "Error",
  };

  return (
    <motion.div
      className={`agent-card ${agent.status === "running" ? "agent-running" : ""}`}
      whileHover={{ y: -2 }}
    >
      <div className="flex items-start justify-between mb-3">
        <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${agent.gradient} flex items-center justify-center flex-shrink-0`}>
          <agent.icon className="w-5 h-5 text-white" />
        </div>
        <div className={`flex items-center gap-1.5 text-xs ${statusColor[agent.status]}`}>
          <div className={`w-1.5 h-1.5 rounded-full bg-current ${agent.status === "running" ? "animate-pulse" : ""}`} />
          {statusLabel[agent.status]}
        </div>
      </div>
      <div>
        <h3 className="text-sm font-semibold text-white">{agent.name}</h3>
        <p className="text-xs text-slate-500 mt-0.5">{agent.currentTask || agent.role}</p>
      </div>
      <div className="mt-3 flex items-center justify-between">
        <span className="text-xs text-slate-600">{agent.tasksCompleted} tasks done</span>
        <ArrowUpRight className="w-3.5 h-3.5 text-slate-600" />
      </div>
    </motion.div>
  );
}

// ── Goal Input ───────────────────────────────────────────────────────────────

function GoalInput({ onSubmit, isProcessing }: { onSubmit: (goal: string) => void; isProcessing: boolean }) {
  const [goal, setGoal] = useState("");
  const [placeholder, setPlaceholder] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPlaceholder((p) => (p + 1) % exampleGoals.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="glass-card p-5 space-y-4">
      <div className="flex items-center gap-2">
        <Sparkles className="w-4 h-4 text-indigo-400" />
        <span className="text-sm font-semibold text-white">New Goal</span>
        <span className="badge-orbit text-[10px]">CEO Agent</span>
      </div>
      <textarea
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
        placeholder={exampleGoals[placeholder]}
        className="goal-input h-20 text-sm"
        disabled={isProcessing}
      />
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-600">
          All 8 agents will be mobilized instantly
        </span>
        <button
          onClick={() => {
            if (goal.trim()) {
              onSubmit(goal.trim());
              setGoal("");
            }
          }}
          disabled={!goal.trim() || isProcessing}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200"
          style={{
            background: (!goal.trim() || isProcessing) ? "rgba(99,102,241,0.2)" : "rgba(99,102,241,0.9)",
            color: (!goal.trim() || isProcessing) ? "#818cf8" : "white",
          }}
        >
          {isProcessing ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <Rocket className="w-4 h-4" />
              Launch
            </>
          )}
        </button>
      </div>
    </div>
  );
}

// ── Agent Execution Feed ──────────────────────────────────────────────────────

interface AgentEvent {
  id: string;
  agent: string;
  status: string;
  message: string;
  timestamp: string;
}

function AgentFeed({ events }: { events: AgentEvent[] }) {
  const feedRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (feedRef.current) {
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
    }
  }, [events]);

  const agentColors: Record<string, string> = {
    "CEO Agent": "#6366f1",
    "PM Agent": "#8b5cf6",
    "Developer Agent": "#06b6d4",
    "Operations Agent": "#10b981",
    "Communications Agent": "#ec4899",
    "HR Agent": "#f59e0b",
    "Finance Agent": "#22c55e",
    "Analytics Agent": "#3b82f6",
  };

  const statusIcon = (status: string) => {
    switch (status) {
      case "completed": return <CheckCircle className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />;
      case "running": return <RefreshCw className="w-3.5 h-3.5 text-indigo-400 flex-shrink-0 animate-spin" />;
      case "started": return <Zap className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />;
      default: return <Activity className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />;
    }
  };

  return (
    <div className="glass-card flex flex-col h-64">
      <div className="flex items-center justify-between p-4 border-b border-white/5">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-indigo-400" />
          <span className="text-sm font-semibold text-white">Agent Feed</span>
          {events.length > 0 && (
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
          )}
        </div>
        <span className="text-xs text-slate-600">{events.length} events</span>
      </div>
      <div ref={feedRef} className="flex-1 overflow-y-auto p-3 space-y-2 sidebar-scroll font-mono">
        {events.length === 0 ? (
          <p className="text-xs text-slate-600 text-center pt-8">
            Submit a goal to see agents in action...
          </p>
        ) : (
          <AnimatePresence>
            {events.map((event) => (
              <motion.div
                key={event.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-start gap-2 text-xs"
              >
                {statusIcon(event.status)}
                <span
                  className="font-semibold flex-shrink-0"
                  style={{ color: agentColors[event.agent] || "#6366f1" }}
                >
                  {event.agent}:
                </span>
                <span className="text-slate-300">{event.message}</span>
                <span className="ml-auto text-slate-600 flex-shrink-0 text-[10px]">
                  {new Date(event.timestamp).toLocaleTimeString()}
                </span>
              </motion.div>
            ))}
          </AnimatePresence>
        )}
      </div>
    </div>
  );
}

// ── Main Dashboard ────────────────────────────────────────────────────────────

export default function DashboardPage() {
  const [activeNav, setActiveNav] = useState("dashboard");
  const [agents, setAgents] = useState(AGENTS);
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [activeGoal, setActiveGoal] = useState<string | null>(null);
  const [successCount, setSuccessCount] = useState(0);
  const wsRef = useRef<WebSocket | null>(null);

  // Simulate WebSocket events for demo
  const simulateAgentExecution = useCallback(async (goalText: string) => {
    const agentSequence = [
      { agent: "CEO Agent", id: "ceo", delay: 0, tasks: [
        { msg: "Analyzing goal semantics...", status: "started" },
        { msg: "12 objectives identified ✓", status: "completed" },
      ]},
      { agent: "PM Agent", id: "pm", delay: 1500, tasks: [
        { msg: "Creating sprint plan...", status: "started" },
        { msg: "47 Jira tickets created ✓", status: "completed" },
      ]},
      { agent: "Developer Agent", id: "dev", delay: 2500, tasks: [
        { msg: "Scanning GitHub repositories...", status: "started" },
        { msg: "3 blockers found — escalating ⚠️", status: "running" },
        { msg: "Developer blockers documented ✓", status: "completed" },
      ]},
      { agent: "Operations Agent", id: "ops", delay: 3500, tasks: [
        { msg: "Creating Jira project ORBIT...", status: "started" },
        { msg: "Notion wiki updated ✓", status: "completed" },
      ]},
      { agent: "Communications Agent", id: "comms", delay: 4000, tasks: [
        { msg: "Scheduling kickoff meeting...", status: "started" },
        { msg: "4 meetings scheduled, team notified ✓", status: "completed" },
      ]},
      { agent: "HR Agent", id: "hr", delay: 4500, tasks: [
        { msg: "Checking team availability...", status: "started" },
        { msg: "8 available, 2 contractors identified ✓", status: "completed" },
      ]},
      { agent: "Finance Agent", id: "finance", delay: 5000, tasks: [
        { msg: "Estimating project budget...", status: "started" },
        { msg: "Budget: $18,400 estimate ready ✓", status: "completed" },
      ]},
      { agent: "Analytics Agent", id: "analytics", delay: 5500, tasks: [
        { msg: "Building project dashboard...", status: "started" },
        { msg: "Live dashboard + 8 KPIs configured ✓", status: "completed" },
      ]},
    ];

    let eventId = 0;

    for (const agentRun of agentSequence) {
      setTimeout(() => {
        // Update agent status
        setAgents(prev => prev.map(a =>
          a.id === agentRun.id ? { ...a, status: "running" as any, currentTask: agentRun.tasks[0].msg } : a
        ));

        agentRun.tasks.forEach((task, ti) => {
          setTimeout(() => {
            setEvents(prev => [...prev, {
              id: `evt-${++eventId}`,
              agent: agentRun.agent,
              status: task.status,
              message: task.msg,
              timestamp: new Date().toISOString(),
            }]);

            if (ti === agentRun.tasks.length - 1) {
              setAgents(prev => prev.map(a =>
                a.id === agentRun.id
                  ? { ...a, status: "active" as any, currentTask: undefined, tasksCompleted: a.tasksCompleted + 1 }
                  : a
              ));
              setSuccessCount(c => c + 1);
            }
          }, ti * 600);
        });
      }, agentRun.delay);
    }

    // Final completion
    setTimeout(() => {
      setIsProcessing(false);
      setEvents(prev => [...prev, {
        id: `evt-final`,
        agent: "CEO Agent",
        status: "completed",
        message: "✅ All agents completed. Mission success in 47 seconds.",
        timestamp: new Date().toISOString(),
      }]);
    }, 7000);
  }, []);

  const handleGoalSubmit = useCallback((goalText: string) => {
    setIsProcessing(true);
    setActiveGoal(goalText);
    setEvents([]);
    
    // Reset all agents to idle
    setAgents(AGENTS.map(a => ({ ...a, status: "idle" as any })));

    // Simulate CEO Agent starting immediately
    setEvents([{
      id: "evt-0",
      agent: "CEO Agent",
      status: "started",
      message: `Processing: "${goalText.substring(0, 50)}..."`,
      timestamp: new Date().toISOString(),
    }]);

    simulateAgentExecution(goalText);
  }, [simulateAgentExecution]);

  return (
    <div className="flex h-screen overflow-hidden bg-[#060611]">
      {/* Sidebar */}
      <Sidebar active={activeNav} onNav={setActiveNav} />

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top bar */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/[0.06] bg-black/10 backdrop-blur-xl flex-shrink-0">
          <div>
            <h1 className="text-lg font-bold text-white capitalize">{activeNav}</h1>
            <p className="text-xs text-slate-500">
              {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white/[0.03] border border-white/[0.06] text-xs text-slate-400">
              <Search className="w-3.5 h-3.5" />
              <span>Search...</span>
            </div>
            <button className="relative p-2 rounded-xl bg-white/[0.03] border border-white/[0.06] text-slate-400 hover:text-white transition-colors">
              <Bell className="w-4 h-4" />
              <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-indigo-400" />
            </button>
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-xs font-bold text-white">
              F
            </div>
          </div>
        </div>

        {/* Dashboard content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-5 sidebar-scroll">
          {/* Metrics row */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { label: "Active Goals", value: "3", change: "+1", icon: Target, color: "#6366f1" },
              { label: "Tasks Automated", value: "847", change: "+23 today", icon: Zap, color: "#10b981" },
              { label: "Hours Saved", value: "124", change: "this week", icon: Clock, color: "#f59e0b" },
              { label: "Agent Actions", value: "2,341", change: "+89 today", icon: Activity, color: "#ec4899" },
            ].map((metric, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
                className="metric-card"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-500 font-medium">{metric.label}</span>
                  <div className="w-8 h-8 rounded-xl flex items-center justify-center"
                    style={{ background: `${metric.color}15` }}>
                    <metric.icon className="w-4 h-4" style={{ color: metric.color }} />
                  </div>
                </div>
                <div className="text-3xl font-black text-white">{metric.value}</div>
                <div className="text-xs text-emerald-400">{metric.change}</div>
              </motion.div>
            ))}
          </div>

          {/* Main 3-column layout */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* Left: Goal Input + Feed */}
            <div className="lg:col-span-1 space-y-4">
              <GoalInput onSubmit={handleGoalSubmit} isProcessing={isProcessing} />
              <AgentFeed events={events} />
            </div>

            {/* Middle: Agents Grid */}
            <div className="lg:col-span-1 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-white">AI Agents</span>
                <span className="text-xs text-slate-500">8 deployed</span>
              </div>
              <div className="grid grid-cols-2 gap-3">
                {agents.map((agent) => (
                  <AgentCard key={agent.id} agent={agent} />
                ))}
              </div>
            </div>

            {/* Right: Analytics */}
            <div className="lg:col-span-1 space-y-4">
              {/* Productivity chart */}
              <div className="glass-card p-4">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-sm font-semibold text-white">Weekly Automation</span>
                  <span className="badge-success text-[10px]">+23%</span>
                </div>
                <ResponsiveContainer width="100%" height={120}>
                  <AreaChart data={productivityData}>
                    <defs>
                      <linearGradient id="colorAutomated" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="day" tick={{ fill: "#64748b", fontSize: 10 }} axisLine={false} tickLine={false} />
                    <Tooltip
                      contentStyle={{ background: "#0f0f1a", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "8px", fontSize: "11px" }}
                      labelStyle={{ color: "#94a3b8" }}
                    />
                    <Area type="monotone" dataKey="automated" stroke="#6366f1" fill="url(#colorAutomated)" strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              {/* KPI Progress */}
              <div className="glass-card p-4 space-y-4">
                <span className="text-sm font-semibold text-white">KPI Overview</span>
                {kpiData.map((kpi, i) => (
                  <div key={i} className="space-y-1.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-slate-400">{kpi.name}</span>
                      <span className="font-semibold" style={{ color: kpi.color }}>{kpi.value}%</span>
                    </div>
                    <div className="progress-orbit">
                      <motion.div
                        className="h-full rounded-full"
                        initial={{ width: 0 }}
                        animate={{ width: `${kpi.value}%` }}
                        transition={{ delay: i * 0.15, duration: 0.8 }}
                        style={{ background: kpi.color }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              {/* Active goal status */}
              {activeGoal && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="glass-card p-4 border-indigo-500/30"
                  style={{ borderColor: "rgba(99,102,241,0.3)" }}
                >
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
                    <span className="text-xs font-semibold text-indigo-300">Active Goal</span>
                  </div>
                  <p className="text-sm text-white leading-relaxed mb-3">"{activeGoal}"</p>
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                    {successCount}/8 agents complete
                  </div>
                  <div className="progress-orbit mt-2">
                    <motion.div
                      className="progress-orbit-fill"
                      animate={{ width: `${(successCount / 8) * 100}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                </motion.div>
              )}
            </div>
          </div>

          {/* Recent activity table */}
          <div className="glass-card p-4">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-semibold text-white">Recent Autonomous Actions</span>
              <button className="text-xs text-indigo-400 hover:text-indigo-300">View all →</button>
            </div>
            <div className="space-y-2">
              {[
                { agent: "PM Agent", action: "Created Sprint 1 board in Jira", time: "2 min ago", type: "jira" },
                { agent: "Comms Agent", action: "Scheduled kickoff meeting (Mon 10am)", time: "5 min ago", type: "calendar" },
                { agent: "Dev Agent", action: "Flagged 3 blockers in main-app PR #42", time: "8 min ago", type: "github" },
                { agent: "Finance Agent", action: "Generated $18,400 budget estimate", time: "12 min ago", type: "finance" },
                { agent: "Ops Agent", action: "Updated Notion project wiki", time: "15 min ago", type: "notion" },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-3 py-2.5 px-3 rounded-xl hover:bg-white/[0.02] transition-colors">
                  <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center flex-shrink-0">
                    <Zap className="w-4 h-4 text-indigo-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-white truncate">{item.action}</p>
                    <p className="text-xs text-slate-500">{item.agent}</p>
                  </div>
                  <span className="text-xs text-slate-600 flex-shrink-0">{item.time}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
