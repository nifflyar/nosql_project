from bson import ObjectId
from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime
from enum import Enum

from models.base import BaseModelConfig, PyObjectId






class OrderStatus(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class QuantityUpdate(BaseModel):
    quantity: int


class OrderItemVariant(BaseModelConfig):
    size: str
    color: str



class OrderItem(BaseModelConfig):
    product_id: PyObjectId
    name: str
    price: float
    quantity: int
    variant: OrderItemVariant

    

class OrderCreate(BaseModelConfig):
    items: List[OrderItem]



class OrderResponse(BaseModelConfig):
    id: PyObjectId = Field(alias="_id")
    user_id: PyObjectId
    status: OrderStatus = OrderStatus.PENDING
    total: float
    items: List[OrderItem]
    created_at: datetime

    @field_validator("id", "user_id", mode="before")
    @classmethod
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
