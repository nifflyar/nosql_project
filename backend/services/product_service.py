from fastapi import HTTPException, status

from utils.handler import validate_mongodb_id
from models.product import ProductCreate, ProductVariant
from repositories.product_repo import ProductRepository
from repositories.category_repo import CategoryRepository


class ProductService:

    def __init__(self, product_repo: ProductRepository, category_repo: CategoryRepository):
        self.product_repo = product_repo
        self.category_repo = category_repo

    async def get_all_products(
        self,
        skip: int = 0,
        limit: int = 10,
        category_id: str | None = None,
        size: str | None = None,
        color: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ):
        return await self.product_repo.get_products(
            skip=skip,
            limit=limit,
            category_id=category_id,
            size=size,
            color=color,
            min_price=min_price,
            max_price=max_price,
        )

    async def get_product_by_id(self, product_id: str):
        validate_mongodb_id(product_id)
        product = await self.product_repo.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    async def create_product(self, product_data: ProductCreate):
        product_dict = product_data.dict()

        category = await self.category_repo.get_category_by_id(product_dict["category_id"])
        if category is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category ID")

        return await self.product_repo.create_product(product_dict)

    async def update_product(self, product_id: str, product_data: dict):
        validate_mongodb_id(product_id)
        return await self.product_repo.update_product(product_id, product_data)

    async def delete_product(self, product_id: str):
        validate_mongodb_id(product_id)
        return await self.product_repo.delete_product(product_id)



    async def add_variant(self, product_id: str, variant: ProductVariant):
        validate_mongodb_id(product_id)
        return await self.product_repo.add_variant(product_id, variant)

    async def remove_variant(self, product_id: str, size: str, color: str):
        validate_mongodb_id(product_id)
        return await self.product_repo.remove_variant(product_id, size, color)

    async def update_variant_stock(self, product_id: str, size: str, color: str, diff: int):
        validate_mongodb_id(product_id)
        return await self.product_repo.update_variant_stock(product_id, size, color, diff)

    async def update_variant_fields(self, product_id: str, size: str, color: str, data: dict):
        validate_mongodb_id(product_id)
        return await self.product_repo.update_variant_fields(product_id, size, color, data)
