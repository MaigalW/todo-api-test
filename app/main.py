from fastapi import FastAPI
from app.routes import task_routes, auth_routes, user_routes, protected_routes
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
from app.crud.user_crud import get_user_by_username, create_user
from app.models.user_model import UserCreate

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que corre al iniciar la app
    admin_user = await get_user_by_username("admin")
    if not admin_user:
        admin = UserCreate(username="admin", password="admin", role="admin")
        await create_user(admin)
        print("Admin user created with username: admin and password: admin")
    else:
        print("Admin user already exists.")
    
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_routes.router)
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(protected_routes.router, prefix="/protected", tags=["Protected"])
