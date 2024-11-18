from asyncpg.pgproto.pgproto import timedelta
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession as AS

from models.comments import CommentModel
from schemas.analytic_schemas import CommentFilterSchema, AnalyticCommentSchema


class AnalyticService:

    @staticmethod
    async def analytic_comments(db: AS, filters: CommentFilterSchema) -> list[AnalyticCommentSchema]:
        stmt = select(
            func.date(CommentModel.created_at).label("created_at"),
            func.count().label("total_count"),
            func.count(case((CommentModel.is_blocked == True, 1), else_=None)).label("blocked_count"),  # noqa E712
            func.count(case((CommentModel.is_blocked == False, 1), else_=None)).label("passed_count")  # noqa E712
        ).where(
            CommentModel.created_at.between(filters.date_from, filters.date_to + timedelta(days=1))
        ).group_by(
            func.date(CommentModel.created_at)
        )
        ans = (await db.execute(stmt)).mappings().all()
        ans = [AnalyticCommentSchema(**rec) for rec in ans]

        return ans
