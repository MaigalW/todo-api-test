from fastapi import APIRouter, Depends
from app.auth.dependencies import require_admin
from app.models.user_model import UserInDB

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
async def admin_dashboard(current_user: UserInDB = Depends(require_admin)):
    return {
        "message": f"Welcome, admin {current_user.username}",
        "user_id": str(current_user.id),
        "role": current_user.role
    }
