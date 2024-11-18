from models.comments import CommentModel, CommentStatus
from repositories.abstract_repository import SQLRepository
from sqlalchemy.ext.asyncio import AsyncSession as AS


class CommentRepository(SQLRepository):
    MODEL = CommentModel

    @classmethod
    async def soft_delete(cls, db: AS, db_obj: MODEL) -> None:
        db_obj.status = CommentStatus.DELETED
        await db.commit()
