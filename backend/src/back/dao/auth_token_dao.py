from sqlalchemy.ext.asyncio import AsyncSession as AS

from back.dao.base_dao import BaseDAO
from back.models.auth_tokens import AuthTokenModel
from back.schemas.auth_schemas import RefreshTokenCreateSchema


class AuthTokenDAO(BaseDAO):
    MODEL = AuthTokenModel

    @classmethod
    async def read_by_user_id(cls, user_id: int, db: AS) -> MODEL:
        return await cls._read_by(db=db, user_id=user_id)

    @classmethod
    async def create_token(cls, obj_in: RefreshTokenCreateSchema, db: AS) -> MODEL:
        return await cls._create(db=db, obj_in=obj_in)

    @classmethod
    async def read_by_token(cls, token: str, db: AS) -> MODEL:
        return await cls._read_by(db=db, refresh_token=token)

    @classmethod
    async def delete_token_by_user_id(cls, user_id: int, db: AS) -> None:
        db_token = await cls.read_by_user_id(user_id=user_id, db=db)
        if db_token:
            await cls._delete(db=db, db_obj=db_token)
