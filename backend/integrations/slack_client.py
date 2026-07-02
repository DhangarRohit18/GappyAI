"""
OrbitOS — Slack Integration Client
"""

from typing import Optional
from loguru import logger
from core.config import settings


class SlackClient:
    def __init__(self):
        self.configured = bool(settings.SLACK_BOT_TOKEN)
    
    async def send_message(self, channel: str, text: str, blocks: Optional[list] = None) -> dict:
        if not self.configured:
            logger.debug(f"[Demo] Slack → {channel}: {text[:50]}")
            return {"ok": True, "demo": True}
        
        try:
            from slack_sdk.web.async_client import AsyncWebClient
            client = AsyncWebClient(token=settings.SLACK_BOT_TOKEN)
            result = await client.chat_postMessage(channel=channel, text=text, blocks=blocks)
            return {"ok": result["ok"]}
        except Exception as e:
            logger.error(f"Slack send failed: {e}")
            return {"ok": False, "error": str(e)}
    
    async def notify_team(self, message: str, channel: str = None) -> dict:
        ch = channel or settings.SLACK_DEFAULT_CHANNEL
        return await self.send_message(ch, f"🤖 OrbitOS: {message}")
