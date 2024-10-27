from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dao.base_dao import BaseDAO
from src.back.models.users import UserModel
from src.back.schemas.user_schemas import UserCreateDBSchema, UserUpdateSchema


class UserDAO(BaseDAO):
    MODEL = UserModel

    @classmethod
    async def create_user(cls, db: AS, user_data: UserCreateDBSchema) -> MODEL:
        return await cls._create(db, user_data)

    @classmethod
    async def read_user_by_id(cls, db: AS, id: int) -> MODEL:
        return await cls._read_by_id(db, id)

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
    async def update_user(cls, db: AS, db_obj: MODEL, obj_in: UserUpdateSchema) -> MODEL:
        return await cls._update(db, db_obj, obj_in)

    @classmethod
    async def delete_user(cls, db: AS, db_obj: MODEL) -> None:
        await cls._delete(db, db_obj)
