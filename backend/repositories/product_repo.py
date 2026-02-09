from bson import ObjectId
from datetime import datetime
from typing import Optional

from db import products_collection
from models.product import ProductVariant


class ProductRepository:
    def __init__(self):
        self.collection = products_collection

    async def get_products(
        self,
        skip: int = 0,
        limit: int = 10,
        category_id: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ):
        query: dict = {}

        if category_id:
            query["category_id"] = ObjectId(category_id)

        variant_filter = {}
        if size:
            variant_filter["size"] = size
        if color:
            variant_filter["color"] = color

        if variant_filter:
            query["variants"] = {"$elemMatch": variant_filter}

        if min_price is not None or max_price is not None:
            price_filter = {}
            if min_price is not None:
                price_filter["$gte"] = min_price
            if max_price is not None:
                price_filter["$lte"] = max_price
            query["price"] = price_filter

        cursor = (
            self.collection
            .find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )

        products = await cursor.to_list(length=limit)

        if variant_filter:
            for p in products:
                p["variants"] = [
                    v for v in p.get("variants", [])
                    if all(v.get(k) == val for k, val in variant_filter.items())
                ]

        return products




    async def get_product_by_id(self, product_id: str | ObjectId):
        if isinstance(product_id, str):
            product_id = ObjectId(product_id)
        return await self.collection.find_one({"_id": product_id})



    async def create_product(self, product_data: dict):
        product_data["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(product_data)
        return await self.get_product_by_id(result.inserted_id)



    async def update_product(self, product_id: str | ObjectId, data: dict):
        if isinstance(product_id, str):
            product_id = ObjectId(product_id)

        await self.collection.update_one(
            {"_id": product_id},
            {"$set": data},
        )
        return await self.get_product_by_id(product_id)

    async def delete_product(self, product_id: str | ObjectId):

        if isinstance(product_id, str):
            product_id = ObjectId(product_id)
        return await self.collection.delete_one({"_id": product_id})


    async def add_variant(self, product_id: str | ObjectId, variant: dict | ProductVariant):

        if isinstance(product_id, str):
            product_id = ObjectId(product_id)

        if hasattr(variant, "model_dump"):
            variant = variant.model_dump()

        await self.collection.update_one(
            {"_id": product_id},
            {"$push": {"variants": variant}},
        )
        return await self.get_product_by_id(product_id)



    async def remove_variant(self, product_id: str | ObjectId, size: str, color: str):

        if isinstance(product_id, str):
            product_id = ObjectId(product_id)

        await self.collection.update_one(
            {"_id": product_id},
            {"$pull": {"variants": {"size": size, "color": color}}},
        )
        return await self.get_product_by_id(product_id)

    async def update_variant_stock(
        self,
        product_id: str | ObjectId,
        size: str,
        color: str,
        diff: int,
    ):
        if isinstance(product_id, str):
            product_id = ObjectId(product_id)

        await self.collection.update_one(
            {
                "_id": product_id,
                "variants.size": size,
                "variants.color": color,
            },
            {
                "$inc": {"variants.$.stock": diff},
            },
        )
        return await self.get_product_by_id(product_id)


    async def update_variant_fields(
        self,
        product_id: str | ObjectId,
        size: str,
        color: str,
        data: dict,
    ):
        if isinstance(product_id, str):
            product_id = ObjectId(product_id)

        set_ops = {f"variants.$.{k}": v for k, v in data.items()}

        await self.collection.update_one(
            {
                "_id": product_id,
                "variants.size": size,
                "variants.color": color,
            },
            {"$set": set_ops},
        )
        return await self.get_product_by_id(product_id)
