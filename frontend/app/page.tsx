"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Brain, Rocket, Zap, GitBranch, Mail, Users, DollarSign, BarChart3,
  ArrowRight, Star, CheckCircle, Play, Sparkles, Globe, Shield, Clock,
  ChevronRight, Terminal, Layers, Cpu
} from "lucide-react";
import Link from "next/link";

// ── Agent data ──────────────────────────────────────────────────────────────
const agents = [
  { icon: Brain, name: "CEO Agent", role: "Goal Decomposition & Delegation", color: "from-indigo-500 to-violet-600", delay: 0 },
  { icon: Layers, name: "PM Agent", role: "Sprint Planning & Roadmaps", color: "from-violet-500 to-purple-600", delay: 0.1 },
  { icon: GitBranch, name: "Developer Agent", role: "GitHub & Code Analysis", color: "from-cyan-500 to-blue-600", delay: 0.2 },
  { icon: Terminal, name: "Operations Agent", role: "Jira, Notion & Docs", color: "from-emerald-500 to-teal-600", delay: 0.3 },
  { icon: Mail, name: "Comms Agent", role: "Email, Slack & Meetings", color: "from-pink-500 to-rose-600", delay: 0.4 },
  { icon: Users, name: "HR Agent", role: "Hiring & Onboarding", color: "from-orange-500 to-amber-600", delay: 0.5 },
  { icon: DollarSign, name: "Finance Agent", role: "Budget & Invoicing", color: "from-green-500 to-emerald-600", delay: 0.6 },
  { icon: BarChart3, name: "Analytics Agent", role: "Dashboards & Reports", color: "from-blue-500 to-indigo-600", delay: 0.7 },
];

const features = [
  { icon: Cpu, title: "Lemma SDK Powered", desc: "Deep native integration — not an API wrapper. Every agent uses Lemma Pods, Tables, Workflows, and Connectors natively.", color: "text-indigo-400" },
  { icon: Zap, title: "Autonomous Execution", desc: "Just say your goal. OrbitOS handles planning, delegation, execution, and reporting — all automatically.", color: "text-violet-400" },
  { icon: Globe, title: "12+ Integrations", desc: "GitHub, Slack, Gmail, Jira, Notion, Google Calendar, Linear, Zoom and more — all connected.", color: "text-cyan-400" },
  { icon: Shield, title: "Human-in-the-Loop", desc: "Built-in approval workflows using Lemma Approvals for high-stakes decisions. You stay in control.", color: "text-emerald-400" },
  { icon: Clock, title: "Long-Term Memory", desc: "Agents remember past goals, outcomes, and context via Lemma Tables and vector search.", color: "text-amber-400" },
  { icon: Star, title: "Investor Ready", desc: "Auto-generated weekly reports, KPI dashboards, and investor updates. Always be prepared.", color: "text-pink-400" },
];

const stats = [
  { value: "10hrs", label: "Saved per day per founder", suffix: "+" },
  { value: "8", label: "Specialized AI agents", suffix: "" },
  { value: "12", label: "Tool integrations", suffix: "+" },
  { value: "47s", label: "Average goal-to-plan time", suffix: "" },
];

// ── Demo terminal simulation ─────────────────────────────────────────────────
const demoLines = [
  { delay: 0, text: '> "Launch our AI Resume Builder in two weeks"', type: "input" },
  { delay: 0.8, text: "🧠 CEO Agent: Analyzing goal...", type: "agent" },
  { delay: 1.4, text: "🧠 CEO Agent: 12 objectives identified ✓", type: "success" },
  { delay: 2.0, text: "📋 PM Agent: Creating sprint plan...", type: "agent" },
  { delay: 2.6, text: "📋 PM Agent: 47 Jira tickets created ✓", type: "success" },
  { delay: 3.2, text: "💻 Dev Agent: Scanning GitHub...", type: "agent" },
  { delay: 3.8, text: "💻 Dev Agent: 3 blockers identified ✓", type: "warning" },
  { delay: 4.2, text: "⚙️  Ops Agent: Updating Notion docs...", type: "agent" },
  { delay: 4.6, text: "📧 Comms Agent: 4 meetings scheduled ✓", type: "success" },
  { delay: 5.0, text: "👥 HR Agent: Team availability confirmed ✓", type: "success" },
  { delay: 5.4, text: "💰 Finance Agent: Budget: $18,400 estimated ✓", type: "success" },
  { delay: 5.8, text: "📊 Analytics Agent: Dashboard live ✓", type: "success" },
  { delay: 6.4, text: "✅ All agents complete in 47 seconds.", type: "complete" },
];

// ── Components ───────────────────────────────────────────────────────────────

function OrbitOSLogo() {
  return (
    <div className="relative flex items-center gap-2.5">
      <div className="relative w-8 h-8">
        <div className="absolute inset-0 rounded-full bg-gradient-to-br from-indigo-500 to-violet-600" />
        <div className="absolute inset-1 rounded-full bg-background" />
        <div className="absolute inset-2 rounded-full bg-gradient-to-br from-indigo-500 to-violet-600 opacity-60" />
      </div>
      <span className="font-bold text-xl tracking-tight text-white">
        Orbit<span className="gradient-text">OS</span>
      </span>
    </div>
  );
}

function DemoTerminal() {
  const [visibleLines, setVisibleLines] = useState<number[]>([]);
  const [running, setRunning] = useState(false);
  const terminalRef = useRef<HTMLDivElement>(null);

  const runDemo = () => {
    setRunning(true);
    setVisibleLines([]);
    demoLines.forEach((line, i) => {
      setTimeout(() => {
        setVisibleLines((prev) => [...prev, i]);
        if (terminalRef.current) {
          terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
        }
      }, line.delay * 1000);
    });
    setTimeout(() => setRunning(false), 7000);
  };

  const lineColor = (type: string) => {
    switch (type) {
      case "input": return "text-white font-semibold";
      case "success": return "text-emerald-400";
      case "warning": return "text-amber-400";
      case "agent": return "text-indigo-300";
      case "complete": return "text-violet-400 font-semibold";
      default: return "text-slate-300";
    }
  };

  return (
    <div className="relative rounded-2xl overflow-hidden border border-white/10 bg-black/40 backdrop-blur-xl">
      {/* Terminal header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-white/10 bg-white/[0.02]">
        <div className="w-3 h-3 rounded-full bg-red-500/70" />
        <div className="w-3 h-3 rounded-full bg-amber-500/70" />
        <div className="w-3 h-3 rounded-full bg-emerald-500/70" />
        <span className="ml-2 text-xs text-slate-500 font-mono">orbitos — autonomous execution</span>
      </div>

      {/* Terminal body */}
      <div ref={terminalRef} className="p-5 h-64 overflow-y-auto font-mono text-sm space-y-1.5 sidebar-scroll">
        {visibleLines.length === 0 && (
          <p className="text-slate-600">Click "Run Demo" to see OrbitOS in action...</p>
        )}
        <AnimatePresence>
          {visibleLines.map((lineIdx) => (
            <motion.p
              key={lineIdx}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
              className={lineColor(demoLines[lineIdx].type)}
            >
              {demoLines[lineIdx].text}
            </motion.p>
          ))}
        </AnimatePresence>
        {running && (
          <motion.span
            animate={{ opacity: [1, 0, 1] }}
            transition={{ duration: 0.8, repeat: Infinity }}
            className="inline-block w-2 h-4 bg-indigo-400 ml-1"
          />
        )}
      </div>

      {/* Run button */}
      <div className="px-5 py-4 border-t border-white/10 flex items-center justify-between">
        <span className="text-xs text-slate-500">Goal → Plan → Execute → Report</span>
        <button
          onClick={runDemo}
          disabled={running}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200"
          style={{
            background: running ? "rgba(99,102,241,0.2)" : "rgba(99,102,241,0.9)",
            color: running ? "#818cf8" : "white",
          }}
        >
          <Play className="w-3.5 h-3.5" />
          {running ? "Running..." : "Run Demo"}
        </button>
      </div>
    </div>
  );
}

// ── Main Landing Page ────────────────────────────────────────────────────────
export default function LandingPage() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-[#060611] text-white overflow-x-hidden">
      {/* Stars background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {Array.from({ length: 60 }).map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-white"
            style={{
              width: Math.random() * 2 + 1,
              height: Math.random() * 2 + 1,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              opacity: Math.random() * 0.5 + 0.1,
              animation: `twinkle ${Math.random() * 3 + 2}s ease-in-out infinite`,
              animationDelay: `${Math.random() * 3}s`,
            }}
          />
        ))}
      </div>

      {/* Gradient orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 rounded-full opacity-10 blur-3xl"
          style={{ background: "radial-gradient(circle, #6366f1, transparent)" }} />
        <div className="absolute top-1/3 -right-40 w-80 h-80 rounded-full opacity-8 blur-3xl"
          style={{ background: "radial-gradient(circle, #8b5cf6, transparent)" }} />
        <div className="absolute -bottom-40 left-1/3 w-96 h-96 rounded-full opacity-6 blur-3xl"
          style={{ background: "radial-gradient(circle, #ec4899, transparent)" }} />
      </div>

      {/* Navigation */}
      <motion.nav
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 md:px-12 py-4"
        style={{
          background: scrollY > 50 ? "rgba(6, 6, 17, 0.8)" : "transparent",
          backdropFilter: scrollY > 50 ? "blur(20px)" : "none",
          borderBottom: scrollY > 50 ? "1px solid rgba(255,255,255,0.05)" : "none",
          transition: "all 0.3s",
        }}
      >
        <OrbitOSLogo />
        <div className="hidden md:flex items-center gap-8 text-sm text-slate-400">
          <Link href="#features" className="hover:text-white transition-colors">Features</Link>
          <Link href="#agents" className="hover:text-white transition-colors">Agents</Link>
          <Link href="#demo" className="hover:text-white transition-colors">Demo</Link>
          <Link href="#pricing" className="hover:text-white transition-colors">Pricing</Link>
        </div>
        <div className="flex items-center gap-3">
          <span className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border border-indigo-500/30 text-indigo-400 bg-indigo-500/10">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
            Powered by Lemma SDK
          </span>
          <Link href="/dashboard" className="btn-orbit text-sm py-2 px-4">
            Launch Dashboard →
          </Link>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex flex-col items-center justify-center px-6 pt-20 pb-16 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-5xl mx-auto space-y-8"
        >
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium border border-indigo-500/30 bg-indigo-500/10 text-indigo-300"
          >
            <Sparkles className="w-4 h-4" />
            Gappy AI Hackathon — Built with Lemma SDK
          </motion.div>

          {/* Main headline */}
          <div className="space-y-4">
            <h1 className="text-6xl md:text-8xl font-black tracking-tight leading-none">
              <span className="text-white">The Autonomous</span>
              <br />
              <span className="gradient-text">Operating System</span>
              <br />
              <span className="text-white">for Startups</span>
            </h1>
            <p className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto font-light leading-relaxed">
              One AI Employee. Infinite Productivity.
              <br />
              <span className="text-slate-300">
                Say your goal. OrbitOS handles everything else.
              </span>
            </p>
          </div>

          {/* Hero CTA */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/dashboard">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="btn-orbit flex items-center gap-2 text-base py-3.5 px-8"
              >
                <Rocket className="w-5 h-5" />
                Launch Your Startup OS
                <ArrowRight className="w-4 h-4" />
              </motion.button>
            </Link>
            <a href="#demo">
              <motion.button
                whileHover={{ scale: 1.02 }}
                className="flex items-center gap-2 px-8 py-3.5 rounded-xl text-base font-semibold text-slate-300 border border-white/10 hover:border-white/20 transition-all duration-200"
                style={{ background: "rgba(255,255,255,0.03)" }}
              >
                <Play className="w-4 h-4 text-indigo-400" />
                Watch Demo
              </motion.button>
            </a>
          </div>

          {/* Social proof */}
          <div className="flex items-center justify-center gap-6 text-sm text-slate-500">
            {[
              "✅ No setup required",
              "✅ 8 AI agents ready",
              "✅ 12+ integrations",
            ].map((item) => (
              <span key={item}>{item}</span>
            ))}
          </div>
        </motion.div>

        {/* Dashboard preview */}
        <motion.div
          initial={{ opacity: 0, y: 60 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.8 }}
          className="relative mt-20 max-w-6xl mx-auto w-full"
        >
          <div className="relative rounded-3xl overflow-hidden border border-white/10"
            style={{ boxShadow: "0 40px 100px rgba(99,102,241,0.2), 0 0 0 1px rgba(255,255,255,0.05)" }}
          >
            {/* Browser chrome */}
            <div className="flex items-center gap-2 px-4 py-3 bg-white/[0.02] border-b border-white/5">
              <div className="w-3 h-3 rounded-full bg-red-500/60" />
              <div className="w-3 h-3 rounded-full bg-amber-500/60" />
              <div className="w-3 h-3 rounded-full bg-green-500/60" />
              <div className="flex-1 mx-4 rounded-md py-1 px-3 text-xs text-slate-500 bg-white/[0.03] text-center">
                orbitos.ai/dashboard
              </div>
            </div>
            {/* Dashboard mockup content */}
            <DashboardMockup />
          </div>
          {/* Glow effect under dashboard */}
          <div className="absolute -bottom-20 left-1/2 -translate-x-1/2 w-3/4 h-20 blur-3xl opacity-40 rounded-full"
            style={{ background: "linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899)" }} />
        </motion.div>
      </section>

      {/* Stats */}
      <section className="relative py-16 px-6">
        <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
          {stats.map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              viewport={{ once: true }}
              className="text-center space-y-1"
            >
              <div className="text-4xl md:text-5xl font-black gradient-text">
                {stat.value}{stat.suffix}
              </div>
              <div className="text-sm text-slate-500">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Agents Section */}
      <section id="agents" className="relative py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16 space-y-4"
          >
            <div className="badge-orbit mx-auto w-fit">8 Specialized AI Agents</div>
            <h2 className="text-4xl md:text-5xl font-black">
              Your entire C-suite,
              <br />
              <span className="gradient-text">powered by Lemma SDK</span>
            </h2>
            <p className="text-slate-400 max-w-2xl mx-auto text-lg">
              Each agent is a Lemma-native AI with its own Pod memory, tool access, and workflow integration.
              They communicate, delegate, and collaborate autonomously.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {agents.map((agent, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: agent.delay }}
                viewport={{ once: true }}
                whileHover={{ y: -4, scale: 1.02 }}
                className="glass-card p-5 space-y-4 group cursor-default"
              >
                <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${agent.color} flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
                  <agent.icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-sm">{agent.name}</h3>
                  <p className="text-slate-500 text-xs mt-1">{agent.role}</p>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  <span className="text-xs text-emerald-400">Active</span>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Agent flow diagram */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="mt-12 glass-card p-8"
          >
            <h3 className="text-center text-lg font-semibold text-slate-300 mb-8">
              Lemma SDK Orchestration Flow
            </h3>
            <div className="flex flex-wrap items-center justify-center gap-3 text-sm">
              {[
                "Founder Goal",
                "CEO Agent (Lemma Workflow)",
                "Task Graph",
                "7 Parallel Agents",
                "Lemma Tables (Memory)",
                "Tool Execution",
                "Result Aggregation",
                "Executive Report",
              ].map((step, i, arr) => (
                <div key={i} className="flex items-center gap-3">
                  <div className="px-3 py-2 rounded-xl border border-indigo-500/30 bg-indigo-500/10 text-indigo-300 text-xs font-medium">
                    {step}
                  </div>
                  {i < arr.length - 1 && (
                    <ChevronRight className="w-4 h-4 text-slate-600 flex-shrink-0" />
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Demo Section */}
      <section id="demo" className="relative py-24 px-6 bg-gradient-to-b from-transparent via-indigo-950/10 to-transparent">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12 space-y-4"
          >
            <div className="badge-orbit mx-auto w-fit">Live Demo</div>
            <h2 className="text-4xl md:text-5xl font-black">
              See OrbitOS
              <br />
              <span className="gradient-text">think and act</span>
            </h2>
            <p className="text-slate-400 text-lg">
              One goal. 8 agents. 47 seconds. Complete execution.
            </p>
          </motion.div>
          <DemoTerminal />
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16 space-y-4"
          >
            <h2 className="text-4xl md:text-5xl font-black">
              Built different.
              <br />
              <span className="gradient-text">Built on Lemma.</span>
            </h2>
          </motion.div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
                viewport={{ once: true }}
                className="glass-card p-6 space-y-3 hover:border-white/[0.12] transition-all duration-300"
              >
                <feature.icon className={`w-8 h-8 ${feature.color}`} />
                <h3 className="text-white font-bold">{feature.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-32 px-6 text-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="max-w-4xl mx-auto"
        >
          <div className="relative glass-card p-16 overflow-hidden">
            <div className="absolute inset-0 opacity-10"
              style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899)" }} />
            <div className="relative space-y-6">
              <h2 className="text-5xl md:text-6xl font-black">
                Ready to hire your
                <br />
                <span className="gradient-text">AI COO?</span>
              </h2>
              <p className="text-xl text-slate-400 max-w-xl mx-auto">
                Launch OrbitOS and let your AI team handle the operational work while you focus on building.
              </p>
              <Link href="/dashboard">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.98 }}
                  className="btn-orbit text-lg py-4 px-12 inline-flex items-center gap-3"
                >
                  <Rocket className="w-5 h-5" />
                  Start for Free
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
              </Link>
              <p className="text-sm text-slate-600">
                No credit card required · Powered by Lemma SDK · Built for Gappy AI Hackathon
              </p>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-12 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <OrbitOSLogo />
          <p className="text-sm text-slate-600">
            © 2026 OrbitOS · Built for the Gappy AI Hackathon · Powered by Lemma SDK
          </p>
          <div className="flex items-center gap-4 text-sm text-slate-500">
            <Link href="/dashboard" className="hover:text-white transition-colors">Dashboard</Link>
            <Link href="#" className="hover:text-white transition-colors">GitHub</Link>
            <Link href="#" className="hover:text-white transition-colors">Discord</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}

// ── Dashboard Mockup Component ────────────────────────────────────────────────
function DashboardMockup() {
  const mockAgents = [
    { name: "CEO Agent", status: "active", task: "Planning goal execution...", color: "#6366f1" },
    { name: "PM Agent", status: "active", task: "Creating sprint board...", color: "#8b5cf6" },
    { name: "Dev Agent", status: "idle", task: "Monitoring GitHub...", color: "#06b6d4" },
    { name: "Comms Agent", status: "active", task: "Drafting meeting invites...", color: "#ec4899" },
  ];

  return (
    <div className="bg-[#070714] p-6 min-h-[360px] flex gap-4">
      {/* Sidebar */}
      <div className="hidden md:flex flex-col gap-1 w-44 flex-shrink-0">
        {["Dashboard", "Projects", "Agents", "Analytics", "Calendar", "Emails"].map((item, i) => (
          <div key={i} className={`px-3 py-2 rounded-lg text-xs flex items-center gap-2 ${i === 0 ? "bg-indigo-500/20 text-indigo-300" : "text-slate-500"}`}>
            <div className="w-1.5 h-1.5 rounded-full bg-current opacity-50" />
            {item}
          </div>
        ))}
      </div>

      {/* Main content */}
      <div className="flex-1 space-y-4">
        {/* Goal input area */}
        <div className="rounded-xl border border-indigo-500/30 bg-indigo-500/5 p-4">
          <p className="text-xs text-indigo-400 font-medium mb-2">Active Goal</p>
          <p className="text-sm text-white font-medium">"Launch our AI Resume Builder in two weeks"</p>
          <div className="mt-3 flex items-center gap-2">
            <div className="flex-1 h-1 rounded-full bg-white/5">
              <div className="h-full w-2/3 rounded-full" style={{ background: "linear-gradient(90deg, #6366f1, #8b5cf6)" }} />
            </div>
            <span className="text-xs text-slate-500">67%</span>
          </div>
        </div>

        {/* Agent grid */}
        <div className="grid grid-cols-2 gap-3">
          {mockAgents.map((agent, i) => (
            <div key={i} className="rounded-xl border border-white/5 bg-white/[0.02] p-3">
              <div className="flex items-center gap-2 mb-2">
                <div className={`w-2 h-2 rounded-full ${agent.status === "active" ? "animate-pulse" : ""}`}
                  style={{ backgroundColor: agent.color }} />
                <span className="text-xs font-medium text-slate-300">{agent.name}</span>
              </div>
              <p className="text-xs text-slate-500">{agent.task}</p>
            </div>
          ))}
        </div>

        {/* Quick metrics */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: "Tasks", value: "47", color: "#6366f1" },
            { label: "Blockers", value: "3", color: "#f59e0b" },
            { label: "Done", value: "89%", color: "#10b981" },
          ].map((m, i) => (
            <div key={i} className="rounded-xl border border-white/5 bg-white/[0.02] p-3 text-center">
              <div className="text-xl font-black" style={{ color: m.color }}>{m.value}</div>
              <div className="text-xs text-slate-500">{m.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
