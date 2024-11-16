from abc import ABC
from typing import Any, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession as AS
from sqlalchemy.future import select

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType")


class BaseDAO(ABC):
    MODEL = None

    @classmethod
    async def _create(cls, db: AS, obj_in: SchemaType) -> MODEL:
        db_obj = cls.MODEL(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @classmethod
    async def _read_by_id(cls, db: AS, id: int) -> MODEL:
        query = select(cls.MODEL).filter_by(id=id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def _read_by(cls, db: AS, **filters: Any) -> MODEL:
        query = select(cls.MODEL).filter_by(**filters)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def _read_many(cls, db: AS,  offset: int = None, limit: int = None, **filters: Any) -> list[MODEL]:
        query = select(cls.MODEL).filter_by(**filters)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await db.execute(query)
        result = result.scalars().all()
        return result

    @classmethod
    async def _update(cls, db: AS, db_obj: MODEL, obj_in: SchemaType) -> MODEL:
        obj_data = obj_in.dict(exclude_unset=True)  # Only update provided fields
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @classmethod
    async def _delete(cls, db: AS, db_obj: MODEL) -> None:
        await db.delete(db_obj)
        await db.commit()
