from sqlalchemy.ext.asyncio import AsyncSession as AS

from exceptions.base_exception import SwearWordException
from exceptions.post_exceptions import PostNotFoundException
from exceptions.user_exceptions import UserForbiddenException
from models.posts import PostModel
from models.users import UserModel
from repositories.post_repository import PostRepository
from schemas.post_schemas import PostCreateDBSchema, PostCreateSchema, PostFilterDBSchema, PostFilterSchema
from managers.openai_manager import openai_manager


class PostService:
    def __init__(self, post_repository: PostRepository):
        self._post_repos = post_repository

    async def create_post(self, db: AS, post_data: PostCreateSchema, curr_user: UserModel) -> PostModel:
        swear_words = bool(openai_manager.detect_swear_words(post_data.content))
        data = {
            "content": post_data.content,
            "author_id": curr_user.id,
            "is_blocked": True if swear_words else False
        }
        post_data = PostCreateDBSchema(**data)
        db_post = await self._post_repos.add_one(db=db, schema=post_data)
        if swear_words:
            raise SwearWordException
        else:
            return db_post

    async def get_post_by_id(self, db: AS, id: int) -> PostModel:
        db_post: PostModel = await self._post_repos.find_one(db=db, id=id)
        if not db_post or db_post.is_blocked or db_post.status is db_post.status.DELETED:
            raise PostNotFoundException
        return db_post

    async def get_posts(self, db: AS, filters: PostFilterSchema) -> list[PostModel]:
        filters = PostFilterDBSchema(**filters.model_dump(), is_blocked=False).model_dump(exclude_none=True)
        db_posts =  await self._post_repos.find_all(db=db, **filters)
        return [post for post in db_posts if post.status is post.status.ACTIVE]

    async def soft_delete(self, db: AS, id: int, curr_user: UserModel) -> None:
        db_post = await self._post_repos.find_one(db=db, id=id)
        if not db_post or db_post.is_blocked or db_post.status is db_post.status.DELETED:
            raise PostNotFoundException

        if curr_user.id != db_post.author_id and curr_user.is_admin is False:
            raise UserForbiddenException

        await self._post_repos.soft_delete(db=db, db_obj=db_post)
