from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/guarani_appstore')
DB_NAME = os.environ.get('DB_NAME', 'guarani_appstore')

# Create MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Collections
users_collection = db['users']
services_collection = db['services']
orders_collection = db['orders']
transactions_collection = db['transactions']
leads_collection = db['leads']
conversations_collection = db['conversations']
blog_posts_collection = db['blog_posts']
password_resets_collection = db['password_resets']
payments_collection = db['payments']

# Dependency for FastAPI
async def get_db():
    return db
