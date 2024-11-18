from models.connections import ConnectionModel
from repositories.abstract_repository import SQLRepository


class ConnectionRepository(SQLRepository):
    MODEL = ConnectionModel
