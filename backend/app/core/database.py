from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://adityakalyanv:Aditya5121@cluster0.2bk52yy.mongodb.net/")

DB_NAME = os.getenv("DB_NAME", "BudgetTracker")

client = AsyncIOMotorClient(MONGO_URL)
database = client[DB_NAME]
