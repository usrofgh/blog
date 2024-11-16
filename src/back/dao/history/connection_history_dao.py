from src.back.dao.base_dao import BaseDAO
from src.back.models.connections import Status
from src.back.models.history.connection_history import ConnectionHistoryModel
from src.back.schemas.connection_history_schemas import ConnectionHistorySchema
from sqlalchemy.ext.asyncio import AsyncSession as AS


class ConnectionHistoryDAO(BaseDAO):
    MODEL = ConnectionHistoryModel

    @classmethod
    async def commit_change(cls, db: AS, connection_id: int, status: Status) -> MODEL:
        schema = ConnectionHistorySchema(connection_id=connection_id, status=status)
        return await cls._create(db=db, obj_in=schema)
