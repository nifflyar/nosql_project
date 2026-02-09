from utils.handler import validate_mongodb_id
from repositories.category_repo import CategoryRepository
from models.category import CategoryCreate

class CategoryService:

    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def get_all_categories(self, skip: int = 0, limit: int = 10):
        return await self.category_repo.get_categories(skip=skip, limit=limit)

    async def get_category_by_id(self, category_id: str):
        validate_mongodb_id(category_id)
        return await self.category_repo.get_category_by_id(category_id)

    async def create_category(self, category_data: CategoryCreate):
        category_dict = category_data.dict()
        return await self.category_repo.create_category(category_dict)

    async def update_category(self, category_id: str, category_data: dict):
        validate_mongodb_id(category_id)
        return await self.category_repo.update_category(category_id, category_data)

    async def delete_category(self, category_id: str):
        validate_mongodb_id(category_id)
        return await self.category_repo.delete_category(category_id)
