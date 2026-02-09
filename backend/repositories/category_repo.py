from bson import ObjectId
from datetime import datetime



from db import categories_collection




class CategoryRepository:
    def __init__(self):
        self.collection = categories_collection


    async def get_categories(self, skip: int = 0, limit: int = 10):
        cursor = (
            self.collection
            .find()
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)


    async def get_category_by_id(self, category_id: str | ObjectId):
        if isinstance(category_id, str):
            category_id = ObjectId(category_id)
        return await self.collection.find_one({"_id": category_id})


    async def get_category_by_name(self, name: str):
        return await self.collection.find_one({"name": name})


    async def create_category(self, category_data: dict):
        category_data["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(category_data)
        return await self.get_category_by_id(result.inserted_id)


    async def update_category(self, category_id: str | ObjectId, data: dict):
        if isinstance(category_id, str):
            category_id = ObjectId(category_id)

        await self.collection.update_one(
            {"_id": category_id},
            {"$set": data},
        )
        return await self.get_category_by_id(category_id)


    async def delete_category(self, category_id: str | ObjectId):
        if isinstance(category_id, str):
            category_id = ObjectId(category_id)
        return await self.collection.delete_one({"_id": category_id})
