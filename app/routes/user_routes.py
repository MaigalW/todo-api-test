from fastapi import APIRouter, HTTPException, status
from app.models.user_model import UserCreate, UserInDB
from app.crud.user_crud import get_user_by_username, create_user

router = APIRouter(prefix="/users", tags=["User"])
"""
    ENDPOINT CREATED FOR INITIAL USERS CREATION 
    I thought it was important to leave it here so you can know how i did it
@router.post("/init", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def init_admin(user_data: UserCreate):
    existing_user = await get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = await create_user(user_data)
    return new_user
"""