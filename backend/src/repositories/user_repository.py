from models.users import UserModel, UserStatus
from repositories.abstract_repository import SQLRepository
from sqlalchemy.ext.asyncio import AsyncSession as AS


class UserRepository(SQLRepository):
    MODEL = UserModel

    @classmethod
    async def soft_delete(cls, db: AS, db_obj: MODEL) -> None:
        delete_marker = "__deleted_8f6fd171c125a9506502440"
        db_obj.email = db_obj.email + delete_marker
        db_obj.username = db_obj.username + delete_marker
        db_obj.status = UserStatus.DELETED
        await db.commit()
