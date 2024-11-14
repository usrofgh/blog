import datetime

import jwt
from asyncpg.pgproto.pgproto import timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jwt import DecodeError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession as AS

from src.back.dao.auth_token_dao import AuthTokenDAO
from src.back.dao.user_dao import UserDAO
from src.back.exceptions.auth_exceptions import JWTIncorrectFormatException, JWTokenExpiredException
from src.back.models.auth_tokens import AuthTokenModel
from src.back.models.users import UserModel
from src.back.schemas.auth_schemas import JWTLoginResponseSchema, RefreshTokenCreateSchema
from src.config import config


class AuthService:
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")

    @classmethod
    def generate_tokens(cls, user_id: int) -> JWTLoginResponseSchema:
        data = {"sub": user_id}
        access_expires_delta = timedelta(minutes=config.JWT_ACCESS_TTL_MIN)
        access_token = cls.create_access_token(data, access_expires_delta)

        refresh_expires_delta = timedelta(minutes=config.JWT_REFRESH_TTL_MIN)
        refresh_token = cls.create_refresh_token(data, refresh_expires_delta)

        token_data = JWTLoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        return token_data

    @staticmethod
    def _create_jwt_token(data: dict, secret_key: str, type_: str, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire, "type": type_})
        encoded_jwt = jwt.encode(to_encode, secret_key, config.JWT_ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta | None = None) -> str:
        token = cls._create_jwt_token(data, config.JWT_ACCESS_KEY.get_secret_value(), "access", expires_delta)
        return token

    @classmethod
    def create_refresh_token(cls, data: dict, expires_delta: timedelta | None = None) -> str:
        token = cls._create_jwt_token(data, config.JWT_REFRESH_KEY.get_secret_value(), "refresh", expires_delta)
        return token

    @classmethod
    def verify_password(cls, plain_password: str, password: str) -> bool:
        return cls.PWD_CONTEXT.verify(plain_password, password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.PWD_CONTEXT.hash(password)

    @classmethod
    async def authenticate_user(cls, db: AS, username: str, password: str) -> UserModel:
        db_user = await UserDAO.read_user_by_username(db=db, username=username)
        if db_user and cls.verify_password(password, db_user.password):
            return db_user

    @classmethod
    def validate_access_token(cls, token: str) -> bool:
        try:
            payload = jwt.decode(
                token,
                config.JWT_ACCESS_KEY,
                config.JWT_ALGORITHM
            )
            if payload["type"] != "access":
                raise JWTIncorrectFormatException

        except JWTError:
            raise JWTIncorrectFormatException

        exp = payload.get("exp")
        if (not exp) or (exp < datetime.datetime.now(datetime.UTC)).timestamp():
            raise JWTokenExpiredException

        return payload

    @classmethod
    def validate_refresh_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                config.JWT_REFRESH_KEY.get_secret_value(),
                algorithms=[config.JWT_ALGORITHM]
            )
            if payload["type"] != "refresh":
                raise JWTIncorrectFormatException

        except (DecodeError, JWTError):
            raise JWTIncorrectFormatException

        exp = payload.get("exp")
        if (not exp) or (exp < datetime.datetime.now(datetime.UTC).timestamp()):
            raise JWTokenExpiredException

        return payload

    @classmethod
    async def save_token(cls, db: AS, user_id: int, refresh_token: str) -> AuthTokenModel:
        db_token: AuthTokenModel = await AuthTokenDAO.read_by_user_id(db=db, user_id=user_id)
        if db_token:
            db_token.refresh_token = refresh_token
            await db.commit()
            return db_token

        token_schema = RefreshTokenCreateSchema(user_id=user_id, refresh_token=refresh_token)
        token = await AuthTokenDAO.create_token(db=db, obj_in=token_schema)
        return token
