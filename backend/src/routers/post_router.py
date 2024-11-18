from typing import Annotated

from fastapi import APIRouter, Depends, status, Query
from fastapi_versioning import version

from dependencies import get_current_user, SessionObj, CurrUserObj, PostServiceObj
from schemas.post_schemas import PostCreateResponseSchema, PostCreateSchema, PostFilterSchema, PostReadSchema

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
    db: SessionObj,
    db_user: CurrUserObj,
    post_service: PostServiceObj,
    post_data: PostCreateSchema,
):
    return await post_service.create_post(db=db, post_data=post_data, curr_user=db_user)


@post_router.get(
    path="/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostReadSchema,
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def get_post(
        db: SessionObj,
        post_service: PostServiceObj,
        post_id: int
):
    return await post_service.get_post_by_id(db=db, id=post_id)


@post_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[PostReadSchema],
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def get_posts(
        db: SessionObj,
        post_service: PostServiceObj,
        filters: Annotated[PostFilterSchema, Query()]
):
    return await post_service.get_posts(db=db, filters=filters)


@post_router.delete(
    path="/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@version(1)
async def delete_post(
    db: SessionObj,
    db_user: CurrUserObj,
    post_service: PostServiceObj,
    post_id: int,
):
    await post_service.soft_delete(db=db, id=post_id, curr_user=db_user)
