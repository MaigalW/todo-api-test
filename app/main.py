from fastapi import FastAPI
from app.routes import task_routes, auth_routes, user_routes, protected_routes
from dotenv import load_dotenv
import os

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(protected_routes.router, prefix="/protected", tags=["Protected"])

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
