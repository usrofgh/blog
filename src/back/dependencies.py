from typing import Annotated

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dao.user_dao import UserDAO
from src.back.exceptions.auth_exceptions import AuthException, IncorrectCredsException
from src.back.exceptions.user_exceptions import UserForbiddenException
from src.back.models.users import UserModel
from src.back.services.auth_service import AuthService
from src.config import config
from src.database import get_db


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
    return db_user


async def get_admin_user(
    user_db: UserModel = Depends(get_current_user)
) -> UserModel:
    if user_db.is_admin is False:
        raise UserForbiddenException
    return user_db
