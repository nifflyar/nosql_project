from pymongo import ASCENDING, DESCENDING
from db import (
    users_collection,
    categories_collection,
    products_collection,
    orders_collection,
)


async def create_indexes():

    # USERS
    await users_collection.create_index(
        [("email", ASCENDING)],
        unique=True,
        name="users_email_unique",
    )

    await users_collection.create_index(
        [("role", ASCENDING)],
        name="users_role_idx",
    )

    # CATEGORIES
    await categories_collection.create_index(
        [("name", ASCENDING)],
        unique=True,
        name="categories_name_unique",
    )

    # PRODUCTS
    await products_collection.create_index(
        [("category_id", ASCENDING)],
        name="products_category_idx",
    )

    await products_collection.create_index(
        [("price", ASCENDING)],
        name="products_price_idx",
    )

    await products_collection.create_index(
        [
            ("variants.size", ASCENDING),
            ("variants.color", ASCENDING),
        ],
        name="products_variants_size_color_idx",
    )

    # ORDERS
    await orders_collection.create_index(
        [("user_id", ASCENDING)],
        name="orders_user_idx",
    )

    await orders_collection.create_index(
        [("status", ASCENDING)],
        name="orders_status_idx",
    )

    await orders_collection.create_index(
        [("created_at", DESCENDING)],
        name="orders_created_at_idx",
    )

