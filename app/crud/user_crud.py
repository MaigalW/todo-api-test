from app.models.user_model import *
from app.core.security import hash_password
from app.database.connection import client

from bson import ObjectId

db = client.todo_db
user_collection = db.users

async def create_user_endpoint(user_data: UserCreate) -> UserInDB:
    user_dict = user_data.model_dump()
    user_dict["hashed_password"] = hash_password(user_dict.pop("password"))
    result = await user_collection.insert_one(user_dict)
    user_dict["_id"] = PyObjectId(result.inserted_id) 
    return UserInDB(**user_dict)

async def get_user_by_username(username: str) -> UserInDB | None:
    user = await user_collection.find_one({"username": username})
    if user:
        user["_id"] = PyObjectId(user["_id"]) 
        return UserInDB(**user)
    return None

async def get_user_by_id(user_id: str) -> UserInDB | None:
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = PyObjectId(user["_id"])
        return UserInDB(**user)
    return None

async def delete_user_by_username(username: str) -> bool:
    result = await user_collection.delete_one({"username": username})
    return result.deleted_count == 1

async def list_all_users() -> list[UserOut]:
    users = []
    async for doc in user_collection.find():
        users.append(UserOut(**doc))
    return users