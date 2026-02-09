from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_URL: str
    DB_NAME: str

    JWT_SECRET_KEY: str
    ALGORITHM: str
    JWT_ACCESS_COOKIE_NAME: str
    JWT_REFRESH_COOKIE_NAME: str
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS: int
    COOKIE_SECURE: bool
    
    REDIS_URL_DOCKER: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore
