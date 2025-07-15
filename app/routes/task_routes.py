from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.task_model import Task, TaskCreate, TaskStatus
from app.crud import task_crud
from datetime import datetime
from app.crud.task_crud import list_tasks
from app.database.connection import task_collection

router = APIRouter()

@router.post("/", response_model=Task)
async def create_task(task_data: TaskCreate):
    return await task_crud.create_task(task_data)

@router.get("/", response_model=List[Task])
async def list_tasks():
    return await task_crud.list_tasks()

@router.get("/tasks", response_model=list[Task])
async def get_tasks(
    status: Optional[TaskStatus] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    try:
        print("===> Recibida solicitud GET /tasks")
        query = {}
        if status:
            query["status"] = status.value
        if start_date or end_date:
            date_filter = {}
            if start_date:
                date_filter["$gte"] = start_date
            if end_date:
                date_filter["$lte"] = end_date
            query["created_at"] = date_filter
        
        print("Consulta Mongo:", query)

        tasks_cursor = task_collection.find(query)
        tasks = []
        async for task in tasks_cursor:
            task["_id"] = str(task["_id"])
            tasks.append(Task(**task))

        print("Tareas encontradas:", tasks)
        return tasks

    except Exception as e:
        print("ERROR en get_tasks:", e)
        raise e  # Deja que FastAPI lo devuelva como 500

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str):
    task = await task_crud.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, task_data: TaskCreate):
    task = await task_crud.update_task(task_id, task_data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    deleted = await task_crud.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
