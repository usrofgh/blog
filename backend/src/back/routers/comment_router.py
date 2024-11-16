from typing import Annotated

from fastapi import APIRouter, Depends, status, Path
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession as AS

from back.dependencies import get_current_user, get_curr_post
from back.models.users import UserModel
from back.schemas.comment_schemas import CommentCreateSchema, CommentEditSchema, CommentReadSchema
from back.services.comment_service import CommentService
from database import get_db

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
    post_id: int,
    comment_data: CommentCreateSchema,
    db: AS = Depends(get_db),
    db_user: UserModel = Depends(get_current_user)
):
    return await CommentService.create_comment(db=db, comment_data=comment_data, curr_user=db_user, post_id=post_id)


@comment_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[CommentReadSchema],
    dependencies=[Depends(get_current_user), Depends(get_curr_post)]
)
@version(1)
async def read_comments(post_id: int, db: AS = Depends(get_db)):
    return await CommentService.read_comments(db=db, post_id=post_id)

@comment_router.get(
    path="/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentReadSchema,
    dependencies=[Depends(get_current_user), Depends(get_curr_post)]
)
@version(1)
async def read_comment(comment_id: Annotated[int, Path(gt=0)], db: AS = Depends(get_db)):
    return await CommentService.read_comment_by_id(db=db, id=comment_id)


@comment_router.patch(
    path="/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentReadSchema,
    dependencies=[Depends(get_curr_post)]
)
@version(1)
async def update_comment(
    comment_id: int,
    comment_data: CommentEditSchema,
    db: AS = Depends(get_db),
    curr_user: UserModel = Depends(get_current_user)
):
    return await CommentService.update_comment(db=db, comment_id=comment_id, comment_data=comment_data, curr_user=curr_user)


@comment_router.delete(
    path="/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user), Depends(get_curr_post)]
)
@version(1)
async def delete_comment(
    comment_id: int,
    db: AS = Depends(get_db),
    db_user: UserModel = Depends(get_current_user)
):
    await CommentService.delete_comment(db=db, id=comment_id, curr_user=db_user)
