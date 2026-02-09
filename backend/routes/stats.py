from fastapi import APIRouter, Query

from dependencies.dependency_injection import (
    AdminDep,
    OrderRepositoryDep,
    ProductRepositoryDep,
    CategoryRepositoryDep,
)


router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get(
    "/sales-by-category",
    description="Total sales (revenue) by category",
)
async def sales_by_category(
    admin: AdminDep,
    order_repo: OrderRepositoryDep,
    product_repo: ProductRepositoryDep,
    category_repo: CategoryRepositoryDep,
):
    pipeline = [
        {"$unwind": "$items"},
        {
            "$lookup": {
                "from": product_repo.collection.name,
                "localField": "items.product_id",
                "foreignField": "_id",
                "as": "product",
            }
        },
        {"$unwind": "$product"},
        {
            "$group": {
                "_id": "$product.category_id",
                "total_revenue": {
                    "$sum": {
                        "$multiply": ["$items.price", "$items.quantity"]
                    }
                },
                "total_items": {"$sum": "$items.quantity"},
            }
        },
        {
            "$lookup": {
                "from": category_repo.collection.name,
                "localField": "_id",
                "foreignField": "_id",
                "as": "category",
            }
        },
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "_id": 0,
                "category_id": {"$toString": "$_id"}, 
                "category_name": "$category.name",
                "total_revenue": 1,
                "total_items": 1,
            }
        },
        {"$sort": {"total_revenue": -1}},
    ]

    cursor = order_repo.collection.aggregate(pipeline)
    results = [doc async for doc in cursor]
    return results





@router.get(
    "/revenue-by-month",
    description="Total revenue grouped by year-month",
)
async def revenue_by_month(
    admin: AdminDep,
    order_repo: OrderRepositoryDep,
):

    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                },
                "total_revenue": {"$sum": "$total"},
                "orders_count": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "year": "$_id.year",
                "month": "$_id.month",
                "total_revenue": 1,
                "orders_count": 1,
            }
        },
        {"$sort": {"year": 1, "month": 1}},
    ]

    cursor = order_repo.collection.aggregate(pipeline)
    results = [doc async for doc in cursor]
    return results





@router.get(
    "/top-products",
    description="Top products by quantity sold",
)
async def top_products(
    order_repo: OrderRepositoryDep,
    product_repo: ProductRepositoryDep,
    admin: AdminDep,
    limit: int = Query(10, gt=0, le=100),
):
    pipeline = [
        {"$unwind": "$items"},
        {
            "$group": {
                "_id": "$items.product_id",
                "total_quantity": {"$sum": "$items.quantity"},
                "total_revenue": {
                    "$sum": {"$multiply": ["$items.price", "$items.quantity"]}
                },
            }
        },
        {
            "$lookup": {
                "from": product_repo.collection.name,
                "localField": "_id",
                "foreignField": "_id",
                "as": "product",
            }
        },
        {"$unwind": {"path": "$product", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "_id": 0,
                "product_id": {"$toString": "$_id"}, 
                "name": "$product.name",
                "total_quantity": 1,
                "total_revenue": 1,
            }
        },
        {"$sort": {"total_quantity": -1}},
        {"$limit": limit},
    ]

    cursor = order_repo.collection.aggregate(pipeline)
    results = [doc async for doc in cursor]
    return results
