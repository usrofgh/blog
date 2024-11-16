from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
from src.back.dao.history.connection_history_dao import ConnectionHistoryDAO
from src.back.models.connections import ConnectionModel
from src.database import get_db


@event.listens_for(AsyncSession, "after_update")
async def commit_connection_changes(mapper, connection, db_conn: ConnectionModel):
    async with next(get_db()) as db:
        await ConnectionHistoryDAO.commit_change(
            db=db,
            connection_id=db_conn.id,
            status=db_conn.status,
        )
