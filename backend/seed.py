import asyncio
import os
import random
from datetime import datetime, timezone

from bson import ObjectId
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient

from utils.password_hasher import hash_password

fake = Faker("en_US")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
DB_NAME = os.getenv("DB_NAME", "clothing_store")

USERS_COUNT = 100
PRODUCTS_COUNT = 100
ORDERS_COUNT = 100

SIZES = ["XS", "S", "M", "L", "XL"]
COLORS = ["Black", "White", "Beige", "Gray", "Brown", "Red", "Blue", "Green", "Pink"]


CATEGORY_POOL = [
    "Dresses",
    "Skirts",
    "Jackets",
    "Coats",
    "Shirts",
    "Blouses",
    "Sweaters",
    "Jeans",
    "Pants",
    "Tops",
    "T-Shirts",
    "Accessories",
    "Bags",
    "Glasses",
    "Shoes",
]



PRODUCT_TYPES = [
    {
        "item": "dress",
        "category": "Dresses",
        "images": [
            "https://i.pinimg.com/736x/a9/76/06/a9760668a7a7ef982f2bc00e22593f72.jpg",
            "https://backend.orbitvu.com/sites/default/files/image/flatlay-photography-automated-product-photography-dress-min.jpeg",
        ],
    },
    {
        "item": "skirt",
        "category": "Skirts",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZ9IRnuNSYMSKtyE2bNOw7-mqhO1Z9PPO8kw&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSoAPPeHUu9ASe-xGbdvLStg5OmjkxLyHx-A&s",
        ],
    },
    {
        "item": "jacket",
        "category": "Jackets",
        "images": [
            "https://shop.in-n-out.com/cdn/shop/products/ShopINO.com_VarsityJacket-ProductThumbnail.jpg?v=1642434406",
        ],
    },
    {
        "item": "coat",
        "category": "Coats",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDWxu0V_jN5MLOoJMS6mFbQJOnhlnwUkGjMg&s",
        ],
    },
    {
        "item": "shirt",
        "category": "Shirts",
        "images": [
            "https://chriscross.in/cdn/shop/files/ChrisCrossBlackCottonT-Shirt.jpg?v=1740994605&width=2048",
        ],
    },
    {
        "item": "blouse",
        "category": "Blouses",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdJgILdE5kg6DRD3EkljeLpv7UW47I4IKp4A&s",
        ],
    },
    {
        "item": "sweater",
        "category": "Sweaters",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTppA5ujTKqFaQH-nGTddj-myCd5mbD5gtbzQ&s",
        ],
    },
    {
        "item": "jeans",
        "category": "Jeans",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQS0xcX-DiNioEPRmZAfXbZhEiS_LoAQDdSIg&s",
        ],
    },
    {
        "item": "pants",
        "category": "Pants",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoiRdCuyh2f7XDRKTZMY-UMR-ka42_yTNFOA&s",
        ],
    },
    {
        "item": "top",
        "category": "Tops",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTI9SE4FpUROlvqE11DcfdtJ9uTGEK4R5oEUg&s",
        ],
    },
    {
        "item": "t-shirt",
        "category": "T-Shirts",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTI9SE4FpUROlvqE11DcfdtJ9uTGEK4R5oEUg&s",
        ],
    },
    {
        "item": "bag",
        "category": "Bags",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmVGotSDJbxxp3zwLRRptGgwbd6Le3-SJ8AA&s",
        ],
    },
    {
        "item": "glasses",
        "category": "Glasses",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRg6UeQTJqkfdm1Q02PuHdPQa_li0t8p5mGAw&s",
        ],
    },
    {
        "item": "shoes",
        "category": "Shoes",
        "images": [
            "https://media.istockphoto.com/id/1688015574/photo/white-sneaker-isolated-on-white-background.jpg?s=612x612&w=0&k=20&c=gz8bGn7h_eaF4uJGJjdZYYhJDrrigHAygo2Vi8tZjH8=",
        ],
    },
    {
        "item": "belt",
        "category": "Accessories",
        "images": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSI_NSNqTU0eKHsAluNR8UoFoKWfzlDwlBN_A&s",
        ],
    },
]

def utc_now():
    return datetime.now(timezone.utc)


def generate_product():
    adj = random.choice(
        ["Stylish", "Classic", "Lightweight", "Warm", "Elegant", "Oversized", "Slim-fit", "Relaxed"]
    )
    material = random.choice(["cotton", "wool", "linen", "viscose", "eco-leather", "denim", "cashmere"])

    ptype = random.choice(PRODUCT_TYPES)
    item = ptype["item"]
    category = ptype["category"]
    image_id = random.choice(ptype["images"])

    name = f"{adj} {material} {item}".title()

    return name, item, category, image_id


def generate_price():
    return round(random.uniform(20, 400), 2)


def build_variants():
    variants = []
    used = set()
    attempts = 0
    target = random.randint(2, 6)

    while len(variants) < target and attempts < 30:
        attempts += 1
        size = random.choice(SIZES)
        color = random.choice(COLORS)
        key = (size, color)
        if key in used:
            continue
        used.add(key)
        variants.append(
            {
                "stock": random.randint(0, 50),
                "size": size,
                "color": color,
            }
        )

    if not variants:
        variants.append({"stock": 10, "size": "M", "color": "black"})
    return variants


def pick_variant(variants):
    available = [v for v in variants if v.get("stock", 0) > 0]
    return random.choice(available) if available else random.choice(variants)


async def clear_database(db):
    await db.categories.delete_many({})
    await db.users.delete_many({})
    await db.products.delete_many({})
    await db.orders.delete_many({})


async def seed_categories(db):

    docs = []
    for name in CATEGORY_POOL:
        docs.append(
            {
                "name": name,
                "description": fake.sentence(nb_words=10),
                "created_at": utc_now(),
            }
        )

    result = await db.categories.insert_many(docs)

    return result.inserted_ids


async def seed_users(db, count=100):
    docs = []

    docs.append(
        {
            "name": "Admin",
            "email": "admin@mail.com",
            "address": fake.address(),
            "role": "admin",
            "passwordHash": hash_password("adminpass"),
            "created_at": utc_now(),
        }
    )

    used_emails = {"admin@mail.com"}

    for _ in range(count - 1):
        email = fake.unique.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)

        docs.append(
            {
                "name": fake.name(),
                "email": email,
                "address": fake.address(),
                "role": "customer",
                "passwordHash": hash_password(fake.password(length=10)),
                "created_at": utc_now(),
            }
        )

    result = await db.users.insert_many(docs)
    return result.inserted_ids


async def seed_products(db, category_ids, count=100):
    category_by_name = dict(zip(CATEGORY_POOL, category_ids))

    docs = []

    for _ in range(count):
        variants = build_variants()
        name, item, category_name, image_id = generate_product()

        cat_id = category_by_name.get(category_name)
        if not cat_id:
            cat_id = random.choice(category_ids)

        docs.append(
            {
                "name": name,
                "price": generate_price(),
                "category_id": cat_id,
                "variants": variants,
                "created_at": utc_now(),
                "image_url": image_id,
            }
        )

    result = await db.products.insert_many(docs)
    return result.inserted_ids


async def seed_orders(db, user_ids, product_docs, count=100):
    docs = []

    customer_ids = user_ids[1:] if len(user_ids) > 1 else user_ids

    for _ in range(count):
        user_id = random.choice(customer_ids)

        items = []
        total = 0.0

        chosen_products = random.sample(product_docs, k=random.randint(1, 5))

        for p in chosen_products:
            variants = p.get("variants", [])
            v = pick_variant(variants)
            qty = random.randint(1, 3)

            price = float(p["price"])
            total += price * qty

            items.append(
                {
                    "product_id": p["_id"],
                    "name": p["name"],
                    "price": price,
                    "quantity": qty,
                    "variant": {"size": v["size"], "color": v["color"]},
                }
            )

        docs.append(
            {
                "user_id": ObjectId(str(user_id)),
                "status": random.choice(["pending", "shipped", "delivered", "canceled"]),
                "items": items,
                "total": round(total, 2),
                "created_at": utc_now(),
            }
        )

    await db.orders.insert_many(docs)


async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    print("🧹Clearing database...")
    await clear_database(db)

    print("Seeding categories...")
    category_ids = await seed_categories(db)

    print("Seeding users...")
    user_ids = await seed_users(db, USERS_COUNT)

    print("Seeding products...")
    await seed_products(db, category_ids, PRODUCTS_COUNT)
    product_docs = await db.products.find().to_list(length=PRODUCTS_COUNT)

    print("Seeding orders...")
    await seed_orders(db, user_ids, product_docs, ORDERS_COUNT)

    c1 = await db.categories.count_documents({})
    c2 = await db.users.count_documents({})
    c3 = await db.products.count_documents({})
    c4 = await db.orders.count_documents({})

    print("DONE")
    print(f"categories: {c1}, users: {c2}, products: {c3}, orders: {c4}")


if __name__ == "__main__":
    asyncio.run(main())
