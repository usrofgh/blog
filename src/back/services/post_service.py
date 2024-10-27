from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dao.post_dao import PostDAO
from src.back.exceptions.base_exception import SwearWordException
from src.back.exceptions.post_exceptions import PostNotFoundException
from src.back.exceptions.user_exceptions import UserForbiddenException
from src.back.models.posts import PostModel
from src.back.models.users import UserModel
from src.back.schemas.post_schemas import PostCreateDBSchema, PostCreateSchema, PostFilterDBSchema, PostFilterSchema
from src.managers.openai_manager import openai_manager


class PostService:

    @staticmethod
    async def create_post(db: AS, post_data: PostCreateSchema, curr_user: UserModel) -> PostModel:
        swear_words = bool(openai_manager.detect_swear_words(post_data.content))
        data = {
            "content": post_data.content,
            "author_id": curr_user.id,
            "is_blocked": True if swear_words else False
        }
        post_data = PostCreateDBSchema(**data)
        db_post = await PostDAO.create_post(db=db, post_data=post_data)
        if swear_words:
            raise SwearWordException
        else:
            return db_post

    @staticmethod
    async def read_post_by_id(db: AS, id: int) -> PostModel:
        db_post = await PostDAO.read_post_by_id(db=db, id=id)
        if not db_post or db_post.is_blocked:
            raise PostNotFoundException
        return db_post

    @staticmethod
    async def read_posts(db: AS, filters: PostFilterSchema) -> list[PostModel]:
        filters = PostFilterDBSchema(**filters.model_dump(), is_blocked=False).model_dump(exclude_none=True)
        return await PostDAO.read_posts(db=db, **filters)

    @staticmethod
    async def delete_post(db: AS, id: int, curr_user: UserModel) -> None:
        db_post = await PostDAO.read_post_by_id(db=db, id=id)
        if not db_post or db_post.is_blocked:
            raise PostNotFoundException

        if curr_user.id != db_post.author_id and curr_user.is_admin is False:
            raise UserForbiddenException

        await PostDAO.delete_post(db=db, db_obj=db_post)
