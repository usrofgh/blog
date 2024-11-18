from fastapi import APIRouter, status
from fastapi.params import Depends

from dependencies import get_current_user, get_curr_post, get_curr_comment, SessionObj, CurrUserObj, LikeServiceObj
from models.likes import ResourceType
from schemas.like_schemas import LikeReadSchema, LikeBaseSchema

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
        db: SessionObj,
        curr_user: CurrUserObj,
        like_service: LikeServiceObj,
        post_id: int,
        like_schema: LikeBaseSchema,
):
    return await like_service.create_reaction(
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
async def get_post_reactions(db: SessionObj, like_service: LikeServiceObj):
    return await like_service.get_reactions(db=db, resource_type=ResourceType.POST)


@like_router.post(
    path="/posts/{post_id}/comments/{comment_id}/likes",
    response_model=LikeReadSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_curr_comment)]
)
async def comment_reaction(
        db: SessionObj,
        curr_user: CurrUserObj,
        like_service: LikeServiceObj,
        comment_id: int,
        like_schema: LikeBaseSchema,
):
    return await like_service.create_reaction(
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
async def get_comment_reactions(db: SessionObj, like_service: LikeServiceObj):
    return await like_service.get_reactions(db=db, resource_type=ResourceType.COMMENT)
