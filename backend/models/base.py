
from typing import Any
from bson import ObjectId
from pydantic import AfterValidator, BaseModel, ConfigDict, PlainSerializer, WithJsonSchema
from typing_extensions import Annotated





def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if not ObjectId.is_valid(v):
        raise ValueError("Invalid ObjectId format")
    return ObjectId(v)



PyObjectId = Annotated[
    str | ObjectId,
    AfterValidator(validate_object_id),
    PlainSerializer(lambda v: str(v), return_type=str),
    WithJsonSchema({"type": "string"}, mode="shard"),
]


class BaseModelConfig(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True 
    )