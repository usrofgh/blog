import uuid

from arq import create_pool
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dao.auth_token_dao import AuthTokenDAO
from src.back.dao.user_dao import UserDAO
from src.back.exceptions.auth_exceptions import IncorrectCredsException
from src.back.exceptions.user_exceptions import (
    IncorrectActivationLink,
    UnactivatedException,
    UserExistException,
    UserForbiddenException,
    UserNotFoundException
)
from src.back.models.users import UserModel
from src.back.schemas.auth_schemas import JWTLoginResponseSchema
from src.back.schemas.user_schemas import (
    AutoReplyDelaySchema,
    UserCreateDBSchema,
    UserCreateSchema,
    UserFilterSchema,
    UserLoginSchema,
    UserUpdateSchema
)
from src.back.services.auth_service import AuthService
from src.back.tasks.task_manager import REDIS_SETTINGS, send_activation_email


class UserService:
    @staticmethod
    async def create_user(db: AS, user_data: UserCreateSchema) -> dict:
        user_data.password = AuthService.get_password_hash(user_data.password)
        db_user = await UserDAO.read_user_by_email(db=db, email=user_data.email)
        if db_user:
            raise UserExistException

        activation_code = uuid.uuid4().hex
        user_data = UserCreateDBSchema(**user_data.model_dump(), activation_code=activation_code)
        await UserDAO.create_user(db=db, user_data=user_data)

        redis = await create_pool(REDIS_SETTINGS)
        await redis.enqueue_job(
            function=send_activation_email.__name__,
            to=user_data.email,
            activation_code=activation_code
        )
        return {
            "status": status.HTTP_201_CREATED,
            "details": "Activation link has been sent to email"
        }

    @classmethod
    async def login(cls, db: AS, user_data: UserLoginSchema) -> JWTLoginResponseSchema:
        db_user = await AuthService.authenticate_user(db=db, email=user_data.email, password=user_data.password)
        if not db_user:
            raise IncorrectCredsException
        if db_user.is_activated is False:
            raise UnactivatedException

        token_data = AuthService.generate_tokens(db_user.id)
        await AuthService.save_token(db=db, user_id=db_user.id, refresh_token=token_data.refresh_token)
        return token_data

    @staticmethod
    async def read_user_by_id(db: AS, id: int) -> UserModel:
        user = await UserDAO.read_user_by_id(db=db, id=id)
        if not user:
            raise UserNotFoundException
        return user

    @staticmethod
    async def read_user_by_email(db: AS, email: str) -> UserModel:
        user = await UserDAO.read_user_by_email(db=db, email=email)
        if not user:
            raise UserNotFoundException
        return user

    @staticmethod
    async def read_users(db: AS, filters: UserFilterSchema) -> list[UserModel]:
        filters = filters.model_dump(exclude_none=True)
        users = await UserDAO.read_users(db=db, **filters)
        return users

    @staticmethod
    async def update_user(db: AS, user: UserUpdateSchema) -> None:
        db_user = await UserDAO.read_user_by_id(db=db, id=user.id)
        if not db_user:
            raise UserNotFoundException
        await UserDAO.update_user(db=db, db_obj=db_user, obj_in=user)

    @staticmethod
    async def delete_user(db: AS, id: int, curr_user: UserModel) -> None:
        user = await UserDAO.read_user_by_id(db=db, id=id)
        if not user:
            raise UserNotFoundException

        if id != curr_user.id and curr_user.is_admin is False:
            raise UserForbiddenException
        await UserDAO.delete_user(db=db, db_obj=user)

    @staticmethod
    async def enable_auto_reply(db: AS, curr_user: UserModel) -> None:
        if not curr_user.auto_reply:
            curr_user.auto_reply = True
            await db.commit()

    @staticmethod
    async def disable_auto_reply(db: AS, curr_user: UserModel) -> None:
        if curr_user.auto_reply:
            curr_user.auto_reply = False
            await db.commit()

    @staticmethod
    async def setup_delay(db: AS, curr_user: UserModel, delay: AutoReplyDelaySchema) -> None:
        curr_user.auto_reply_sec_delay = delay.delay
        await db.commit()

    @staticmethod
    async def activate_account(activation_code: str, db: AS) -> None:
        db_user: UserModel = await UserDAO.read_user_by_act_code(db=db, activation_code=activation_code)
        if not db_user:
            raise IncorrectActivationLink

        db_user.is_activated = True
        await db.commit()

    @staticmethod
    async def refresh_token(refresh_token: str, db: AS) -> JWTLoginResponseSchema:
        payload = AuthService.validate_refresh_token(refresh_token)
        db_token = await AuthTokenDAO.read_by_token(refresh_token, db=db)

        if not (payload and db_token):
            raise IncorrectCredsException

        tokens = AuthService.generate_tokens(payload["sub"])
        await AuthService.save_token(db=db, user_id=payload["sub"], refresh_token=tokens.refresh_token)
        return tokens

    # TODO: Implement 'reset_password' method
