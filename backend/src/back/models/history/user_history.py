from datetime import datetime
from enum import StrEnum, auto

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from database import BaseModel


class UserHistoryField(StrEnum):
    EMAIL = auto()
    PASSWORD = auto()
    AUTO_REPLY = auto()
    AUTO_REPLY_SEC_DELAY = auto()
    STATUS = auto()
    EMAIL_VERIFIED = auto()
    IS_ADMIN = auto()


class UserHistoryModel(BaseModel):
    __tablename__ = "users_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    field_name: Mapped["UserHistoryField"]
    old_value: Mapped[str]
    new_value: Mapped[str]

    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
