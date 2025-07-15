from datetime import datetime, timezone
from bson import ObjectId
from app.database.connection import task_collection
from pymongo import ReturnDocument
from app.models.task_model import TaskCreate, Task, TaskStatus
from typing import Optional

async def create_task(task_data: TaskCreate) -> Task:
    task_dict = task_data.model_dump()
    now = datetime.now(timezone.utc)
    task_dict.update({"created_at": now, "updated_at": now})
    result = await task_collection.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    return Task(**task_dict)


async def list_tasks(
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> list[Task]:
    query = {}

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

async def get_task(task_id: str) -> Task | None:
    doc = await task_collection.find_one({"_id": ObjectId(task_id)})
    if doc:
        doc["_id"] = str(doc["_id"])
        return Task(**doc)
    return None


async def update_task(task_id: str, task_data: TaskCreate) -> Task | None:
    now = datetime.now(timezone.utc)
    updated = await task_collection.find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": {**task_data.model_dump(), "updated_at": now}},
        return_document=ReturnDocument.AFTER
    )
    if updated:
        updated["_id"] = str(updated["_id"])
        return Task(**updated)
    return None



async def delete_task(task_id: str) -> bool:
    result = await task_collection.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count == 1
