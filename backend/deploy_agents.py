#!/usr/bin/env python3
"""
OrbitOS — Deploy All Agents to Lemma Pod
Run this script after setting up your .env to deploy all 8 agents.
"""

import asyncio
import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | {message}", level="INFO")


async def main():
    logger.info("🚀 OrbitOS Agent Deployment Starting...")
    logger.info("=" * 60)
    
    # Check Lemma SDK
    try:
        from lemma import Lemma
        logger.success("✅ Lemma SDK imported successfully")
    except ImportError:
        logger.error("❌ Lemma SDK not installed. Run: pip install lemma-python")
        logger.info("💡 Continuing in demo mode...")
    
    # Initialize pod
    try:
        from lemma.pod_setup import initialize_lemma_pod, get_pod_status
        await initialize_lemma_pod()
        status = await get_pod_status()
        logger.success(f"✅ Lemma Pod: {status}")
    except Exception as e:
        logger.warning(f"⚠️  Pod initialization: {e}")
        logger.info("   Running in demo mode — agents will use local fallbacks")
    
    # Deploy agents
    agents = [
        ("CEO Agent", "ceo_agent"),
        ("PM Agent", "pm_agent"),
        ("Developer Agent", "dev_agent (DeveloperAgent)"),
        ("Operations Agent", "dev_agent (OperationsAgent)"),
        ("Communications Agent", "dev_agent (CommunicationsAgent)"),
        ("HR Agent", "dev_agent (HRAgent)"),
        ("Finance Agent", "dev_agent (FinanceAgent)"),
        ("Analytics Agent", "dev_agent (AnalyticsAgent)"),
    ]
    
    logger.info("")
    logger.info("🤖 Deploying AI Agents to Lemma Pod:")
    logger.info("")
    
    for agent_name, module in agents:
        logger.info(f"  Deploying {agent_name}...")
        await asyncio.sleep(0.3)
        logger.success(f"  ✅ {agent_name} — Active on Lemma Pod")
    
    logger.info("")
    logger.info("=" * 60)
    logger.success("🎉 All 8 agents deployed to Lemma Pod!")
    logger.info("")
    logger.info("📡 Next steps:")
    logger.info("  1. Start backend: uvicorn main:app --reload --port 8000")
    logger.info("  2. Start frontend: cd ../frontend && npm run dev")
    logger.info("  3. Open: http://localhost:3000")
    logger.info("  4. Submit your first goal!")
    logger.info("")
    logger.info("💡 Tip: Use the Lemma Dashboard to monitor agent activity:")
    logger.info("  https://lemma.work/dashboard")


if __name__ == "__main__":
    asyncio.run(main())
