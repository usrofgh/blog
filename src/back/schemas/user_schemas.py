from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class _BaseUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchema(_BaseUserSchema):
    pass


class UserCreateDBSchema(_BaseUserSchema):
    activation_code: str


class UserUpdateSchema(_BaseUserSchema):
    pass


class UserLoginSchema(_BaseUserSchema):
    pass


class UserFilterSchema(BaseModel):
    is_activated: bool | None = None
    is_admin: bool | None = None


class UserReadSchema(BaseModel):
    id: int
    email: EmailStr
    is_activated: bool
    is_admin: bool
    registered_at: datetime


class AutoReplyDelaySchema(BaseModel):
    delay: int = Field(ge=0, le=86_400)
