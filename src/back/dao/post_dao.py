from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dao.base_dao import BaseDAO
from src.back.models.posts import PostModel
from src.back.schemas.post_schemas import PostCreateDBSchema, PostEditSchema


class PostDAO(BaseDAO):
    MODEL = PostModel

    @classmethod
    async def create_post(cls, db: AS, post_data: PostCreateDBSchema) -> MODEL:
        return await cls._create(db, post_data)

    @classmethod
    async def read_post_by_id(cls, db: AS, id: int) -> MODEL:
        return await cls._read_by_id(db, id)

    @classmethod
    async def read_posts_by_author_id(cls, db: AS, author_id: int) -> list[MODEL]:
        return await cls._read_many(db, author_id=author_id)

    @classmethod
    async def read_posts(cls, db: AS, **filters: Any) -> list[MODEL]:
        return await cls._read_many(db, **filters)

    @classmethod
    async def update_post(cls, db: AS, db_obj: MODEL, obj_in: PostEditSchema) -> MODEL:
        return await cls._update(db, db_obj, obj_in)

    @classmethod
    async def delete_post(cls, db: AS, db_obj: MODEL) -> None:
        await cls._delete(db, db_obj)
