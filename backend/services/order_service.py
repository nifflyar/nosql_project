from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status

from utils.handler import validate_mongodb_id
from models.order import OrderCreate, OrderStatus
from repositories.order_repo import OrderRepository
from repositories.product_repo import ProductRepository
from repositories.user_repo import UserRepository


class OrderService:
    
    def __init__(
        self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
        user_repo: UserRepository,
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.user_repo = user_repo

    async def get_orders(
        self,
        skip: int = 0,
        limit: int = 10,
        user_id: str | None = None,
        status_filter: str | None = None,
    ):

        if user_id:
            validate_mongodb_id(user_id)
        return await self.order_repo.get_orders(
            skip=skip,
            limit=limit,
            user_id=user_id,
            status=status_filter,
        )


    async def get_order_by_id(self, order_id: str):
        validate_mongodb_id(order_id)
        order = await self.order_repo.get_order_by_id(order_id)
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order


    async def create_order(self, current_user_id: str, order_data: OrderCreate):

        validate_mongodb_id(current_user_id)
        user = await self.user_repo.get_user_by_id(current_user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist",
            )

        for item in order_data.items:
            product = await self.product_repo.get_product_by_id(str(item.product_id))
            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} does not exist",
                )

            matched_variant = None
            for variant in product.get("variants", []):
                if (
                    variant["size"] == item.variant.size
                    and variant["color"] == item.variant.color
                ):
                    matched_variant = variant
                    break

            if matched_variant is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No such variant for product {item.product_id} "
                           f"({item.variant.size}, {item.variant.color})",
                )

            if matched_variant["stock"] < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product {item.product_id} "
                           f"({item.variant.size}, {item.variant.color})",
                )


        return await self.order_repo.create_order(current_user_id, order_data.items)

    async def update_order(self, order_id: str, order_data: dict):
        validate_mongodb_id(order_id)
        return await self.order_repo.update_order(order_id, order_data)

    async def delete_order(self, order_id: str):
        validate_mongodb_id(order_id)
        return await self.order_repo.delete_order(order_id)

    async def add_item_to_order(self, order_id: str, item):
        validate_mongodb_id(order_id)
        return await self.order_repo.add_item(order_id, item)


    async def remove_item_from_order(self, order_id: str, product_id: str):
        validate_mongodb_id(order_id)
        validate_mongodb_id(product_id)
        return await self.order_repo.remove_item(order_id, product_id)

    async def update_item_quantity(self, order_id: str, product_id: str, qty: int):
        validate_mongodb_id(order_id)
        validate_mongodb_id(product_id)
        return await self.order_repo.update_quantity(order_id, product_id, qty)

    async def cancel_order(self, order_id: str):
        validate_mongodb_id(order_id)
        result = await self.order_repo.cancel_order(order_id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return result
    


    async def update_order_status(
        self,
        order_id: str,
        status: OrderStatus,
    ) -> Optional[dict]:
        validate_mongodb_id(order_id)
        oid = ObjectId(order_id)
        order = await self.order_repo.get_order_by_id(oid)

        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        result = await self.order_repo.update_status(
            order_id=oid,
            status=status,
        )

        return result
