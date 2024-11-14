from fastapi import APIRouter, Depends, status, Query
from fastapi_cache.decorator import cache
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession as AS
from typing import Annotated

from src.back.dependencies import get_current_user
from src.back.schemas.analytic_schemas import CommentFilterSchema, AnalyticCommentSchema
from src.back.services.analytic_service import AnalyticService
from src.database import get_db

analytic_router = APIRouter(
    prefix="/analytic",
    tags=["Analytic"]
)


@analytic_router.get(
    path='/comments-daily-breakdown',
    status_code=status.HTTP_200_OK,
    response_model=list[AnalyticCommentSchema],
    dependencies=[Depends(get_current_user)]
)
@version(1)
@cache(expire=30)
async def comments_daily_breakdown(filters: Annotated[CommentFilterSchema, Query()], db: AS = Depends(get_db)):
    return await AnalyticService.analytic_comments(db=db, filters=filters)
