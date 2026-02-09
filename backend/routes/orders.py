
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel

from dependencies.dependency_injection import AdminDep, OrderServiceDep, CurrentUserDep
from models.order import OrderCreate, OrderResponse, OrderItem, OrderStatusUpdate, QuantityUpdate
from models.user import UserRole


router = APIRouter(prefix="/orders", tags=["Orders"])






@router.get("/my", description="Get current user's orders", response_model=list[OrderResponse])
async def get_my_orders(
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
    status_filter: str | None = None,
):
    return await order_service.get_orders(
        skip=skip,
        limit=limit,
        user_id=str(current_user.id),
        status_filter=status_filter,
    )



@router.get(
    "/",
    description="Get orders (admin: all, customer: own)",
    response_model=list[OrderResponse],
)
async def get_all_orders(
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
    status_filter: str | None = None,
):
    user_id: str | None = None
    if current_user.role == UserRole.CUSTOMER:
        user_id = str(current_user.id)

    return await order_service.get_orders(
        skip=skip,
        limit=limit,
        user_id=user_id,
        status_filter=status_filter,
    )



@router.get(
    "/{order_id}",
    description="Get order by ID",
    response_model=OrderResponse,
)
async def get_order_by_id(
    order_id: str,
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
):
    order = await order_service.get_order_by_id(order_id=order_id)
    if current_user.role == UserRole.CUSTOMER and str(order["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return order




@router.patch(
    "/{order_id}/status",
    description="Change order status (admin only, business logic + $inc stock if needed)",
    response_model=OrderResponse,
)
async def change_order_status(
    order_id: str,
    body: OrderStatusUpdate,
    order_service: OrderServiceDep,
    admin: AdminDep,
):

    return await order_service.update_order_status(
        order_id=order_id,
        status=body.status,
    )




@router.post(
    "/",
    description="Create a new order",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderResponse,
)
async def create_order(
    order_data: OrderCreate,
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
):
    return await order_service.create_order(
        current_user_id=str(current_user.id),
        order_data=order_data,
    )




@router.put(
    "/{order_id}",
    description="Update an existing order (admin only)",
    response_model=OrderResponse,
)
async def update_order(
    order_id: str,
    order_data: dict,
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    return await order_service.update_order(order_id=order_id, order_data=order_data)




@router.delete(
    "/{order_id}",
    description="Delete an order (admin only)",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order(
    order_id: str,
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    await order_service.delete_order(order_id=order_id)
    return None




@router.post(
    "/{order_id}/items",
    description="Add item to order (advanced update: $push)",
    response_model=OrderResponse,
)
async def add_item_to_order(
    order_id: str,
    item: OrderItem,
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
):
    order = await order_service.get_order_by_id(order_id)
    if current_user.role == UserRole.CUSTOMER and str(order["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    return await order_service.add_item_to_order(order_id=order_id, item=item)




@router.delete(
    "/{order_id}/items/{product_id}",
    description="Remove item from order (advanced delete: $pull)",
    response_model=OrderResponse,
)
async def remove_item_from_order(
    order_id: str,
    product_id: str,
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
):
    order = await order_service.get_order_by_id(order_id)
    if current_user.role == UserRole.CUSTOMER and str(order["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    return await order_service.remove_item_from_order(order_id=order_id, product_id=product_id)




@router.patch(
    "/{order_id}/items/{product_id}/quantity",
    description="Update item quantity (advanced update: $set with positional '$')",
    response_model=OrderResponse,
)
async def update_item_quantity_in_order(
    order_id: str,
    product_id: str,
    body: QuantityUpdate,
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
):
    order = await order_service.get_order_by_id(order_id)
    if current_user.role == UserRole.CUSTOMER and str(order["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    return await order_service.update_item_quantity(
        order_id=order_id,
        product_id=product_id,
        qty=body.quantity,
    )




@router.post(
    "/{order_id}/cancel",
    description="Cancel order (business logic + $inc stock back)",
    response_model=OrderResponse,
)
async def cancel_order(
    order_id: str,
    order_service: OrderServiceDep,
    current_user: CurrentUserDep,
):
    order = await order_service.get_order_by_id(order_id)
    if current_user.role == UserRole.CUSTOMER and str(order["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    return await order_service.cancel_order(order_id=order_id)



