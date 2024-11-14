import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from src.back.exceptions.user_exceptions import (
    PasswordMismatchException,
    UsernameSpecialSymbolsException,
    PasswordNotProperException,
    InvalidEmailException
)


class UserCreateSchema(BaseModel):
    email: EmailStr
    username: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=8, max_length=300)
    confirm_password: str = Field(min_length=8, max_length=300)

    @field_validator("confirm_password")
    def validate_password(cls, password: str, info: FieldValidationInfo) -> str:
        if "password" in info.data and password != info.data["password"]:
            raise PasswordMismatchException

        is_upper = False
        is_digit = False
        is_special = False
        special_characters = set("!@#$%^&*(),.?\":{}|<>")

        for ch in password:
            if ch == ch.upper():
                is_upper = True
            if ch.isdigit():
                is_digit = True
            if ch in special_characters:
                is_special = True

        if all([is_upper, is_digit, is_special]):
            return password
        else:
            raise PasswordNotProperException()


    @field_validator("username")
    def validate_username(cls, username: str) -> str:
        if not re.match("^[a-zA-Z0-9_]+$", username):
            raise UsernameSpecialSymbolsException
        return username

    @field_validator("email")
    def validate_email(cls, email: str) -> str:
        if "+" in email:
            raise InvalidEmailException

        dot_count = email.count(".") - 1
        cleaned_email = []

        if not dot_count:
            return email

        for ch in email:
            if ch == "." and dot_count != 0:
                dot_count -= 1
            else:
                cleaned_email.append(ch)
        return "".join(cleaned_email)



class UserCreateDBSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
    activation_code: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserFilterSchema(BaseModel):
    username: str | None = None
    online: bool | None = None
    is_admin: bool | None = None


class UserReadSchema(BaseModel):
    id: int
    username: str
    email: str
    online: bool
    is_admin: bool
    registered_at: datetime


class AutoReplyDelaySchema(BaseModel):
    delay: int = Field(gt=0, le=86_400, default=30)
