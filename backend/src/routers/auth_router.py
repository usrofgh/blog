from fastapi import APIRouter, status
from fastapi_versioning import version

from dependencies import SessionObj, UserServiceObj, AuthServiceObj
from schemas.auth_schemas import JWTLoginResponseSchema, RefreshTokenSchema
from schemas.user_schemas import UserLoginSchema
from services.user_service import UserService

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
async def login(db: SessionObj, user_data: UserLoginSchema):
    return await UserService.login(db=db, user_data=user_data)


@auth_router.get("/activate-account/{activation_code}", status_code=status.HTTP_200_OK)
@version(1)
async def activate_account(
        db: SessionObj,
        user_service: UserServiceObj,
        activation_code: str
):
    return await user_service.activate_account(db=db, activation_code=activation_code)


@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
@version(1)
async def refresh_token(
        db: SessionObj,
        auth_service: AuthServiceObj,
        token: RefreshTokenSchema

):
    return await auth_service.refresh_token(db=db, refresh_token=token.refresh_token)
