from fastapi import APIRouter

from routes.categories import router as categories_router
from routes.users import router as users_router
from routes.products import router as products_router
from routes.orders import router as orders_router
from routes.auth import router as auth_router
from routes.stats import router as stats_router



routers = [
    auth_router,
    users_router,
    categories_router,
    products_router,
    orders_router,
    stats_router,
]

main_router = APIRouter()

for router in routers:
    main_router.include_router(router)