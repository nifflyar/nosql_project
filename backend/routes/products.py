from fastapi import APIRouter, Query, HTTPException, status


from dependencies.dependency_injection import ProductServiceDep, AdminDep
from models.product import ProductCreate, ProductResponse, ProductVariant





router = APIRouter(prefix="/products", tags=["Products"])





@router.get(
    "/",
    response_model=list[ProductResponse],
    description="Get all products with optional filters",
)
async def get_all_products(
    product_service: ProductServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
    category_id: str | None = None,
    size: str | None = None,
    color: str | None = None,
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
):
    return await product_service.get_all_products(
        skip=skip,
        limit=limit,
        category_id=category_id,
        size=size,
        color=color,
        min_price=min_price,
        max_price=max_price,
    )





@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    description="Get product by ID",
)
async def get_product_by_id(
    product_id: str,
    product_service: ProductServiceDep,
):
    return await product_service.get_product_by_id(product_id=product_id)





@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse,
    description="Create a new product (admin only)",
)
async def create_product(
    product_data: ProductCreate,
    product_service: ProductServiceDep,
    admin: AdminDep,
):
    return await product_service.create_product(product_data=product_data)




@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    description="Partially update product fields (admin only)",
)
async def update_product(
    product_id: str,
    product_data: ProductCreate,
    product_service: ProductServiceDep,
    admin: AdminDep,
):
    if not product_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update",
        )
    return await product_service.update_product(product_id=product_id, product_data=product_data.dict())




@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a product (admin only)",
)
async def delete_product(
    product_id: str,
    product_service: ProductServiceDep,
    admin: AdminDep,
):
    await product_service.delete_product(product_id=product_id)
    return None




@router.post(
    "/{product_id}/variants",
    response_model=ProductResponse,
    description="Add a new variant (admin only)",
)
async def add_variant_to_product(
    product_id: str,
    variant: ProductVariant,
    product_service: ProductServiceDep,
    admin: AdminDep,
):
    return await product_service.add_variant(product_id=product_id, variant=variant)




@router.delete(
    "/{product_id}/variants",
    response_model=ProductResponse,
    description="Remove variant by size/color (admin only)",
)
async def remove_variant_from_product(
    product_id: str,
    size: str,
    color: str,
    product_service: ProductServiceDep,
    admin: AdminDep,
):
    return await product_service.remove_variant(product_id=product_id, size=size, color=color)




@router.patch(
    "/{product_id}/variants/stock",
    response_model=ProductResponse,
    description="Change variant stock by diff (admin only, uses $inc + positional '$')",
)
async def change_variant_stock(
    product_id: str,
    size: str,
    color: str,
    product_service: ProductServiceDep,
    admin: AdminDep,
    diff: int = Query(..., description="Positive or negative integer"),
):
    return await product_service.update_variant_stock(
        product_id=product_id,
        size=size,
        color=color,
        diff=diff,
    )




@router.patch(
    "/{product_id}/variants/fields",
    response_model=ProductResponse,
    description="Partially update variant fields (admin only, uses $set + positional '$')",
)
async def update_variant_fields(
    product_id: str,
    size: str,
    color: str,
    data: dict,
    product_service: ProductServiceDep,
    admin: AdminDep,
):

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update",
        )

    return await product_service.update_variant_fields(
        product_id=product_id,
        size=size,
        color=color,
        data=data,
    )
