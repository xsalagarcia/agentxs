from dataclasses import dataclass

from agents import Agent
from sqlalchemy import Engine, create_engine, text

from agentxs.myagents.agentwrapper import AgentWrapper, AgentMemory
from agentxs.myagents import custompostgrestools as postgrestools
from agentxs.myagents.postgresagentwrappercontext import PostgresAgentWrapperContext


class PostgresAgentWrapper(AgentWrapper):
    def __init__(self, agent: Agent, agent_memory: AgentMemory,
                 context: PostgresAgentWrapperContext = PostgresAgentWrapperContext()):
        super().__init__(agent, agent_memory, context)
        self.agent = agent
        self.agent_memory = agent_memory
        self.__historical = []
        self.__username: str | None = None
        self.__password: str | None = None
        self.__port: int | None = None
        self.__database: str | None = None
        self.__host: str | None = None

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username
        self.__set_database_engine()

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password: str):
        self.__password = password
        self.__set_database_engine()

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port: int):
        self.__port = port
        self.__set_database_engine()

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, database: str):
        self.__database = database
        self.__set_database_engine()

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host: str):
        self.__host = host
        self.__set_database_engine()

    def __set_database_engine(self):
        if self.username is None or self.password is None or self.port is None or self.database is None or self.host is None:
            return

        if self.context is not None and self.context.database_engine is not None:
            self.context.database_engine.dispose()

        self.context.database_engine = create_engine(
            f"postgresql+psycopg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}")

    @property
    def has_db_engine(self):
        return self.context is not None and self.context.database_engine is not None

    def get_missing_connection_params(self) -> list[str]:
        missing_connection_params = list[str]()
        if self.username is None:
            missing_connection_params.append("username")
        if self.password is None:
            missing_connection_params.append("password")
        if self.host is None:
            missing_connection_params.append("host")
        if self.port is None:
            missing_connection_params.append("port")
        if self.database is None:
            missing_connection_params.append("database")
        return missing_connection_params


postgres_agent = PostgresAgentWrapper(
    agent=Agent(
        name="PostgreSQL agent",
        instructions="You provide help about SQL and PostgreSQL. Your answers are based on SQL standard and PostgreSQL "
                     "dialect and its particularities. Use the given tools to retrieve information about the available"
                     "schemas and databases for the user and adapt the SQL sentences to the tables of the database.",
        model="gpt-4o-mini",
        tools=[postgrestools.get_available_tables_from_database,
               postgrestools.get_columns_and_basic_properties,
               postgrestools.get_primary_keys,
               postgrestools.get_foreign_keys]
    ),
    agent_memory=AgentMemory.NONE,
    context=PostgresAgentWrapperContext()
)
