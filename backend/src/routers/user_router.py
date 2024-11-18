from typing import Annotated

from fastapi import APIRouter, status, Query, File, UploadFile, Depends
from fastapi_versioning import version

from dependencies import SessionObj, UserServiceObj, CurrUserObj, get_current_user
from exceptions.user_exceptions import UserForbiddenException
from schemas.user_schemas import AutoReplyDelaySchema, UserCreateSchema, UserFilterSchema, UserReadSchema

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ------------------------------------------------------------------------------------------------------------
@user_router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema
)
@version(1)
async def get_me(curr_user: CurrUserObj):
    return curr_user


@user_router.get(
    path="/me/auto-reply/enable",
    status_code=status.HTTP_200_OK
)
@version(1)
async def enable_auto_reply(
        db: SessionObj,
        user_service: UserServiceObj,
        curr_user: CurrUserObj
):
    await user_service.enable_auto_reply(db=db, curr_user=curr_user)


@user_router.get(
    path="/me/auto-reply/disable",
    status_code=status.HTTP_200_OK
)
@version(1)
async def disable_auto_reply(
        db: SessionObj,
        user_service: UserServiceObj,
        curr_user: CurrUserObj
):
    await user_service.disable_auto_reply(db=db, curr_user=curr_user)


@user_router.post(
    path="/me/auto-reply/delay",
    status_code=status.HTTP_200_OK
)
@version(1)
async def setup_reply_delay(
        db: SessionObj,
        user_service: UserServiceObj,
        delay: AutoReplyDelaySchema,
        curr_user: CurrUserObj
):
    await user_service.setup_delay(db=db, curr_user=curr_user, delay=delay)


# ------------------------------------------------------------------------------------------------------------

@user_router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
@version(1)
async def register_user(
        db: SessionObj,
        user_service: UserServiceObj,
        user_data: UserCreateSchema
):
    return await user_service.create_user(db=db, user_data=user_data)


@user_router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def get_user(
        db: SessionObj,
        user_service: UserServiceObj,
        user_id: int
):
    return await user_service.get_user(db=db, id=user_id)


@user_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[UserReadSchema],
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def get_users(
        db: SessionObj,
        user_service: UserServiceObj,
        filters: Annotated[UserFilterSchema, Query()]
):
    return await user_service.get_users(db=db, filters=filters)


@user_router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@version(1)
async def delete_user(
        db: SessionObj,
        user_service: UserServiceObj,
        curr_user: CurrUserObj,
        user_id: int,
):
    await user_service.soft_delete_user(db=db, id=user_id, curr_user=curr_user)


@user_router.post(
    path="/{user_id}/avatar",
    status_code=status.HTTP_200_OK
)
@version(1)
async def upload_avatar(
        db: SessionObj,
        user_service: UserServiceObj,
        curr_user: CurrUserObj,
        user_id: int,
        avatar: UploadFile = File(...),
):
    if curr_user.id != user_id:
        raise UserForbiddenException

    await user_service.upload_avatar(db=db, curr_user=curr_user, avatar=avatar)


@user_router.delete(
    path="/{user_id}/avatar",
    status_code=status.HTTP_204_NO_CONTENT
)
@version(1)
async def delete_avatar(
        db: SessionObj,
        user_service: UserServiceObj,
        user_id: int,
        curr_user: CurrUserObj,
):
    if curr_user.id != user_id:
        raise UserForbiddenException

    await user_service.avatar_to_archive(db=db, curr_user=curr_user)
