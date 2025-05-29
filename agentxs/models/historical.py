import os
from datetime import datetime

from sqlalchemy import String, DateTime, func, event
from sqlalchemy.orm import mapped_column, Mapped

from agentxs.models.base import Base
from agentxs.settings.settings import settings


class HistoricalChats(Base):
    __tablename__ = "historicalchats"

    id: Mapped[int] = mapped_column(primary_key=True)
    agent_name: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String())
    last_modification: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


@event.listens_for(target=HistoricalChats, identifier="after_delete")
def receive_after_delete(mapper, connection, target):
    os.remove(path=settings.data_folder.joinpath(f"{target.id}.json"))
