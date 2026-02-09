from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DB_NAME]

users_collection = db.users
products_collection = db.products
categories_collection = db.categories
orders_collection = db.orders
