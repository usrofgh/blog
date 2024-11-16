import uuid
from datetime import datetime
from pathlib import Path

from arq import create_pool
from fastapi import status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dao.user_dao import UserDAO
from src.back.exceptions.auth_exceptions import IncorrectCredsException
from src.back.exceptions.user_exceptions import (
    IncorrectActivationLink,
    UnactivatedException,
    UserEmailExistException,
    UserForbiddenException,
    UserNotFoundException,
    UserNameExistException,
    IncorrectAvatarException,
    AvatarDoesNotExist
)
from src.back.models.users import UserModel, UserStatus
from src.back.schemas.auth_schemas import JWTLoginResponseSchema
from src.back.schemas.user_schemas import (
    AutoReplyDelaySchema,
    UserCreateDBSchema,
    UserCreateSchema,
    UserFilterSchema,
    UserLoginSchema
)
from src.back.services.auth_service import AuthService
from src.back.tasks.task_manager import REDIS_SETTINGS, send_activation_email


class UserService:
    @staticmethod
    async def create_user(db: AS, user_data: UserCreateSchema) -> dict:
        db_user = await UserDAO.read_user_by_username(db=db, username=user_data.username)
        if db_user:
            raise UserNameExistException
        db_user = await UserDAO.read_user_by_email(db=db, email=user_data.email)
        if db_user:
            raise UserEmailExistException


        activation_code = uuid.uuid4().hex
        user_data.password = AuthService.get_password_hash(user_data.password)
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
        db_user = await AuthService.authenticate_user(db=db, username=user_data.username, password=user_data.password)
        if not db_user:
            raise IncorrectCredsException
        if db_user.email_verified is False:
            raise UnactivatedException

        token_data = AuthService.generate_tokens(db_user.id)
        await AuthService.save_token(db=db, user_id=db_user.id, refresh_token=token_data.refresh_token)
        return token_data

    @staticmethod
    async def read_user_by_id(db: AS, id: int) -> UserModel:
        user = await UserDAO.read_user_by_id(db=db, id=id)
        if not user or user.status is not user.status.ACTIVE:
            raise UserNotFoundException
        return user

    @staticmethod
    async def read_users(db: AS, filters: UserFilterSchema) -> list[UserModel]:
        filters = filters.model_dump(exclude_none=True)
        users = await UserDAO.read_users(db=db, **filters, status=UserStatus.ACTIVE)
        return users

    @staticmethod
    async def delete_user(db: AS, id: int, curr_user: UserModel) -> None:
        user = await UserDAO.read_user_by_id(db=db, id=id)
        if not user or user.status is user.status.DELETED:
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

        db_user.email_verified = True
        await db.commit()

    @classmethod
    async def upload_avatar(cls, curr_user: UserModel, avatar: UploadFile, db: AS) -> None:
        allowed_extensions = {"png", "jpg", "jpeg"}
        file_extension = avatar.filename.split(".")[-1]
        if file_extension not in allowed_extensions:
            raise IncorrectAvatarException

        path = Path(__file__).parent.parent.parent/"static"/"avatars"/f"{str(curr_user.id)}.{file_extension}"
        if path.exists():
            await cls.avatar_to_archive(curr_user=curr_user, db=db)

        with path.open("wb") as file:
            file.write(await avatar.read())

        if not curr_user.avatar_url:
            curr_user.avatar_url = f"/static/avatars/{str(curr_user.id)}.{file_extension}"
        await db.commit()

    @staticmethod
    async def avatar_to_archive(curr_user: UserModel, db: AS) -> None:
        if not curr_user.avatar_url:
            raise AvatarDoesNotExist

        curr_photo_name = curr_user.avatar_url.split("/")[-1]
        name, ext = curr_photo_name.split(".")
        archived_at = str(datetime.now().timestamp()).replace(".", "")
        archived_photo_name = f"{name}_{archived_at}.{ext}"

        base_path = Path(__file__).parent.parent.parent/"static"
        curr_photo_path = base_path/"avatars"/curr_photo_name
        archive_path = base_path/"archive"
        archive_photo_path = base_path/"archive"/archived_photo_name

        archive_path.mkdir(parents=True, exist_ok=True)
        curr_photo_path.rename(archive_photo_path)
        curr_user.avatar_url = None
        await db.commit()

    # TODO: Implement 'reset_password' method
