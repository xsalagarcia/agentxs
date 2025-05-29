import os

from sqlalchemy import create_engine

from agentxs.models.base import Base
from agentxs.settings.settings import settings
from agentxs.models.historical import HistoricalChats

engine = create_engine(url=f"sqlite:///{settings.data_folder}/mytable.db" if os.getenv("IN_MEMORY_DB") is None else "sqlite://")

# Creates the tables associated to Base if they don't exist.
Base.metadata.create_all(engine)

def restart_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)