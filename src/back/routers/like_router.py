from fastapi import APIRouter, status
from fastapi.params import Depends

from src.back.dependencies import get_current_user, get_curr_post, get_curr_comment
from src.back.models.likes import ResourceType
from src.back.models.users import UserModel
from src.back.schemas.like_schemas import LikeReadSchema, LikeBaseSchema
from src.back.services.like_service import LikeService
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.database import get_db

like_router = APIRouter(
    prefix="",
    tags=["Likes"]
)


@like_router.post(
    path="/posts/{post_id}/likes",
    response_model=LikeReadSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_curr_post)]
)
async def post_reaction(
        post_id: int,
        like_schema: LikeBaseSchema,
        db: AS = Depends(get_db),
        curr_user: UserModel = Depends(get_current_user)
):
    return await LikeService.create_reaction(
        db=db,
        resource_type=ResourceType.POST,
        resource_id=post_id,
        is_like=like_schema.is_like,
        author_id=curr_user.id
    )

@like_router.get(
    path="/posts/{post_id}/likes",
    response_model=list[LikeReadSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user), Depends(get_curr_post)]
)
async def read_post_reactions(db: AS = Depends(get_db)):
    return await LikeService.read_reactions(db=db, resource_type=ResourceType.POST)


@like_router.post(
    path="/posts/{post_id}/comments/{comment_id}/likes",
    response_model=LikeReadSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_curr_comment)]
)
async def comment_reaction(
        comment_id: int,
        like_schema: LikeBaseSchema,
        db: AS = Depends(get_db),
        curr_user: UserModel = Depends(get_current_user)
):
    return await LikeService.create_reaction(
        db=db,
        resource_type=ResourceType.COMMENT,
        resource_id=comment_id,
        is_like=like_schema.is_like,
        author_id=curr_user.id
    )

@like_router.get(
    path="/posts/{post_id}/comments/{comment_id}/likes",
    response_model=list[LikeReadSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user), Depends(get_curr_comment)]
)
async def read_comment_reactions(db: AS = Depends(get_db)):
    return await LikeService.read_reactions(db=db, resource_type=ResourceType.COMMENT)
