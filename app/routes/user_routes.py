from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user_model import UserCreate, UserInDB
from app.crud.user_crud import *
from app.auth.dependencies import require_admin

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/create_user", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user_data: UserCreate,
    _: UserInDB = Depends(require_admin)
):
    existing_user = await get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = await create_user_endpoint(user_data)
    return new_user


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    username: str,
    _: UserInDB = Depends(require_admin) 
):
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await delete_user_by_username(username)

from app.auth.dependencies import require_admin

@router.get("/", response_model=list[UserOut])
async def get_all_users(_: UserInDB = Depends(require_admin)):
    return await list_all_users()
