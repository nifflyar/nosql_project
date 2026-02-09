from pydantic import Field
from typing import List
from datetime import datetime
from models.base import BaseModelConfig, PyObjectId




class ProductVariant(BaseModelConfig):
    stock: int
    size: str
    color: str


class ProductCreate(BaseModelConfig):
    name: str
    description: str
    image_url: str
    price: float
    category_id: PyObjectId
    variants: List[ProductVariant]

    

class ProductResponse(BaseModelConfig):
    id: PyObjectId = Field(alias="_id")
    name: str
    price: float
    category_id: PyObjectId
    image_url: str
    variants: List[ProductVariant]
    created_at: datetime

