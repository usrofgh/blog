from fastapi import APIRouter, Depends, status, Query
from fastapi_cache.decorator import cache
from fastapi_versioning import version
from typing import Annotated

from dependencies import get_current_user, SessionObj
from schemas.analytic_schemas import CommentFilterSchema, AnalyticCommentSchema
from services.analytic_service import AnalyticService

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
async def comments_daily_breakdown(db: SessionObj, filters: Annotated[CommentFilterSchema, Query()]):
    return await AnalyticService.analytic_comments(db=db, filters=filters)
