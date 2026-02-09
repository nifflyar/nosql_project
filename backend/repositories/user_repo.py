from bson import ObjectId
from datetime import datetime



from db import users_collection
from models.user import UserRole



class UserRepository:
    def __init__(self):
        self.collection = users_collection


    async def get_users(self, skip: int = 0, limit: int = 10):
        cursor = (
            self.collection
            .find()
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)
    

    async def get_user_by_id(self, user_id: str | ObjectId):
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        return await self.collection.find_one({"_id": user_id})
    

    async def get_users_by_role(self, role: str, skip: int = 0, limit: int = 20):
        cursor = (
            self.collection
            .find({"role": role})
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)
    

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({"email": email})
    

    async def create_user(self, user_data: dict):
        if "role" not in user_data:
            user_data["role"] = UserRole.CUSTOMER.value

        user_data["created_at"] = datetime.utcnow()

        result = await self.collection.insert_one(user_data)
        return await self.get_user_by_id(result.inserted_id)
    

    async def update_user(self, user_id: str | ObjectId, user_data: dict):
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        await self.collection.update_one(
            {"_id": user_id},
            {"$set": user_data},
        )
        return await self.get_user_by_id(user_id)
    

    async def update_user_role(self, user_id: str | ObjectId, new_role: UserRole):
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {"role": new_role.value}},
        )
        return await self.get_user_by_id(user_id)
    

    async def delete_user(self, user_id: str | ObjectId):
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        return await self.collection.delete_one({"_id": user_id})
