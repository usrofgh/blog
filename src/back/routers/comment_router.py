from fastapi import APIRouter, Depends, status
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dependencies import get_current_user
from src.back.models.users import UserModel
from src.back.schemas.comment_schemas import CommentCreateSchema, CommentEditSchema, CommentReadSchema
from src.back.services.comment_service import CommentService
from src.database import get_db

comment_router = APIRouter(
    prefix="/api/comments",
    tags=["Comment"]
)


@comment_router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentReadSchema
)
@version(1)
async def create_comment(
    comment_data: CommentCreateSchema,
    db: AS = Depends(get_db),
    db_user: UserModel = Depends(get_current_user)
):
    return await CommentService.create_comment(db=db, comment_data=comment_data, curr_user=db_user)


@comment_router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentReadSchema,
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def read_comment(id: int, db: AS = Depends(get_db)):
    return await CommentService.read_comment_by_id(db=db, id=id)


@comment_router.patch(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentReadSchema,
)
@version(1)
async def update_comment(
    comment_data: CommentEditSchema = Depends(),
    db: AS = Depends(get_db),
    curr_user=Depends(get_current_user)
):
    return await CommentService.update_comment(db=db, comment_data=comment_data, curr_user=curr_user)


@comment_router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def delete_comment(
    id: int,
    db: AS = Depends(get_db),
    db_user: UserModel = Depends(get_current_user)
):
    await CommentService.delete_comment(db=db, id=id, curr_user=db_user)
