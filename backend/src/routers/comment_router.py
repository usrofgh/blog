from typing import Annotated

from fastapi import APIRouter, Depends, status, Path
from fastapi_versioning import version

from dependencies import get_current_user, get_curr_post, SessionObj, CurrUserObj, CommentServiceObj
from schemas.comment_schemas import CommentCreateSchema, CommentEditSchema, CommentReadSchema

comment_router = APIRouter(
    prefix="/posts/{post_id}/comments",
    tags=["Comments"]
)


@comment_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentReadSchema,
    dependencies=[Depends(get_curr_post)]
)
@version(1)
async def create_comment(
    db: SessionObj,
    db_user: CurrUserObj,
    comment_service: CommentServiceObj,
    post_id: int,
    comment_data: CommentCreateSchema,
):
    return await comment_service.create_comment(db=db, comment_data=comment_data, curr_user=db_user, post_id=post_id)


@comment_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[CommentReadSchema],
    dependencies=[Depends(get_current_user), Depends(get_curr_post)]
)
@version(1)
async def get_comments(
        db: SessionObj,
        comment_service: CommentServiceObj,
        post_id: int,
):
    return await comment_service.get_comments(db=db, post_id=post_id)

@comment_router.get(
    path="/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentReadSchema,
    dependencies=[Depends(get_current_user), Depends(get_curr_post)]
)
@version(1)
async def get_comment(
        db: SessionObj,
        comment_service: CommentServiceObj,
        comment_id: Annotated[int, Path(gt=0)]
):
    return await comment_service.read_comment_by_id(db=db, id=comment_id)


@comment_router.patch(
    path="/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentReadSchema
)
@version(1)
async def update_comment(
    db: SessionObj,
    db_user: CurrUserObj,
    comment_service: CommentServiceObj,
    comment_id: int,
    comment_data: CommentEditSchema,
):
    return await comment_service.update_comment(db=db, comment_id=comment_id, comment_data=comment_data, curr_user=db_user)


@comment_router.delete(
    path="/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user), Depends(get_curr_post)]
)
@version(1)
async def delete_comment(
    db: SessionObj,
    db_user: CurrUserObj,
    comment_service: CommentServiceObj,
    comment_id: int,
):
    await comment_service.soft_delete(db=db, id=comment_id, curr_user=db_user)
