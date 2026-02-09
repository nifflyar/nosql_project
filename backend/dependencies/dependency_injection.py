from typing import Annotated

from fastapi import Depends, Request, HTTPException, status
from pydantic import BaseModel




from core.security import decode_token  
from core.config import settings   

from repositories.product_repo import ProductRepository
from repositories.category_repo import CategoryRepository
from repositories.user_repo import UserRepository
from repositories.order_repo import OrderRepository

from services.product_service import ProductService
from services.category_service import CategoryService
from services.user_service import UserService
from services.order_service import OrderService
from services.auth_service import AuthService

from models.user import UserResponse, UserRole




class TokenPayload(BaseModel):
    sub: str | None = None
    role: str | None = None
    exp: int | None = None


# Repository Getters

async def get_product_repo() -> ProductRepository:
    return ProductRepository()


async def get_category_repo() -> CategoryRepository:
    return CategoryRepository()


async def get_user_repo() -> UserRepository:
    return UserRepository()


async def get_order_repo() -> OrderRepository:
    return OrderRepository()

# Repository Dependencies

ProductRepositoryDep = Annotated[ProductRepository, Depends(get_product_repo)]
CategoryRepositoryDep = Annotated[CategoryRepository, Depends(get_category_repo)]
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repo)]
OrderRepositoryDep = Annotated[OrderRepository, Depends(get_order_repo)]



# Service Getters

async def get_product_service(
    product_repo: ProductRepositoryDep,
    category_repo: CategoryRepositoryDep,
) -> ProductService:
    return ProductService(product_repo, category_repo)


async def get_category_service(
    category_repo: CategoryRepositoryDep,
) -> CategoryService:
    return CategoryService(category_repo)


async def get_user_service(
    user_repo: UserRepositoryDep,
) -> UserService:
    return UserService(user_repo)


async def get_order_service(
    order_repo: OrderRepositoryDep,
    product_repo: ProductRepositoryDep,
    user_repo: UserRepositoryDep,
) -> OrderService:
    return OrderService(order_repo, product_repo, user_repo)


async def get_auth_service(
    user_repo: UserRepositoryDep,
) -> AuthService:
    return AuthService(user_repo)


# Service Dependencies

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]



# Auth & User Dependencies

async def get_access_payload(request: Request) -> TokenPayload:
    token: str | None = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()
    else:
        token = request.cookies.get(settings.JWT_ACCESS_COOKIE_NAME)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing",
        )

    payload_dict = decode_token(token)
    try:
        return TokenPayload(**payload_dict)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )


TokenPayloadDep = Annotated[TokenPayload, Depends(get_access_payload)]


async def get_refresh_payload(request: Request) -> TokenPayload:

    token = request.cookies.get(settings.JWT_REFRESH_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    payload_dict = decode_token(token)
    try:
        return TokenPayload(**payload_dict)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired or invalid",
        )


RefreshPayloadDep = Annotated[TokenPayload, Depends(get_refresh_payload)]




async def get_current_user(
    payload: TokenPayloadDep,
    user_service: UserServiceDep,
) -> UserResponse:
    
    if not payload.sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: no subject",
        )

    user = await user_service.get_user_by_id(str(payload.sub))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return UserResponse(**user)


CurrentUserDep = Annotated[UserResponse, Depends(get_current_user)]




async def require_admin(current_user: CurrentUserDep) -> UserResponse:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Admins only",
        )
    return current_user


AdminDep = Annotated[UserResponse, Depends(require_admin)]


async def require_authenticated(current_user: CurrentUserDep) -> UserResponse:
    return current_user


AuthUserDep = Annotated[UserResponse, Depends(require_authenticated)]