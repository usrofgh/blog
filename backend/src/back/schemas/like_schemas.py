from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from back.models.likes import ResourceType


class LikeBaseSchema(BaseModel):
    is_like: Literal[True, False, None] = Field(..., description="True for like, False for dislike")

class LikeDBCreateSchema(LikeBaseSchema):
    author_id: int
    resource_id: int
    resource_type: ResourceType


class LikeReadSchema(LikeBaseSchema):
    author_id: int
    created_at: datetime
