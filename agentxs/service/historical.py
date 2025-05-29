import json
from pathlib import Path
from typing import Any, Sequence

import agentxs.data.historical as data
from agentxs.models.historical import HistoricalChats
from agentxs.settings.settings import settings


def create_historical(agent_name: str, name: str, description: str, chat: list) -> int:
    """
    Sends agent_name, name and description to the database, saves chat to a file.
    :param agent_name:
    :param name:
    :param description:
    :param chat: The list contained at `AgentWrapper.historical`
    :return: The id at database.
    """
    historical = HistoricalChats(agent_name=agent_name, name=name, description=description)
    historical_id = data.create_historical(historical=historical, get_id=True)
    with open(Path(settings.data_folder).joinpath(f"{historical_id}.json"), "w") as file:
        json.dump(chat, file)
    return historical_id


def list_historical_by_agent_name(agent_name: str) -> Sequence[HistoricalChats]:
    return data.get_historical(where=HistoricalChats.agent_name.is_(agent_name), ordered_by=HistoricalChats.name)


def get_historical(id: int) -> Any:
    with open(Path(settings.data_folder).joinpath(f"{id}.json")) as file:
        return json.load(file)


def delete_saved_historical(id: int) -> int:
    data.delete_historical(id=id)