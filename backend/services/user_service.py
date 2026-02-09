from fastapi import HTTPException, status

from utils.handler import validate_mongodb_id
from models.user import UserRole, UserCreate
from utils.password_hasher import hash_password 
from repositories.user_repo import UserRepository


class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_all_users(self, skip: int = 0, limit: int = 10):
        return await self.user_repo.get_users(skip=skip, limit=limit)

    async def get_user_by_id(self, user_id: str):
        validate_mongodb_id(user_id)
        return await self.user_repo.get_user_by_id(user_id)

    async def get_users_by_role(self, role: str, skip: int = 0, limit: int = 20):
        return await self.user_repo.get_users_by_role(role, skip=skip, limit=limit)

    async def get_user_by_email(self, email: str):
        return await self.user_repo.get_user_by_email(email)

    async def create_user(self, user_data: UserCreate):
        user = await self.get_user_by_email(user_data.email)
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        hashed_password = hash_password(user_data.password)
        user_dict = user_data.dict()

        user_dict["passwordHash"] = hashed_password
        user_dict["role"] = UserRole.CUSTOMER.value
        del user_dict["password"]

        return await self.user_repo.create_user(user_dict)

    async def update_user(self, user_id: str, user_data: dict):
        validate_mongodb_id(user_id)

        if "password" in user_data:
            user_data["passwordHash"] = hash_password(user_data["password"])
            del user_data["password"]

        return await self.user_repo.update_user(user_id, user_data)

    async def update_user_role(self, user_id: str, new_role: UserRole):
        validate_mongodb_id(user_id)
        return await self.user_repo.update_user_role(user_id, new_role)

    async def delete_user(self, user_id: str):
        validate_mongodb_id(user_id)
        return await self.user_repo.delete_user(user_id)
    

    async def create_initial_admin(self):
        admin_email = "admin@mail.com"
        existing_admin = await self.get_user_by_email(admin_email)
        if existing_admin is not None:
            return


        admin_dict = {
            "name": "Initial Admin",
            "email": admin_email,
            "address": "Admin address",
            "passwordHash": hash_password("adminpass"),
            "role": UserRole.ADMIN.value,
        }

        await self.user_repo.create_user(admin_dict)