from datetime import datetime

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str | None] = mapped_column(unique=True)
    password: Mapped[str]

    auto_reply: Mapped[bool] = mapped_column(default=False)
    auto_reply_sec_delay: Mapped[int] = mapped_column(default=30)

    is_activated: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    activation_code: Mapped[str | None] = mapped_column(unique=True)
    registered_at: Mapped[datetime] = mapped_column(server_default=func.now())

    posts: Mapped[list["PostModel"]] = relationship("PostModel", back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[list["CommentModel"]] = relationship("CommentModel", back_populates="author", cascade="all, delete-orphan")
    auth_token: Mapped["AuthTokenModel"] = relationship("AuthTokenModel", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_users_email", "email"),
    )

    def __repr__(self) -> str:
        return self.email


from src.back.models.comments import CommentModel  # noqa E402
# https://ru.stackoverflow.com/questions/1593274/sqlalchemy-relationship-с-моделями-в-отдельных-файлах
# Fixing of the error - "sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[UserModel(users)]
from src.back.models.posts import PostModel  # noqa E402
from src.back.models.auth_tokens import AuthTokenModel   # noqa E402
