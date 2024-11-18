from repositories.abstract_repository import SQLRepository
from models.auth_tokens import AuthTokenModel


class AuthRepository(SQLRepository):
    MODEL = AuthTokenModel
