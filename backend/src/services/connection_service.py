from sqlalchemy.ext.asyncio import AsyncSession as AS

from exceptions.connection_exceptions import ConnectionYourselfException, ConnectionNotExistException, \
    ConnectionFailedException
from models.connections import ConnectionModel, Status
from repositories.connection_repository import ConnectionRepository
from schemas.connection_schemas import ConnectionCreateSchema


class ConnectionService:
    def __init__(self, conn_repos: ConnectionRepository):
        self._conn_repos = conn_repos

    async def create_connection(
            self,
            db: AS,
            follower_id: int,
            followed_id: int
    ) -> ConnectionModel:
        if follower_id == followed_id:
            raise ConnectionYourselfException

        db_conn: ConnectionModel = await self._conn_repos.find_one(db, follower_id=follower_id, followed_id=followed_id)
        if db_conn and db_conn.status in [Status.CANCELLED, Status.REJECTED]:
            db_conn.status = Status.PENDING
            await db.commit()
            return db_conn

        if db_conn:
            return db_conn

        conn_schema = ConnectionCreateSchema(follower_id=follower_id, followed_id=followed_id)
        db_conn = await self._conn_repos.add_one(db=db, schema=conn_schema)
        return db_conn


    async def unfollow(self, db: AS, follower_id: int, followed_id: int) -> ConnectionModel:
        db_conn: ConnectionModel = await self._conn_repos.find_one(db, follower_id=follower_id, followed_id=followed_id)

        if not db_conn:
            raise ConnectionNotExistException

        if db_conn.status in [Status.CANCELLED.value, Status.REJECTED.value]:
            raise ConnectionFailedException

        if db_conn.status in [Status.ACCEPTED.value, Status.PENDING.value]:
            db_conn.status = Status.CANCELLED
            await db.commit()
            return db_conn

    async def accept_or_reject_request(self, db: AS, follower_id: int, followed_id: int, status: Status) -> ConnectionModel:
        db_conn: ConnectionModel = await self._conn_repos.find_one(db, follower_id=follower_id, followed_id=followed_id)

        if not db_conn:
            raise ConnectionNotExistException

        if (
                (db_conn.status is Status.PENDING and status in [Status.ACCEPTED, Status.REJECTED]) or
                (db_conn.status is Status.ACCEPTED and status == Status.REJECTED.value)
        ):
            db_conn.status = status
            await db.commit()
            return db_conn

        raise ConnectionFailedException

    async def get_followers(self, db: AS, follower_id: int) -> list[int]:
        db_connections = await self._conn_repos.find_all(db=db, followed_id=follower_id, status=Status.ACCEPTED.value)
        print(db_connections)
        return [conn.follower_id for conn in db_connections]

    async def get_following(self, db: AS, follower_id: int) -> list[int]:
        db_connections = await self._conn_repos.find_all(db=db, follower_id=follower_id, status=Status.ACCEPTED.value)
        return [conn.followed_id for conn in db_connections]
