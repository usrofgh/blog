import datetime

from arq import create_pool
from sqlalchemy.ext.asyncio import AsyncSession as AS
from tenacity import RetryError

from repositories.comment_repository import CommentRepository
from exceptions.base_exception import NetworkErrorException, SwearWordException
from exceptions.comment_exceptions import (
    CommentNotFoundException,
    CommentOlderThanOneDayError,
    ParentCommentDoesNotExistException
)
from exceptions.post_exceptions import PostNotFoundException
from exceptions.user_exceptions import UserForbiddenException
from models.comments import CommentModel
from models.users import UserModel
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from schemas.comment_schemas import CommentCreateDBSchema, CommentCreateSchema, CommentEditSchema
from tasks.task_manager import REDIS_SETTINGS, auto_reply
from managers.openai_manager import openai_manager


class CommentService:
    def __init__(self, comment_repository: CommentRepository):
        self._comment_repos = comment_repository

    async def create_comment(self, db: AS, post_id: int, comment_data: CommentCreateSchema, curr_user: UserModel) -> CommentModel:
        db_post = await PostRepository.find_one(db=db, id=post_id)
        if not db_post or db_post.is_blocked:
            raise PostNotFoundException

        if comment_data.parent_comment_id is not None:
            db_parent_comm = await self._comment_repos.find_one(db=db, id=comment_data.parent_comment_id)
            if not db_parent_comm:
                raise ParentCommentDoesNotExistException

        try:
            swear_words = openai_manager.detect_swear_words(comment_data.content)
        except RetryError:
            raise NetworkErrorException

        comment_data = CommentCreateDBSchema(
            **comment_data.model_dump(),
            post_id=post_id,
            author_id=curr_user.id,
            is_blocked=bool(swear_words)
        )
        db_comment = await self._comment_repos.add_one(db=db, schema=comment_data)

        if swear_words:
            raise SwearWordException

        if db_comment.author_id == db_post.author_id:
            return db_comment

        post_author = await UserRepository.find_one(db=db, id=db_post.author_id)

        if post_author.auto_reply:
            kwargs = {
                "post_text": db_post.content,
                "comment_text": db_comment.content,
                "author_id": post_author.id,
                "post_id": db_post.id,
                "parent_comment_id": db_comment.id
            }

            redis = await create_pool(REDIS_SETTINGS)
            await redis.enqueue_job(
                function=auto_reply.__name__,
                _defer_by=datetime.timedelta(seconds=5),
                **kwargs
            )

        return db_comment

    async def get_comment_by_id(self, db: AS, id: int) -> CommentModel:
        db_comment = await self._comment_repos.find_one(db=db, id=id)
        if not db_comment or db_comment.is_blocked:
            raise CommentNotFoundException
        return db_comment


    async def get_comments(self, db: AS, post_id: int) -> list[CommentModel]:
        db_comments = await self._comment_repos.find_all(db=db, post_id=post_id)
        return db_comments

    async def update_comment(self, db: AS, comment_id: int, comment_data: CommentEditSchema, curr_user: UserModel) -> CommentModel:
        db_comment: CommentModel = await self._comment_repos.find_one(db=db, id=comment_id)
        if not db_comment or db_comment.is_blocked:
            raise CommentNotFoundException

        if db_comment.author_id != curr_user.id and curr_user.is_admin is False:
            raise UserForbiddenException

        is_one_day_passed = (datetime.datetime.now() - db_comment.created_at).days > 0
        if is_one_day_passed:
            raise CommentOlderThanOneDayError

        swear_words = openai_manager.detect_swear_words(comment_data.content)
        if bool(swear_words):
            raise SwearWordException

        return await self._comment_repos.update(db=db, db_obj=db_comment, schema=comment_data)

    async def soft_delete(self, db: AS, id: int, curr_user: UserModel) -> None:
        db_comment: CommentModel = await self._comment_repos.find_one(db=db, id=id)
        if not db_comment or db_comment.is_blocked:
            raise CommentNotFoundException

        if curr_user.id != db_comment.author_id and curr_user.is_admin is False:
            raise UserForbiddenException

        await self._comment_repos.soft_delete(db=db, db_obj=db_comment)
