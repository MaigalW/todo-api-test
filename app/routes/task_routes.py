from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from app.models.task_model import Task, TaskCreate, TaskStatus
from app.crud import task_crud
from datetime import datetime
from app.database.connection import task_collection
from app.auth.dependencies import get_current_user
from app.models.user_model import UserInDB

router = APIRouter()


@router.post("/", response_model=Task)
async def create_task(
    task_data: TaskCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    return await task_crud.create_task(task_data, current_user)


@router.get("/", response_model=List[Task])
async def list_tasks(current_user: UserInDB = Depends(get_current_user)):
    return await task_crud.list_tasks(current_user)


@router.get("/tasks", response_model=List[Task])
async def get_tasks(
    status: Optional[TaskStatus] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        query = {}
        if current_user.role != "admin":
            query["owner_id"] = str(current_user.id)

        if status:
            query["status"] = status.value

        if start_date or end_date:
            date_filter = {}
            if start_date:
                date_filter["$gte"] = start_date
            if end_date:
                date_filter["$lte"] = end_date
            query["created_at"] = date_filter

        tasks_cursor = task_collection.find(query)
        tasks = []
        async for task in tasks_cursor:
            task["_id"] = str(task["_id"])
            tasks.append(Task(**task))

        return tasks

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str, current_user: UserInDB = Depends(get_current_user)):
    task = await task_crud.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != str(current_user.id) and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_data: TaskCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    task = await task_crud.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != str(current_user.id) and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    return await task_crud.update_task(task_id, task_data)


@router.delete("/{task_id}")
async def delete_task(task_id: str, current_user: UserInDB = Depends(get_current_user)):
    task = await task_crud.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != str(current_user.id) and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    deleted = await task_crud.delete_task(task_id)
    return {"message": "Task deleted"}
