from typing import Annotated

from fastapi import APIRouter, Depends, status, Query
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dependencies import get_current_user
from src.back.models.users import UserModel
from src.back.schemas.user_schemas import AutoReplyDelaySchema, UserCreateSchema, UserFilterSchema, UserReadSchema
from src.back.services.user_service import UserService
from src.database import get_db

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
async def get_me(curr_user: UserModel = Depends(get_current_user)):
    return curr_user


@user_router.get(
    path="/me/auto-reply/enable",
    status_code=status.HTTP_200_OK
)
@version(1)
async def enable_auto_reply(db: AS = Depends(get_db), curr_user: UserModel = Depends(get_current_user)):
    await UserService.enable_auto_reply(db=db, curr_user=curr_user)


@user_router.get(
    path="/me/auto-reply/disable",
    status_code=status.HTTP_200_OK
)
@version(1)
async def disable_auto_reply(db: AS = Depends(get_db), curr_user: UserModel = Depends(get_current_user)):
    await UserService.disable_auto_reply(db=db, curr_user=curr_user)


@user_router.post(
    path="/me/auto-reply/delay",
    status_code=status.HTTP_200_OK
)
@version(1)
async def setup_reply_delay(
    delay: AutoReplyDelaySchema,
    db: AS = Depends(get_db),
    curr_user: UserModel = Depends(get_current_user)
):
    await UserService.setup_delay(db=db, curr_user=curr_user, delay=delay)


# ------------------------------------------------------------------------------------------------------------

@user_router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
@version(1)
async def create_user(user_data: UserCreateSchema, db: AS = Depends(get_db)):
    return await UserService.create_user(db=db, user_data=user_data)


@user_router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def read_user(user_id: int, db: AS = Depends(get_db)):
    return await UserService.read_user_by_id(db=db, id=user_id)


@user_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[UserReadSchema],
    dependencies=[Depends(get_current_user)]
)
@version(1)
async def read_users(filters: Annotated[UserFilterSchema, Query()], db: AS = Depends(get_db)):
    return await UserService.read_users(db=db, filters=filters)


@user_router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@version(1)
async def delete_user(user_id: int, db: AS = Depends(get_db), curr_user: UserModel = Depends(get_current_user)):
    await UserService.delete_user(db=db, id=user_id, curr_user=curr_user)
