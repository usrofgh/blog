from typing import Annotated

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession as AS, AsyncSession

from exceptions.auth_exceptions import AuthException, IncorrectCredsException
from exceptions.user_exceptions import UserForbiddenException
from models.comments import CommentModel
from models.posts import PostModel
from models.users import UserModel, UserStatus
from repositories.auth_repository import AuthRepository
from repositories.comment_repository import CommentRepository
from repositories.connection_repository import ConnectionRepository
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.comment_service import CommentService
from services.connection_service import ConnectionService
from services.like_service import LikeService
from services.post_service import PostService
from services.user_service import UserService
from config import config
from database import get_db




def get_connection_service():
    return ConnectionService(ConnectionRepository())

def get_post_service():
    return PostService(PostRepository())

def get_comment_service():
    return CommentService(CommentRepository())

def get_like_service():
    return CommentService(CommentRepository())

def get_auth_service():
    return AuthService(AuthRepository())

def get_user_service():
    return UserService(UserRepository())


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

    db_user = await UserRepository.find_one(db=db, id=user_id)
    if not db_user:
        raise UserForbiddenException
    if db_user.status is UserStatus.DELETED:
        raise IncorrectCredsException
    return db_user


SessionObj = Annotated[AsyncSession, Depends(get_db)]
CurrUserObj = Annotated[UserModel, Depends(get_current_user)]

UserServiceObj = Annotated[UserService, Depends(get_user_service)]
ConnServiceObj = Annotated[ConnectionService, Depends(get_connection_service)]
PostServiceObj = Annotated[PostService, Depends(get_post_service)]
AuthServiceObj = Annotated[AuthService, Depends(get_auth_service)]
CommentServiceObj = Annotated[CommentService, Depends(get_comment_service)]
LikeServiceObj = Annotated[LikeService, Depends(get_like_service)]



async def get_admin_user(user_db: CurrUserObj) -> UserModel:
    if user_db.is_admin is False:
        raise UserForbiddenException
    return user_db


async def get_user_by_id(
        db: SessionObj,
        user_service: UserServiceObj,
        user_id: int,
) -> UserModel:
    return await user_service.get_user(db=db, id=user_id)


async def get_curr_post(
        db: SessionObj,
        post_service: PostServiceObj,
        post_id: int,
) -> PostModel:
    return await post_service.get_post_by_id(db=db, id=post_id)


async def get_curr_comment(
        db: SessionObj,
        comment_service: CommentServiceObj,
        comment_id: int,
        post: PostModel = Depends(get_curr_post),
) -> CommentModel:
    return await comment_service.get_comment_by_id(db=db, id=comment_id)
