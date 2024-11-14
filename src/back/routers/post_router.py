from typing import Annotated

from fastapi import APIRouter, Depends, status, Query
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dependencies import get_current_user
from src.back.models.users import UserModel
from src.back.schemas.post_schemas import PostCreateResponseSchema, PostCreateSchema, PostFilterSchema, PostReadSchema
from src.back.services.post_service import PostService
from src.database import get_db

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@post_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=PostCreateResponseSchema
)
@version(1)
async def create_post(
    post_data: PostCreateSchema,
    db: AS = Depends(get_db),
    db_user: UserModel = Depends(get_current_user)
):
    return await PostService.create_post(db=db, post_data=post_data, curr_user=db_user)


@post_router.get(
    path="/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostReadSchema,
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def read_post(post_id: int, db: AS = Depends(get_db)):
    return await PostService.read_post_by_id(db=db, id=post_id)


@post_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[PostReadSchema],
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def read_posts(filters: Annotated[PostFilterSchema, Query()], db: AS = Depends(get_db)):
    return await PostService.read_posts(db=db, filters=filters)


@post_router.delete(
    path="/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@version(1)
async def delete_post(
    post_id: int,
    db: AS = Depends(get_db),
    db_user: UserModel = Depends(get_current_user)
):
    await PostService.delete_post(db=db, id=post_id, curr_user=db_user)
