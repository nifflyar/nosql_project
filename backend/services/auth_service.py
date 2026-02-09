from fastapi import HTTPException, status, Response

from argon2.exceptions import VerifyMismatchError

from models.user import UserLogin
from core.security import create_access_token, create_refresh_token, decode_token
from core.config import settings
from repositories.user_repo import UserRepository
from utils.redis import get_redis
from core.security import create_access_token, create_refresh_token
from utils.password_hasher import verify_password


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login(self, creds: UserLogin, response: Response):
        redis = await get_redis()

        user_obj = await self.user_repo.get_user_by_email(creds.email)

        if user_obj is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        try:

            if not verify_password(creds.password, user_obj["passwordHash"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                )

        except VerifyMismatchError:
            raise HTTPException(status_code=401, detail="Incorrect email or password")


        payload = {
            "sub": str(user_obj["_id"]),
            "role": user_obj["role"],
        }

        access_token = create_access_token(payload,
                                           expires_delta=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS)
        refresh_token = create_refresh_token(payload,
                                             expires_delta=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS)


        await redis.setex(
            f"user:{str(user_obj['_id'])}:refresh",
            settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
            refresh_token,
        )

        response.set_cookie(
            key=settings.JWT_ACCESS_COOKIE_NAME,
            value=access_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite="lax",
            max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
        )

        response.set_cookie(
            key=settings.JWT_REFRESH_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite="lax",
            max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
        )


    async def refresh(self, refresh_token: str, response: Response):
        
        redis = await get_redis()

        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        saved_token = await redis.get(f"user:{user_id}:refresh")
        if isinstance(saved_token, bytes):
            saved_token = saved_token.decode("utf-8")

        if saved_token != refresh_token:
            raise HTTPException(status_code=401, detail="Token revoked")

        new_payload = {"sub": user_id, "role": role}
        new_access = create_access_token(new_payload,
                                         expires_delta=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS)
        new_refresh = create_refresh_token(new_payload,
                                           expires_delta=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS)

        await redis.setex(
            f"user:{user_id}:refresh",
            settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
            new_refresh,
        )

        response.set_cookie(
            key=settings.JWT_ACCESS_COOKIE_NAME,
            value=new_access,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite="lax",
            max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
        )

        response.set_cookie(
            key=settings.JWT_REFRESH_COOKIE_NAME,
            value=new_refresh,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite="lax",
            max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
        )


    async def logout(self, response: Response, user_id: str):
        
        redis = await get_redis()

        response.delete_cookie(
            key=settings.JWT_ACCESS_COOKIE_NAME,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite="lax",
        )
        response.delete_cookie(
            key=settings.JWT_REFRESH_COOKIE_NAME,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite="lax",
        )

        await redis.delete(f"user:{user_id}:refresh")