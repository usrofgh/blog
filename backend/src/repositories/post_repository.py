from models.posts import PostModel, PostStatus
from repositories.abstract_repository import SQLRepository
from sqlalchemy.ext.asyncio import AsyncSession as AS


class PostRepository(SQLRepository):
    MODEL = PostModel

    @classmethod
    async def soft_delete(cls, db: AS, db_obj: MODEL) -> None:
        db_obj.status = PostStatus.DELETED
        await db.commit()
