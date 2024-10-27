from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import config


class BaseModel(DeclarativeBase):
    pass


DB_PARAMS = {}
if config.MODE == "TEST":
    DB_PARAMS["poolclass"] = NullPool  # To use a new connection every time

engine = create_async_engine(config.PSQL_URI, **DB_PARAMS)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
