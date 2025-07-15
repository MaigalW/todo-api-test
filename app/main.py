from fastapi import FastAPI
from app.routes import task_routes

app = FastAPI()

app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
