"""
OrbitOS — Core Memory Module
Implements short-term and long-term memory for AI agents using Lemma Tables + Vector DB.
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from loguru import logger


class AgentMemory:
    """
    Multi-tier memory system for OrbitOS agents.
    
    Tiers:
    1. In-prompt (context window) — current task context
    2. Lemma Tables — structured working memory  
    3. Vector DB (ChromaDB) — semantic long-term memory
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._short_term: List[Dict] = []
        self._max_short_term = 20
    
    def add_to_short_term(self, content: str, role: str = "assistant") -> None:
        """Add to in-context short-term memory."""
        self._short_term.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
        })
        # Keep within context limit
        if len(self._short_term) > self._max_short_term:
            self._short_term = self._short_term[-self._max_short_term:]
    
    def get_short_term_context(self) -> str:
        """Get formatted short-term memory for prompt injection."""
        if not self._short_term:
            return ""
        recent = self._short_term[-5:]  # Last 5 interactions
        return "\n".join([f"[{m['role']}]: {m['content'][:200]}" for m in recent])
    
    async def store_long_term(self, content: str, metadata: Dict = None) -> None:
        """Store to vector DB for long-term semantic retrieval."""
        try:
            import chromadb
            client = chromadb.HttpClient(host="localhost", port=8001)
            collection = client.get_or_create_collection(f"agent-{self.agent_id}")
            collection.add(
                documents=[content],
                metadatas=[{**(metadata or {}), "timestamp": datetime.utcnow().isoformat()}],
                ids=[f"{self.agent_id}-{datetime.utcnow().timestamp()}"],
            )
        except Exception as e:
            logger.debug(f"Long-term storage not available: {e}")
    
    async def retrieve_relevant(self, query: str, n_results: int = 3) -> List[str]:
        """Semantic search in long-term memory."""
        try:
            import chromadb
            client = chromadb.HttpClient(host="localhost", port=8001)
            collection = client.get_collection(f"agent-{self.agent_id}")
            results = collection.query(query_texts=[query], n_results=n_results)
            return results["documents"][0] if results["documents"] else []
        except Exception:
            return []
    
    def clear_short_term(self) -> None:
        self._short_term = []
