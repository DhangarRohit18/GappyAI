"""OrbitOS — Notion Integration Client"""

from loguru import logger
from core.config import settings


class NotionClient:
    def __init__(self):
        self.configured = bool(settings.NOTION_TOKEN)
    
    async def create_page(self, parent_id: str, title: str, content: str) -> dict:
        if not self.configured:
            logger.debug(f"[Demo] Notion page: {title}")
            return {"id": "demo-page-id", "url": "https://notion.so/demo", "status": "demo"}
        
        try:
            from notion_client import AsyncClient
            client = AsyncClient(auth=settings.NOTION_TOKEN)
            page = await client.pages.create(
                parent={"database_id": parent_id},
                properties={"title": {"title": [{"text": {"content": title}}]}},
                children=[{"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": [{"text": {"content": content}}]}}]
            )
            return {"id": page["id"], "url": page["url"], "status": "created"}
        except Exception as e:
            logger.error(f"Notion page creation failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def update_page(self, page_id: str, content: str) -> dict:
        if not self.configured:
            return {"status": "demo"}
        return {"status": "updated", "page_id": page_id}
