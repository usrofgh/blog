from pydantic import BaseModel

from back.models.connections import Status


class ConnectionHistorySchema(BaseModel):
    connection_id: int
    status: Status
