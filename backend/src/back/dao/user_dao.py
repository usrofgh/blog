from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession as AS

from back.dao.auth_token_dao import AuthTokenDAO
from back.dao.base_dao import BaseDAO
from back.models.users import UserModel, UserStatus
from back.schemas.user_schemas import UserCreateDBSchema


class UserDAO(BaseDAO):
    MODEL = UserModel

    @classmethod
    async def create_user(cls, db: AS, user_data: UserCreateDBSchema) -> MODEL:
        return await cls._create(db, user_data)

    @classmethod
    async def read_user_by_id(cls, db: AS, id: int) -> MODEL:
        return await cls._read_by_id(db, id)

    @classmethod
    async def read_user_by_username(cls, db: AS, username: str) -> MODEL:
        return await cls._read_by(db, username=username)

    @classmethod
    async def read_user_by_email(cls, db: AS, email: str) -> MODEL:
        return await cls._read_by(db, email=email)

    @classmethod
    async def read_user_by_act_code(cls, db: AS, activation_code: str) -> MODEL:
        return await cls._read_by(db, activation_code=activation_code)

    @classmethod
    async def read_users(cls, db: AS, **filters: Any) -> list[MODEL]:
        return await cls._read_many(db, **filters)

    @classmethod
    async def delete_user(cls, db: AS, db_obj: MODEL) -> None:
        delete_marker = "__deleted_8f6fd171c125a9506502440"
        db_obj.email = db_obj.email + delete_marker
        db_obj.username = db_obj.username + delete_marker
        db_obj.status = UserStatus.DELETED
        await db.commit()

        await AuthTokenDAO.delete_token_by_user_id(db_obj.id, db)
