from back.dao.base_dao import BaseDAO
from back.models.messages import MessageModel
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession as AS

class MessageDAO(BaseDAO):
    MODEL = MessageModel

    @classmethod
    async def get_messages_between_users(cls, user_id_1: int, user_id_2: int, db: AS):
        query = select(cls.MODEL).filter(
            or_(
                and_(cls.MODEL.sender_id == user_id_1, cls.MODEL.recipient_id == user_id_2),
                and_(cls.MODEL.sender_id == user_id_2, cls.MODEL.recipient_id == user_id_1)
            )
        ).order_by(cls.MODEL.id)
        result = await db.execute(query)
        return result.scalars().all()
