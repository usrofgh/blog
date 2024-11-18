from datetime import datetime
from enum import StrEnum, auto

from sqlalchemy import ForeignKey, func, UniqueConstraint, Enum

from database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class Status(StrEnum):
    ACCEPTED = auto()
    REJECTED = auto()
    CANCELLED = auto()
    PENDING = auto()


class ConnectionModel(BaseModel):
    __tablename__ = "connections"

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    followed_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.PENDING)

    requested_at: Mapped[datetime] = mapped_column(server_default=func.now())



    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="_follower_followed_uc"),
    )
