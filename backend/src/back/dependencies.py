from typing import Annotated

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession as AS

from back.dao.user_dao import UserDAO
from back.exceptions.auth_exceptions import AuthException, IncorrectCredsException
from back.exceptions.user_exceptions import UserForbiddenException, BlockedAccountException
from back.models.comments import CommentModel
from back.models.posts import PostModel
from back.models.users import UserModel, UserStatus
from back.services.auth_service import AuthService
from back.services.comment_service import CommentService
from back.services.post_service import PostService
from back.services.user_service import UserService
from config import config
from database import get_db


async def get_current_user(
        token: Annotated[str, Depends(AuthService.OAUTH2_SCHEME)],
        db: AS = Depends(get_db)
) -> UserModel:
    try:
        payload = jwt.decode(jwt=token, key=config.JWT_ACCESS_KEY.get_secret_value(), algorithms=[config.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthException
    except InvalidTokenError:
        raise IncorrectCredsException

    db_user = await UserDAO.read_user_by_id(db=db, id=user_id)
    if not db_user:
        raise UserForbiddenException
    if db_user.status is UserStatus.SUSPENDED:
        raise BlockedAccountException
    if db_user.status is UserStatus.DELETED:
        raise IncorrectCredsException
    return db_user


async def get_admin_user(
        user_db: UserModel = Depends(get_current_user)
) -> UserModel:
    if user_db.is_admin is False:
        raise UserForbiddenException
    return user_db


async def get_user_by_id(
        user_id: int,
        db: AS = Depends(get_db)
) -> UserModel:
    return await UserService.read_user_by_id(db=db, id=user_id)


async def get_curr_post(
        post_id: int,
        db: AS = Depends(get_db)
) -> PostModel:
    return await PostService.read_post_by_id(db=db, id=post_id)


async def get_curr_comment(
        comment_id: int,
        post: PostModel = Depends(get_curr_post),
        db: AS = Depends(get_db)
) -> CommentModel:
    return await CommentService.read_comment_by_id(db=db, id=comment_id)
