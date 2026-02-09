from fastapi import APIRouter, Request, Response, HTTPException, status

from models.user import UserCreate, UserLogin, UserResponse
from dependencies.dependency_injection import (
    CurrentUserDep,
    UserServiceDep,
    AuthServiceDep,
)
from core.config import settings 




router = APIRouter(prefix="/auth", tags=["Authentication"])




@router.post("/register", description="Register new user")
async def user_register(
    user: UserCreate,
    user_service: UserServiceDep,
):
    await user_service.create_user(user_data=user)
    return {"msg": "User registered successfully"}




@router.post("/login", description="Login into account")
async def user_login(
    user: UserLogin,
    response: Response,
    auth_service: AuthServiceDep,
):
    await auth_service.login(creds=user, response=response)
    return {"msg": "Login successful"}




@router.post("/refresh", description="Refresh the token")
async def user_token_refresh(
    auth_service: AuthServiceDep,
    response: Response,
    request: Request,
):
    refresh_from_cookie = request.cookies.get(settings.JWT_REFRESH_COOKIE_NAME)
    if not refresh_from_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token cookie missing",
        )

    await auth_service.refresh(refresh_token=refresh_from_cookie, response=response)
    return {"msg": "Token refreshed successfully"}





@router.post("/logout", description="Logout from account")
async def user_logout(
    current_user: CurrentUserDep,
    auth_service:  AuthServiceDep,
    response: Response,
):
    await auth_service.logout(response=response, user_id=str(current_user.id))
    return {"msg": "Logged out successfully"}





@router.get(
    "/me",
    description="Get current user info",
    response_model=UserResponse,
)
async def get_current_user_info(
    current_user: CurrentUserDep,
):
    return current_user
