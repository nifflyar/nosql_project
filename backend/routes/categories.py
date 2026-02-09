from fastapi import APIRouter, Query, HTTPException, status

from dependencies.dependency_injection import CategoryServiceDep, AdminDep
from models.category import CategoryCreate, CategoryResponse






router = APIRouter(prefix="/categories", tags=["Categories"])





@router.get(
    "/",
    description="Get all categories",
    response_model=list[CategoryResponse],
)
async def get_all_categories(
    category_service: CategoryServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
):
    return await category_service.get_all_categories(skip=skip, limit=limit)





@router.get(
    "/{category_id}",
    description="Get category by ID",
    response_model=CategoryResponse,
)
async def get_category_by_id(
    category_id: str,
    category_service: CategoryServiceDep,
):
    category = await category_service.get_category_by_id(category_id=category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category




@router.post(
    "/",
    description="Create a new category",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category: CategoryCreate,
    category_service: CategoryServiceDep,
    admin: AdminDep,
):
    return await category_service.create_category(category_data=category)




@router.put(
    "/{category_id}",
    description="Update an existing category",
    response_model=CategoryResponse,
)
async def update_category(
    category_id: str,
    category_data: CategoryCreate,
    category_service: CategoryServiceDep,
    admin: AdminDep,
):
    return await category_service.update_category(
        category_id=category_id,
        category_data=category_data.dict(),
    )




@router.delete(
    "/{category_id}",
    description="Delete a category",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: str,
    category_service: CategoryServiceDep,
    admin: AdminDep,
):
    await category_service.delete_category(category_id=category_id)
    return None
