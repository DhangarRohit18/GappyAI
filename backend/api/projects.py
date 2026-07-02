"""OrbitOS stub API modules."""

from fastapi import APIRouter

# Projects router
router = APIRouter()

@router.get("/")
async def list_projects():
    return {"projects": [], "total": 0}
