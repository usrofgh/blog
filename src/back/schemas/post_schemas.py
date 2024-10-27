from datetime import datetime

from pydantic import BaseModel, Field


class PostCreateSchema(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


class PostCreateDBSchema(PostCreateSchema):
    author_id: int
    is_blocked: bool = False


class PostCreateResponseSchema(BaseModel):
    id: int
    content: str = Field(min_length=1, max_length=1000)
    author_id: int
    created_at: datetime
    updated_at: datetime


class PostEditSchema(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


class PostFilterSchema(BaseModel):
    author_id: int | None = None


class PostFilterDBSchema(BaseModel):
    author_id: int | None = None
    is_blocked: bool = False


class PostReadSchema(BaseModel):
    id: int
    content: str
    author_id: int
    # comments: list[int]
    created_at: datetime
    updated_at: datetime
