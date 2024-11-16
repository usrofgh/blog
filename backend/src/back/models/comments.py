from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import BaseModel


class CommentModel(BaseModel):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]

    parent_comment_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id"), nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    is_blocked: Mapped[bool]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    replies: Mapped["CommentModel"] = relationship("CommentModel", back_populates="parent_comment")
    parent_comment: Mapped["CommentModel"] = relationship("CommentModel", remote_side=[id], back_populates="replies")
    author: Mapped["UserModel"] = relationship("UserModel", back_populates="comments")
    post: Mapped["PostModel"] = relationship("PostModel", back_populates="comments")

    def __repr__(self) -> str:
        return (
            f"<CommentModel(id={self.id}, content={self.content[:15]}..., author_id={self.author_id}, post_id={self.post_id})>"
        )


# https://ru.stackoverflow.com/questions/1593274/sqlalchemy-relationship-с-моделями-в-отдельных-файлах
# Fixing of the error - "sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[UserModel(users)]
from back.models.posts import PostModel  # noqa E402
from back.models.users import UserModel  # noqa E402
