from fastapi import APIRouter, status as status_codes, Depends

from back.dependencies import get_current_user, get_user_by_id
from back.exceptions.user_exceptions import UserForbiddenException
from back.models.connections import Status
from back.models.users import UserModel
from back.schemas.connection_schemas import ConnectionReadSchema

from back.services.connection_service import ConnectionService
from sqlalchemy.ext.asyncio import AsyncSession as AS

from database import get_db

connection_router = APIRouter(
    prefix="/users/{user_id}",
    tags=["Connections"]
)


@connection_router.get(
    path="/followers",
    response_model=list[int],
    status_code=status_codes.HTTP_200_OK,
    dependencies=[Depends(get_current_user), Depends(get_user_by_id)]
)
async def get_followers(
        user_id: int,
        db: AS = Depends(get_db)
):
    return await ConnectionService.read_followers(db=db, follower_id=user_id)

@connection_router.get(
    path="/following",
    response_model=list[int],
    status_code=status_codes.HTTP_200_OK,
    dependencies=[Depends(get_current_user), Depends(get_user_by_id)]
)
async def get_following(
        user_id: int,
        db: AS = Depends(get_db)
):
    return await ConnectionService.read_following(db=db, follower_id=user_id)

@connection_router.post(
    path="/follow/{target_user_id}",
    status_code=status_codes.HTTP_200_OK,
    response_model=ConnectionReadSchema
)
async def follow(
        user_id: int,
        target_user_id: int,
        curr_user: UserModel = Depends(get_current_user),
        db: AS = Depends(get_db)
):
    if curr_user.id != user_id:
        raise UserForbiddenException()
    return await ConnectionService.create_connection(db=db, follower_id=curr_user.id, followed_id=target_user_id)

@connection_router.delete(
    path="/follow/{target_user_id}",
    status_code=status_codes.HTTP_200_OK,
    response_model=ConnectionReadSchema
)
async def unfollow(
        user_id: int,
        target_user_id: int,
        curr_user: UserModel = Depends(get_current_user),
        db: AS = Depends(get_db)
):
    if curr_user.id != user_id:
        raise UserForbiddenException()

    return await ConnectionService.unfollow(db=db, follower_id=curr_user.id, followed_id=target_user_id)


@connection_router.patch(
    path="/follow/{target_user_id}",
    status_code=status_codes.HTTP_200_OK,
    dependencies=[Depends(get_current_user)]
)
async def accept_or_reject_connection(
        user_id: int,
        target_user_id: int,
        status: Status,
        db: AS = Depends(get_db),
        curr_user: UserModel = Depends(get_current_user)
):
    if curr_user.id != target_user_id:
        raise UserForbiddenException()

    return await ConnectionService.accept_or_reject_request(
        db=db,
        follower_id=user_id,
        followed_id=target_user_id,
        status=status
    )
