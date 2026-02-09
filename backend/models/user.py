from pydantic import ConfigDict, EmailStr, Field
from datetime import datetime
from enum import Enum

from models.base import BaseModelConfig, PyObjectId


class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"



class UserCreate(BaseModelConfig):
    name: str
    email: EmailStr
    password: str
    address: str


class UserResponse(BaseModelConfig):
    id: PyObjectId = Field(alias="_id")
    name: str
    email: EmailStr
    role: UserRole
    address: str
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True 
    )


class UserLogin(BaseModelConfig):
    email: EmailStr
    password: str
