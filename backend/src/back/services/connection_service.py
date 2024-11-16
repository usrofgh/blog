from sqlalchemy.ext.asyncio import AsyncSession as AS

from back.dao.connection_dao import ConnectionDAO
from back.exceptions.connection_exceptions import ConnectionYourselfException, ConnectionNotExistException, \
    ConnectionFailedException
from back.models.connections import ConnectionModel, Status
from back.schemas.connection_schemas import ConnectionCreateSchema, ConnectionChangeStatusSchema


class ConnectionService:

    @staticmethod
    async def create_connection(db: AS, follower_id: int, followed_id: int) -> ConnectionModel:
        if follower_id == followed_id:
            raise ConnectionYourselfException

        db_conn: ConnectionModel = await ConnectionDAO.read_connection(db, follower_id, followed_id)
        if db_conn and db_conn.status in [Status.CANCELLED, Status.REJECTED]:
            schema = ConnectionChangeStatusSchema(
                follower_id=follower_id,
                followed_id=followed_id,
                status=Status.PENDING
            )
            db_connection = await ConnectionDAO.change_connection_status(db, db_conn, schema)
            # await ConnectionHistoryDAO.commit_change(db, db_connection.id, db_connection.status, follower_id)
            return db_connection


        if db_conn:
            return db_conn

        connection_data = ConnectionCreateSchema(follower_id=follower_id, followed_id=followed_id)
        db_connection = await ConnectionDAO.create_connection(db=db, connection_data=connection_data)
        # await ConnectionHistoryDAO.commit_change(db, db_connection.id, db_connection.status, follower_id)
        return db_connection


    @staticmethod
    async def unfollow(db: AS, follower_id: int, followed_id: int) -> ConnectionModel:
        db_connection: ConnectionModel = await ConnectionDAO.read_connection(db, follower_id, followed_id)
        schema = ConnectionChangeStatusSchema(follower_id=follower_id, followed_id=followed_id, status=Status.CANCELLED)

        if not db_connection:
            raise ConnectionNotExistException

        if db_connection.status in [Status.CANCELLED.value, Status.REJECTED.value]:
            raise ConnectionFailedException

        if db_connection.status in [Status.ACCEPTED.value, Status.PENDING.value]:
            db_connection =  await ConnectionDAO.change_connection_status(db, db_connection, schema)
            # await ConnectionHistoryDAO.commit_change(db, db_connection.id, db_connection.status, follower_id)
            return db_connection

    @staticmethod
    async def accept_or_reject_request(db: AS, follower_id: int, followed_id: int, status: Status) -> ConnectionModel:
        db_connection: ConnectionModel = await ConnectionDAO.read_connection(db, follower_id, followed_id)
        schema = ConnectionChangeStatusSchema(follower_id=follower_id, followed_id=followed_id, status=status)

        if not db_connection:
            raise ConnectionNotExistException

        if (
                (db_connection.status is Status.PENDING and status in [Status.ACCEPTED, Status.REJECTED]) or
                (db_connection.status is Status.ACCEPTED and status == Status.REJECTED.value)
        ):
            db_connection = await ConnectionDAO.change_connection_status(db, db_connection, schema)
            # await ConnectionHistoryDAO.commit_change(db, db_connection.id, db_connection.status, follower_id)
            return db_connection

        raise ConnectionFailedException

    @staticmethod
    async def read_followers(db: AS, follower_id: int) -> list[int]:
        db_connections = await ConnectionDAO.read_connections(db=db, followed_id=follower_id, status=Status.ACCEPTED.value)
        return [conn.follower_id for conn in db_connections]

    @staticmethod
    async def read_following(db: AS, follower_id: int) -> list[int]:
        db_connections = await ConnectionDAO.read_connections(db=db, follower_id=follower_id, status=Status.ACCEPTED.value)
        return [conn.followed_id for conn in db_connections]
