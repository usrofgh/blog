from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.models.comments import CommentModel
from src.back.schemas.analytic_schemas import AnalyticCommentFilterSchema, AnalyticCommentSchema


class AnalyticService:

    @staticmethod
    async def analytic_comments(db: AS, filters: AnalyticCommentFilterSchema) -> list[AnalyticCommentSchema]:
        stmt = select(
            func.date(CommentModel.created_at).label("created_at"),
            func.count().label("total_count"),
            func.count(case((CommentModel.is_blocked == True, 1), else_=None)).label("blocked_count"),
            func.count(case((CommentModel.is_blocked == False, 1), else_=None)).label("passed_count")
        ).where(
            CommentModel.created_at.between(filters.date_from, filters.date_to)
        ).group_by(
            func.date(CommentModel.created_at)
        )
        ans = (await db.execute(stmt)).mappings().all()
        ans = [AnalyticCommentSchema(**rec) for rec in ans]

        return ans
