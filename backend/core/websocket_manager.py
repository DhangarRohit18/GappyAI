"""
OrbitOS WebSocket Manager
Handles real-time streaming of agent execution events to the dashboard.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import WebSocket
from loguru import logger


class WebSocketManager:
    """Manages WebSocket connections and broadcasts agent updates."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.message_history: Dict[str, List[Dict]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.message_history[client_id] = []
        logger.info(f"WebSocket connected: {client_id}")
        
        # Send welcome message
        await self.send_to_client(client_id, {
            "type": "connected",
            "message": "OrbitOS real-time feed active",
            "timestamp": datetime.utcnow().isoformat(),
        })
    
    async def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        logger.info(f"WebSocket disconnected: {client_id}")
    
    async def disconnect_all(self):
        for client_id in list(self.active_connections.keys()):
            await self.disconnect(client_id)
    
    async def send_to_client(self, client_id: str, data: Dict):
        websocket = self.active_connections.get(client_id)
        if websocket:
            try:
                message = json.dumps(data, default=str)
                await websocket.send_text(message)
                # Store in history
                if client_id in self.message_history:
                    self.message_history[client_id].append(data)
                    # Keep last 100 messages
                    self.message_history[client_id] = self.message_history[client_id][-100:]
            except Exception as e:
                logger.warning(f"Failed to send WebSocket message: {e}")
                await self.disconnect(client_id)
    
    async def broadcast(self, data: Dict):
        """Broadcast to all connected clients."""
        for client_id in list(self.active_connections.keys()):
            await self.send_to_client(client_id, data)
    
    async def send_agent_update(
        self,
        client_id: str,
        agent_name: str,
        status: str,
        message: str,
        data: Optional[Dict] = None,
    ):
        """Send a structured agent status update to the dashboard."""
        await self.send_to_client(client_id, {
            "type": "agent_update",
            "agent": agent_name,
            "status": status,
            "message": message,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat(),
        })
    
    async def handle_message(self, client_id: str, raw_message: str):
        """Handle incoming messages from the client."""
        try:
            data = json.loads(raw_message)
            msg_type = data.get("type", "")
            
            if msg_type == "ping":
                await self.send_to_client(client_id, {"type": "pong"})
            elif msg_type == "subscribe_goal":
                goal_id = data.get("goal_id")
                logger.info(f"Client {client_id} subscribed to goal: {goal_id}")
        except json.JSONDecodeError:
            pass


# Global singleton
websocket_manager = WebSocketManager()
