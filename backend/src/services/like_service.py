from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession as AS

from repositories.like_repository import LikeRepository
from models.likes import LikeModel, ResourceType
from schemas.like_schemas import LikeDBCreateSchema


class LikeService:
    def __init__(self, like_repository: LikeRepository):
        self._like_repos  = like_repository

    async def create_reaction(
            self,
            db: AS,
            resource_type: ResourceType,
            resource_id: int,
            is_like: Literal[True, False, None],
            author_id: int
    ) -> LikeModel:
        req_data = {"author_id": author_id, "resource_id": resource_id, "resource_type": resource_type}
        db_like = await self._like_repos.find_one(db=db, **req_data)
        req_data["is_like"] = is_like
        like_data = LikeDBCreateSchema(**req_data)

        if db_like:
            if db_like.is_like is is_like:
                like_data.is_like = None
            return await self._like_repos.update(db=db, db_obj=db_like, schema=like_data)
        else:
            return await self._like_repos.add_one(db=db, schema=like_data)

    async def get_reactions(self, db: AS, resource_type: ResourceType)  -> list[LikeModel]:
        return await self._like_repos.find_all(db=db, resource_type=resource_type)

    async def get_reactions_by_post_id(self, db: AS, post_id: int)  -> list[LikeModel]:
        return await self._like_repos.find_all(db=db, post_id=post_id)

    async def get_reactions_by_author_id(self, db: AS, author_id: int)  -> list[LikeModel]:
        return await self._like_repos.find_all(db=db, author_id=author_id)
