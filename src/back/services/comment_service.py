import datetime

from arq import create_pool
from sqlalchemy.ext.asyncio import AsyncSession as AS
from tenacity import RetryError

from src.back.dao.comment_dao import CommentDAO
from src.back.dao.post_dao import PostDAO
from src.back.dao.user_dao import UserDAO
from src.back.exceptions.base_exception import NetworkErrorException, SwearWordException
from src.back.exceptions.comment_exceptions import CommentNotFoundException, CommentOlderThanOneDayError, \
    ParentCommentDoesNotExistException
from src.back.exceptions.post_exceptions import PostNotFoundException
from src.back.exceptions.user_exceptions import UserForbiddenException
from src.back.models.comments import CommentModel
from src.back.models.users import UserModel
from src.back.schemas.analytic_schemas import CommentFilterSchema
from src.back.schemas.comment_schemas import CommentCreateDBSchema, CommentCreateSchema, CommentEditSchema
from src.back.tasks.task_manager import REDIS_SETTINGS, auto_reply
from src.managers.openai_manager import openai_manager


class CommentService:

    @staticmethod
    async def create_comment(db: AS, post_id: int, comment_data: CommentCreateSchema, curr_user: UserModel) -> CommentModel:
        db_post = await PostDAO.read_post_by_id(db=db, id=post_id)
        if not db_post or db_post.is_blocked:
            raise PostNotFoundException

        if comment_data.parent_comment_id is not None:
            db_parent_comm = await CommentDAO.read_comment_by_id(db=db, id=comment_data.parent_comment_id)
            if not db_parent_comm:
                raise ParentCommentDoesNotExistException()

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
        db_comment = await CommentDAO.create_comment(db=db, comment_data=comment_data)

        if swear_words:
            raise SwearWordException

        if db_comment.author_id == db_post.author_id:
            return db_comment

        post_author = await UserDAO.read_user_by_id(db=db, id=db_post.author_id)

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

    @staticmethod
    async def read_comment_by_id(db: AS, id: int) -> CommentModel:
        db_comment = await CommentDAO.read_comment_by_id(db=db, id=id)
        if not db_comment or db_comment.is_blocked:
            raise CommentNotFoundException
        return db_comment


    @staticmethod
    async def read_comments(db: AS, post_id: int) -> list[CommentModel]:
        db_comments = await CommentDAO.read_comments(db=db, post_id=post_id)
        return db_comments

    @staticmethod
    async def update_comment(db: AS, comment_id: int, comment_data: CommentEditSchema, curr_user: UserModel) -> CommentModel:
        db_comment: CommentModel = await CommentDAO.read_comment_by_id(db=db, id=comment_id)
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

        return await CommentDAO.update_comment(db=db, db_obj=db_comment, obj_in=comment_data)

    @staticmethod
    async def delete_comment(db: AS, id: int, curr_user: UserModel) -> None:
        db_comment: CommentModel = await CommentDAO.read_comment_by_id(db=db, id=id)
        if not db_comment or db_comment.is_blocked:
            raise CommentNotFoundException

        if curr_user.id != db_comment.author_id and curr_user.is_admin is False:
            raise UserForbiddenException

        await CommentDAO.delete_comment(db=db, db_obj=db_comment)
