from pydantic import BaseModel, Field
from datetime import datetime


from models.base import BaseModelConfig, PyObjectId



class CategoryCreate(BaseModel):
    name: str
    description: str



class CategoryResponse(BaseModelConfig):
    id: PyObjectId = Field(alias="_id")
    name: str
    description: str
    created_at: datetime

