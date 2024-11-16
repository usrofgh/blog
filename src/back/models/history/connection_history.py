from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseModel


class ConnectionHistoryModel(BaseModel):
    __tablename__ = "connections_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    connection_id: Mapped[int] = mapped_column(ForeignKey("connections.id"))
    status: Mapped[str]
    changed_at: Mapped[datetime] = mapped_column(server_default=func.now())
