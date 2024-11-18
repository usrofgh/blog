from repositories.abstract_repository import AbstractRepository
from models.connections import Status
from models.history.connection_history import ConnectionHistoryModel
from schemas.connection_history_schemas import ConnectionHistorySchema
from sqlalchemy.ext.asyncio import AsyncSession as AS


class ConnectionHistoryDAO(AbstractRepository):
    MODEL = ConnectionHistoryModel

    @classmethod
    async def commit_change(cls, db: AS, connection_id: int, status: Status) -> MODEL:
        schema = ConnectionHistorySchema(connection_id=connection_id, status=status)
        return await cls.add_one(db=db, schema=schema)
