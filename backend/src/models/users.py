from datetime import datetime
from enum import StrEnum, auto

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import BaseModel

class UserStatus(StrEnum):
    ACTIVE = auto()
    DELETED = auto()
    SUSPENDED = auto()

class UserModel (BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    auto_reply: Mapped[bool] = mapped_column(default=False)
    auto_reply_sec_delay: Mapped[int] = mapped_column(default=30)

    status: Mapped["UserStatus"] = mapped_column(default=UserStatus.ACTIVE)
    email_verified: Mapped[bool] = mapped_column(default=False)
    online: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    activation_code: Mapped[str | None] = mapped_column(unique=True)
    registered_at: Mapped[datetime] = mapped_column(server_default=func.now())
    avatar_url: Mapped[str | None]

    posts: Mapped[list["PostModel"]] = relationship("PostModel", back_populates="author")
    comments: Mapped[list["CommentModel"]] = relationship("CommentModel", back_populates="author")
    auth_token: Mapped["AuthTokenModel"] = relationship("AuthTokenModel")

    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_username", "username")
    )

    def __repr__(self) -> str:
        return self.username



# https://ru.stackoverflow.com/questions/1593274/sqlalchemy-relationship-с-моделями-в-отдельных-файлах
# Fixing of the error - "sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[UserModel(users)]
from models.auth_tokens import AuthTokenModel  # noqa E402
from models.comments import CommentModel  # noqa E402
from models.posts import PostModel  # noqa E402
