from pydantic import BaseModel

from models.connections import Status


class ConnectionHistorySchema(BaseModel):
    connection_id: int
    status: Status
