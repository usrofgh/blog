from datetime import datetime
from enum import StrEnum, auto

from sqlalchemy import ForeignKey, func, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from database import BaseModel


class ResourceType(StrEnum):
    POST = auto()
    COMMENT = auto()
    PHOTO = auto()
    VIDEO = auto()


class LikeModel(BaseModel):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    resource_type: Mapped[ResourceType] = mapped_column(Enum(ResourceType))
    resource_id: Mapped[int]
    is_like: Mapped[bool | None]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint("author_id", "resource_id", "resource_type", name="unique_like_uc"),
    )


# https://ru.stackoverflow.com/questions/1593274/sqlalchemy-relationship-с-моделями-в-отдельных-файлах
# Fixing of the error - "sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[UserModel(users)]
from back.models.users import UserModel  # noqa E402
