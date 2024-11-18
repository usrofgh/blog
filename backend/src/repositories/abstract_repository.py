from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import select

SchemaType = TypeVar("SchemaType", bound=BaseModel)
DBSession = TypeVar("DBSession")


class AbstractRepository(ABC):
    MODEL = None

    @classmethod
    @abstractmethod
    async def add_one(cls, db: DBSession, schema: SchemaType) -> MODEL:
        ...

    @classmethod
    @abstractmethod
    async def find_one(cls, db: DBSession, **filters) -> MODEL:
        ...

    @classmethod
    @abstractmethod
    async def find_all(cls, db: DBSession, **filters) -> list[MODEL]:
        ...

    @classmethod
    @abstractmethod
    async def update(cls, db: DBSession, db_obj: MODEL, schema: SchemaType) -> MODEL:
        ...

    @classmethod
    @abstractmethod
    async def delete(cls, db: DBSession, db_obj: MODEL) -> None:
        ...


class SQLRepository(AbstractRepository, ABC):
    MODEL = None

    @classmethod
    async def add_one(cls, db: DBSession, schema: SchemaType) -> MODEL:
        db_obj = cls.MODEL(**schema.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @classmethod
    async def find_one(cls, db: DBSession, **filters) -> MODEL:
        stmt = select(cls.MODEL).filter_by(**filters)
        result = await db.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def find_all(cls, db: DBSession, offset: int = None, limit: int = None, **filters) -> list[MODEL]:
        stmt = select(cls.MODEL).filter_by(**filters)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update(cls, db: DBSession, db_obj: MODEL, schema: SchemaType) -> MODEL:
        obj_data = schema.model_dump(exclude_unset=True)  # Only update provided fields
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @classmethod
    async def delete(cls, db: DBSession, db_obj: MODEL) -> None:
        await db.delete(db_obj)
        await db.commit()
