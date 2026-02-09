from fastapi import APIRouter, HTTPException, status, Query

from models.user import UserResponse, UserRole
from dependencies.dependency_injection import UserServiceDep, CurrentUserDep, AdminDep


router = APIRouter(prefix="/users", tags=["Users"])




@router.get(
    "/",
    response_model=list[UserResponse],
    description="Get all users (admin only)",
)
async def get_users(
    user_service: UserServiceDep,
    admin: AdminDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
):
    return await user_service.get_all_users(skip=skip, limit=limit)




@router.get(
    "/{user_id}",
    response_model=UserResponse,
    description="Get user by ID (self or admin)",
)
async def get_user_by_id(
    user_id: str,
    user_service: UserServiceDep,
    current_user: CurrentUserDep,
):
    if current_user.role != UserRole.ADMIN and str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    return await user_service.get_user_by_id(user_id=user_id)




@router.get(
    "/email/{email}",
    response_model=UserResponse,
    description="Get user by email (admin only)",
)
async def get_user_by_email(
    email: str,
    user_service: UserServiceDep,
    admin: AdminDep,
):
    user = await user_service.get_user_by_email(email=email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user




@router.get(
    "/role/{role}",
    response_model=list[UserResponse],
    description="Get users by role (admin only)",
)
async def get_users_by_role(
    role: UserRole,
    user_service: UserServiceDep,
    admin: AdminDep,
):
    return await user_service.get_users_by_role(role=role.value)




@router.put(
    "/{user_id}",
    description="Update user (self or admin)",
    response_model=UserResponse,
)
async def update_user(
    user_id: str,
    user_data: dict,
    user_service: UserServiceDep,
    current_user: CurrentUserDep,
):
    if current_user.role != UserRole.ADMIN and str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    return await user_service.update_user(user_id=user_id, user_data=user_data)




@router.patch(
    "/{user_id}/role",
    description="Update user role (admin only)",
    response_model=UserResponse,
)
async def update_user_role(
    user_id: str,
    new_role: UserRole,
    user_service: UserServiceDep,
    admin: AdminDep,
):
    return await user_service.update_user_role(user_id=user_id, new_role=new_role)




@router.delete(
    "/{user_id}",
    description="Delete user (admin only)",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: str,
    user_service: UserServiceDep,
    admin: AdminDep,
):
    await user_service.delete_user(user_id=user_id)
    return None
