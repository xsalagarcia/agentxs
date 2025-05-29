from dataclasses import dataclass

from sqlalchemy import Engine


@dataclass
class PostgresAgentWrapperContext:
    database_engine: Engine | None = None
    """ use connection -> https://docs.sqlalchemy.org/en/20/core/connections.html#basic-usage"""