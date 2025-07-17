from datetime import datetime, timezone
from bson import ObjectId
from app.database.connection import task_collection
from pymongo import ReturnDocument
from app.models.task_model import TaskCreate, Task, TaskStatus
from app.models.user_model import UserInDB

from typing import Optional

async def create_task(task_data: TaskCreate, current_user: UserInDB) -> Task:
    task_dict = task_data.model_dump()
    now = datetime.now(timezone.utc)
    task_dict.update({
        "owner_id": str(current_user.id),
        "created_at": now,
        "updated_at": now
    })
    result = await task_collection.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    return Task(**task_dict)


async def list_tasks(
    current_user: UserInDB,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> list[Task]:
    query = {}

    if current_user.role != "admin":
        query["owner_id"] = str(current_user.id)

    if status:
        query["status"] = status

    if start_date or end_date:
        query["created_at"] = {}
        if start_date:
            query["created_at"]["$gte"] = start_date
        if end_date:
            query["created_at"]["$lte"] = end_date

    tasks = []
    async for doc in task_collection.find(query):
        doc["_id"] = str(doc["_id"])
        tasks.append(Task(**doc))
    return tasks

async def get_task(task_id: str, current_user: UserInDB) -> Task | None:
    query = {"_id": ObjectId(task_id)}
    
    # Si no es admin, añadimos condición de propietario
    if current_user.role != "admin":
        query["owner_id"] = str(current_user.id)

    doc = await task_collection.find_one(query)
    
    if doc:
        doc["_id"] = str(doc["_id"])
        return Task(**doc)
    
    return None

async def update_task(task_id: str, task_data: TaskCreate, current_user: UserInDB) -> Task | None:
    query = {"_id": ObjectId(task_id)}
    if current_user.role != "admin":
        query["owner_id"] = str(current_user.id)

    now = datetime.now(timezone.utc)
    updated = await task_collection.find_one_and_update(
        query,
        {"$set": {**task_data.model_dump(), "updated_at": now}},
        return_document=ReturnDocument.AFTER
    )
    if updated:
        updated["_id"] = str(updated["_id"])
        return Task(**updated)
    return None

async def delete_task(task_id: str, current_user: UserInDB) -> bool:
    query = {"_id": ObjectId(task_id)}
    if current_user.role != "admin":
        query["owner_id"] = str(current_user.id)

    result = await task_collection.delete_one(query)
    return result.deleted_count == 1
