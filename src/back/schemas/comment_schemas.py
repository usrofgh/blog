from datetime import datetime

from pydantic import BaseModel, Field


class CommentCreateSchema(BaseModel):
    content: str = Field(min_length=1, max_length=500)
    post_id: int
    parent_comment_id: int | None = None


class CommentCreateDBSchema(BaseModel):
    content: str = Field(min_length=1, max_length=500)
    post_id: int
    author_id: int
    is_blocked: bool
    parent_comment_id: int | None


class CommentReadSchema(BaseModel):
    id: int
    content: str
    author_id: int
    post_id: int
    parent_comment_id: int | None
    created_at: datetime
    updated_at: datetime


class CommentEditSchema(BaseModel):
    id: int
    content: str = Field(min_length=1, max_length=500)
