from back.dao.base_dao import BaseDAO
from back.models.connections import ConnectionModel
from sqlalchemy.ext.asyncio import AsyncSession as AS

from back.schemas.connection_schemas import ConnectionCreateSchema, ConnectionChangeStatusSchema


class ConnectionDAO(BaseDAO):
    MODEL = ConnectionModel

    @classmethod
    async def create_connection(cls, db: AS, connection_data: ConnectionCreateSchema) -> ConnectionModel:
        return await cls._create(db=db, obj_in=connection_data)

    @classmethod
    async def delete_connection(cls, db: AS, connection_data: ConnectionModel) -> None:
        return await cls._delete(db=db, db_obj=connection_data)

    @classmethod
    async def read_connection(cls, db: AS, follower_id: int, followed_id: int) -> ConnectionModel:
        return await cls._read_by(db=db, follower_id=follower_id, followed_id=followed_id)

    @classmethod
    async def read_connections(cls, db: AS, **filters) -> list[ConnectionModel]:
        return await cls._read_many(db=db, **filters)

    @classmethod
    async def change_connection_status(
            cls,
            db: AS,
            db_connection: ConnectionModel,
            connection_data: ConnectionChangeStatusSchema
    ) -> ConnectionModel:
        return await cls._update(db=db, db_obj=db_connection, obj_in=connection_data)
