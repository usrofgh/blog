from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import BaseModel


class PostModel(BaseModel):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_blocked: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    comments: Mapped[list["CommentModel"]] = relationship("CommentModel", back_populates="post")
    author: Mapped["UserModel"] = relationship("UserModel", back_populates="posts")

    def __repr__(self) -> str:
        return f"<PostModel(id={self.id}, content={self.content[:15]}..., author_id={self.author_id}, post_id={self.id})>"


# https://ru.stackoverflow.com/questions/1593274/sqlalchemy-relationship-с-моделями-в-отдельных-файлах
# Fixing of the error - "sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[UserModel(users)]
from back.models.comments import CommentModel  # noqa E402
from back.models.users import UserModel  # noqa E402
