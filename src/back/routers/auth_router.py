from fastapi import APIRouter, Depends, status
from fastapi_versioning import version
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.schemas.auth_schemas import JWTLoginResponseSchema, RefreshTokenSchema
from src.back.schemas.user_schemas import UserLoginSchema
from src.back.services.user_service import UserService
from src.database import get_db

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@auth_router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=JWTLoginResponseSchema
)
@version(1)
async def login(user_data: UserLoginSchema, db: AS = Depends(get_db)):
    return await UserService.login(db=db, user_data=user_data)


@auth_router.get("/activate-account", status_code=status.HTTP_200_OK)
@version(1)
async def activate_account(
    activation_code: str,
    db: AS = Depends(get_db)
):
    return await UserService.activate_account(activation_code=activation_code, db=db)


@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
@version(1)
async def refresh_token(
    token: RefreshTokenSchema,
    db: AS = Depends(get_db)
):
    return await UserService.refresh_token(refresh_token=token.refresh_token, db=db)
