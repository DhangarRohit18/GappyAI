from fastapi import APIRouter
router = APIRouter()

@router.post("/login")
async def login():
    return {"message": "Auth handled by Clerk"}

@router.get("/me")
async def get_me():
    return {"user": "demo@orbitos.ai", "plan": "pro"}
