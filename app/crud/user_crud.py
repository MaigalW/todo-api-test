from app.models.user_model import UserCreate, UserInDB, PyObjectId
from app.core.security import hash_password
from app.database.connection import client
from bson import ObjectId

db = client.todo_db
user_collection = db.users

async def create_user(user_data: UserCreate) -> UserInDB:
    user_dict = user_data.model_dump()
    user_dict["hashed_password"] = hash_password(user_dict.pop("password"))
    result = await user_collection.insert_one(user_dict)
    user_dict["_id"] = PyObjectId(result.inserted_id)  # convertir a PyObjectId
    return UserInDB(**user_dict)

async def get_user_by_username(username: str) -> UserInDB | None:
    user = await user_collection.find_one({"username": username})
    if user:
        user["_id"] = PyObjectId(user["_id"])  # convertir a PyObjectId
        return UserInDB(**user)
    return None

async def get_user_by_id(user_id: str) -> UserInDB | None:
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = PyObjectId(user["_id"])  # convertir a PyObjectId
        return UserInDB(**user)
    return None
