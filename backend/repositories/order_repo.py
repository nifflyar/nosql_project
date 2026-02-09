from bson import ObjectId
from datetime import datetime
from typing import List, Dict, Any


from db import orders_collection, products_collection
from models.order import OrderStatus




class OrderRepository:
    def __init__(self):
        self.collection = orders_collection
        self.products = products_collection

    async def get_orders(
        self,
        skip: int = 0,
        limit: int = 10,
        user_id: str | ObjectId | None = None,
        status: str | None = None,
    ):
        query: dict = {}
        if user_id is not None:
            if isinstance(user_id, str):
                user_id = ObjectId(user_id)
            query["user_id"] = user_id

        if status is not None:
            query["status"] = status

        cursor = (
            self.collection
            .find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)



    async def get_order_by_id(self, order_id: str | ObjectId):
        if isinstance(order_id, str):
            order_id = ObjectId(order_id)
        return await self.collection.find_one({"_id": order_id})



    async def get_item_by_id_in_order(self, order_id: str | ObjectId, product_id: str | ObjectId):
        order = await self.get_order_by_id(order_id)
        if order:
            for item in order.get("items", []):
                if str(item["product_id"]) == str(product_id):
                    return item
        return None



    async def create_order(self, user_id: str | ObjectId, items: List[Any]):
    
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        serialized_items: List[Dict[str, Any]] = []
        for item in items:
            if hasattr(item, "model_dump"):
                item = item.model_dump()
            serialized_items.append(item)

        total = sum(i["price"] * i["quantity"] for i in serialized_items)

        order_doc = {
            "user_id": user_id,
            "status": OrderStatus.PENDING.value,
            "items": serialized_items,
            "total": total,
            "created_at": datetime.utcnow(),
        }


        for item in serialized_items:
            product_id = ObjectId(item["product_id"])
            size = item["variant"]["size"]
            color = item["variant"]["color"]
            qty = item["quantity"]

            await self.products.update_one(
                {
                    "_id": product_id,
                    "variants.size": size,
                    "variants.color": color,
                },
                {"$inc": {"variants.$.stock": -qty}},
            )

        result = await self.collection.insert_one(order_doc)
        return await self.get_order_by_id(result.inserted_id)



    async def update_order(self, order_id: str | ObjectId, order_data: dict):
        if isinstance(order_id, str):
            order_id = ObjectId(order_id)

        await self.collection.update_one(
            {"_id": order_id},
            {"$set": order_data},
        )
        return await self.get_order_by_id(order_id)


    async def delete_order(self, order_id: str | ObjectId):
        
        if isinstance(order_id, str):
            order_id = ObjectId(order_id)
        return await self.collection.delete_one({"_id": order_id})




    async def add_item(self, order_id: str | ObjectId, item: dict):
        if isinstance(order_id, str):
            order_id = ObjectId(order_id)

        if hasattr(item, "model_dump"):
            item = item.model_dump()

        await self.collection.update_one(
            {"_id": order_id},
            {"$push": {"items": item}},
        )
        return await self.get_order_by_id(order_id)



    async def remove_item(self, order_id: str | ObjectId, product_id: str | ObjectId):

        if isinstance(order_id, str):
            order_id = ObjectId(order_id)
        if isinstance(product_id, str):
            product_id = ObjectId(product_id)

        await self.collection.update_one(
            {"_id": order_id},
            {"$pull": {"items": {"product_id": product_id}}},
        )
        return await self.get_order_by_id(order_id)
    


    async def update_quantity(self, order_id: str | ObjectId, product_id: str | ObjectId, qty: int):

        if isinstance(order_id, str):
            order_id = ObjectId(order_id)
        if isinstance(product_id, str):
            product_id = ObjectId(product_id)

        await self.collection.update_one(
            {"_id": order_id, "items.product_id": product_id},
            {"$set": {"items.$.quantity": qty}},
        )
        return await self.get_order_by_id(order_id)



    async def update_status(self, order_id: str | ObjectId, status: OrderStatus):

        if isinstance(order_id, str):
            order_id = ObjectId(order_id)

        await self.collection.update_one(
            {"_id": order_id},
            {"$set": {"status": status.value}},
        )
        return await self.get_order_by_id(order_id)



    async def cancel_order(self, order_id: str | ObjectId):

        if isinstance(order_id, str):
            order_id = ObjectId(order_id)

        order = await self.get_order_by_id(order_id)
        if not order:
            return None

        if order.get("status") == OrderStatus.CANCELED.value:
            return order

        for item in order.get("items", []):
            product_id = ObjectId(item["product_id"])
            size = item["variant"]["size"]
            color = item["variant"]["color"]
            qty = item["quantity"]

            await self.products.update_one(
                {
                    "_id": product_id,
                    "variants.size": size,
                    "variants.color": color,
                },
                {"$inc": {"variants.$.stock": qty}},
            )

        await self.collection.update_one(
            {"_id": order_id},
            {"$set": {"status": OrderStatus.CANCELED.value}},
        )
        return await self.get_order_by_id(order_id)
