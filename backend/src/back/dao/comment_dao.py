from sqlalchemy.ext.asyncio import AsyncSession as AS

from back.dao.base_dao import BaseDAO
from back.models.comments import CommentModel
from back.schemas.comment_schemas import CommentCreateDBSchema, CommentEditSchema


class CommentDAO(BaseDAO):
    MODEL = CommentModel

    @classmethod
    async def create_comment(cls, db: AS, comment_data: CommentCreateDBSchema) -> MODEL:
        return await cls._create(db, comment_data)

    @classmethod
    async def read_comment_by_id(cls, db: AS, id: int) -> MODEL:
        return await cls._read_by_id(db, id)

    @classmethod
    async def read_comments_by_author_id(cls, db: AS, author_id: int) -> list[MODEL]:
        return await cls._read_many(db, author_id=author_id)

    @classmethod
    async def read_comments(cls, db: AS, **filters) -> list[MODEL]:
        return await cls._read_many(db=db, **filters)

    @classmethod
    async def update_comment(cls, db: AS, db_obj: MODEL, obj_in: CommentEditSchema) -> MODEL:
        return await cls._update(db, db_obj, obj_in)

    @classmethod
    async def delete_comment(cls, db: AS, db_obj: MODEL) -> None:
        await cls._delete(db, db_obj)
