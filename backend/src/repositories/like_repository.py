from models.likes import LikeModel
from repositories.abstract_repository import SQLRepository


class LikeRepository(SQLRepository):
    MODEL = LikeModel
