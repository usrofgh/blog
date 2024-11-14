from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dao.like_dao import LikeDAO
from src.back.models.likes import LikeModel, ResourceType
from src.back.schemas.like_schemas import LikeDBCreateSchema


class LikeService:

    @classmethod
    async def create_reaction(
            cls,
            db: AS,
            resource_type: ResourceType,
            resource_id: int,
            is_like: Literal[True, False, None],
            author_id: int
    ) -> LikeModel:
        req_data = {"author_id": author_id, "resource_id": resource_id, "resource_type": resource_type}
        db_like = await LikeDAO.read_record(db, **req_data)
        req_data["is_like"] = is_like
        like_data = LikeDBCreateSchema(**req_data)

        if db_like:
            if db_like.is_like is is_like:
                like_data.is_like = None
            return await LikeDAO.change_like(db=db, db_like=db_like, like_data=like_data)
        else:
            return await LikeDAO.add_reaction(db=db, like_data=like_data)

    @classmethod
    async def read_reactions(cls, db: AS, resource_type: ResourceType)  -> list[LikeModel]:
        return await LikeDAO._read_many(db=db, resource_type=resource_type)

    @classmethod
    async def read_reactions_by_post_id(cls, db: AS, post_id: int)  -> list[LikeModel]:
        return await LikeDAO.read_reactions_by_post_id(db=db, post_id=post_id)

    @classmethod
    async def read_reactions_by_author_id(cls, db: AS, author_id: int)  -> list[LikeModel]:
        return await LikeDAO.read_reactions_by_author_id(db=db, author_id=author_id)
