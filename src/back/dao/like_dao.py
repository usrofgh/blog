from src.back.dao.base_dao import BaseDAO
from src.back.models.likes import LikeModel, ResourceType
from src.back.schemas.like_schemas import LikeDBCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession as AS


class LikeDAO(BaseDAO):
    MODEL = LikeModel

    @classmethod
    async def add_reaction(cls, db: AS, like_data: LikeDBCreateSchema) -> LikeModel:
        return await cls._create(db=db, obj_in=like_data)

    @classmethod
    async def change_like(cls, db: AS, db_like: LikeModel, like_data: LikeDBCreateSchema) -> LikeModel:
        return await cls._update(db=db, db_obj=db_like, obj_in=like_data)

    @classmethod
    async def read_record(cls, db: AS, author_id: int, resource_id: int, resource_type: ResourceType) -> LikeModel:
        return await cls._read_by(db=db, author_id=author_id, resource_id=resource_id, resource_type=resource_type)

    @classmethod
    async def read_reactions_by_post_id(cls, db: AS, post_id: int) -> list[LikeModel]:
        return await cls._read_many(db=db, post_id=post_id)

    @classmethod
    async def read_reactions_by_author_id(cls, db: AS, author_id: int) -> list[LikeModel]:
        return await cls._read_many(db=db, author_id=author_id)
