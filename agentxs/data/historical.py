from typing import Sequence, Any

from sqlalchemy import ColumnElement, select, delete, ColumnExpressionArgument, update, inspect, func
from sqlalchemy.orm import Session

from agentxs.data import engine
from agentxs.models.historical import HistoricalChats


def create_historical(historical: HistoricalChats, get_id: bool = False) -> bool | int:
    """
    Adds a new historical to the database.
    :param historical:
    :param get_id: Forces to return id of the new element.
    :returns: ``True`` if the object has been saved. Otherwise, ``False``. Or if
    """
    with Session(engine) as session:
        session.add(historical)
        session.commit()
        if get_id:
            return historical.id
        return inspect(historical).persistent


def get_historical(offset: int | None = None, limit: int | None = None, ordered_by: ColumnElement | None = None,
                   order_desc=False, where: ColumnExpressionArgument[bool] | None = None) -> Sequence[HistoricalChats]:
    """
    Gets saved historical.
    :param offset:
    :param limit:
    :param ordered_by:
    :param order_desc:
    :param where:
    :return:
    """
    with Session(engine) as session:
        stmt = select(HistoricalChats)
        if where is not None:
            stmt.where(where)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        if ordered_by is not None:
            stmt = stmt.order_by(ordered_by.desc() if order_desc else ordered_by)

        return session.scalars(stmt).all()


def delete_historical(id: int | list[int]) -> int:
    """
    Deletes the history of a chat.
    :param id:
    :return: Number of modified rows. Expected is 1. 0 if no chat history has been deleted.
    """

    with Session(engine) as session:
        # Attempt to fetch the historical chat instance first.
        if isinstance(id, int):
            chat_to_delete = session.get(HistoricalChats, id)
            if chat_to_delete:
                session.delete(chat_to_delete)
        else:
            chats_to_delete = session.scalars(session.query(HistoricalChats).filter(HistoricalChats.id.in_(id))).all()
            for chat in chats_to_delete:
                session.delete(chat)

        session.commit()
        return len(chats_to_delete) if isinstance(id, list) else (1 if chat_to_delete else 0)


def update_historical(id: int, values: dict[str, Any]) -> int:
    """
    :param id:
    :param values:
    :return: Number of modified rows. 0 if no entry has been modified.
    """
    with Session(engine) as session:
        stmt = update(HistoricalChats).where(HistoricalChats.id == id).values(values)
        result = session.execute(stmt)
        session.commit()
        return result.rowcount

def count_historical() -> int:
    with Session(engine) as session:
        return session.execute(select(func.count()).select_from(HistoricalChats)).scalars().one()