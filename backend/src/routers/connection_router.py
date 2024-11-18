from fastapi import APIRouter, status as status_codes, Depends

from dependencies import get_current_user, get_user_by_id, ConnServiceObj, SessionObj, CurrUserObj
from exceptions.user_exceptions import UserForbiddenException
from models.connections import Status
from schemas.connection_schemas import ConnectionReadSchema


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
        db: SessionObj,
        conn_service: ConnServiceObj,
        user_id: int,
):
    return await conn_service.get_followers(db=db, follower_id=user_id)

@connection_router.get(
    path="/following",
    response_model=list[int],
    status_code=status_codes.HTTP_200_OK,
    dependencies=[Depends(get_current_user), Depends(get_user_by_id)]
)
async def get_following(
        db: SessionObj,
        conn_service: ConnServiceObj,
        user_id: int,
):
    return await conn_service.get_following(db=db, follower_id=user_id)

@connection_router.post(
    path="/follow/{target_user_id}",
    status_code=status_codes.HTTP_200_OK,
    response_model=ConnectionReadSchema
)
async def follow(
        db: SessionObj,
        conn_service: ConnServiceObj,
        curr_user: CurrUserObj,
        user_id: int,
        target_user_id: int
):
    if curr_user.id != user_id:
        raise UserForbiddenException()
    return await conn_service.create_connection(db=db, follower_id=curr_user.id, followed_id=target_user_id)

@connection_router.delete(
    path="/follow/{target_user_id}",
    status_code=status_codes.HTTP_200_OK,
    response_model=ConnectionReadSchema
)
async def unfollow(
        db: SessionObj,
        conn_service: ConnServiceObj,
        curr_user: CurrUserObj,
        user_id: int,
        target_user_id: int,
):
    if curr_user.id != user_id:
        raise UserForbiddenException()

    return await conn_service.unfollow(db=db, follower_id=curr_user.id, followed_id=target_user_id)


@connection_router.patch(
    path="/follow/{target_user_id}",
    status_code=status_codes.HTTP_200_OK,
)
async def accept_or_reject_connection(
        db: SessionObj,
        curr_user: CurrUserObj,
        conn_service: ConnServiceObj,
        user_id: int,
        target_user_id: int,
        status: Status,
):
    if curr_user.id != target_user_id:
        raise UserForbiddenException()

    return await conn_service.accept_or_reject_request(
        db=db,
        follower_id=user_id,
        followed_id=target_user_id,
        status=status
    )
