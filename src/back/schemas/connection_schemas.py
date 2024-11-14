from datetime import datetime

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from src.back.exceptions.connection_exceptions import ConnectionYourselfException
from src.back.models.connections import Status


class ConnectionReadSchema(BaseModel):
    id: int
    follower_id: int
    followed_id: int
    status: Status
    requested_at: datetime


class ConnectionCreateSchema(BaseModel):
    follower_id: int
    followed_id: int

    @field_validator("follower_id")
    def validate_follow(cls, follower_id: int, info: FieldValidationInfo) -> int:
        if "followed_id" in info.data and follower_id != info.data["followed_id"]:
            raise ConnectionYourselfException
        return follower_id

class ConnectionChangeStatusSchema(ConnectionCreateSchema):
    status: Status
