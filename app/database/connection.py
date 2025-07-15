import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()  # Carga variables de entorno desde .env

MONGO_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # fallback local si no está la variable
client = AsyncIOMotorClient(MONGO_URL)
db = client.todo_db
task_collection = db.tasks