import logging

from agents import function_tool, RunContextWrapper
from sqlalchemy import text, inspect
from sqlalchemy.engine.interfaces import ReflectedColumn, ReflectedPrimaryKeyConstraint, ReflectedForeignKeyConstraint

from agentxs.models.pydanticmodels.tableatpostgres import TableAtPostgres
from agentxs.myagents.postgresagentwrappercontext import PostgresAgentWrapperContext


def _get_available_tables_from_database(context: PostgresAgentWrapperContext) -> list[TableAtPostgres]:
    with context.database_engine.connect() as connection:
        result = connection.execute(text("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema');
            """))

        return [TableAtPostgres(table_schema=row.table_schema, table_name=row.table_name) for row in result]


@function_tool
def get_available_tables_from_database(ctx: RunContextWrapper[PostgresAgentWrapperContext]) -> list[TableAtPostgres]:
    """
    Returns a list of the table names and their associated schemas.
    :param ctx:
    :return:
    """
    logging.info("Accessing to get_available_tables_from_database.")
    return _get_available_tables_from_database(context=ctx.context)


def _get_columns_and_basic_properties(context: PostgresAgentWrapperContext, schema_name: str, table_name: str) \
        -> list[ReflectedColumn]:
    # ReflectedColumn is a TypedDict, so openai agents library should parse it to the agent.
    inspector = inspect(context.database_engine)
    return inspector.get_columns(schema=schema_name, table_name=table_name)


@function_tool
def get_columns_and_basic_properties(ctx: RunContextWrapper[PostgresAgentWrapperContext], schema_name: str,
                                     table_name: str) \
        -> list[ReflectedColumn]:
    logging.info("Accessing to get_columns_and_basic_properties")
    return _get_columns_and_basic_properties(context=ctx.context, schema_name=schema_name, table_name=table_name)


def _get_primary_keys(context: PostgresAgentWrapperContext, schema_name: str, table_name: str) -> list[str]:
    inspector = inspect(context.database_engine)
    return inspector.get_pk_constraint(schema=schema_name, table_name=table_name)["constrained_columns"]


@function_tool
def get_primary_keys(ctx: RunContextWrapper[PostgresAgentWrapperContext], schema_name: str, table_name: str) -> list[str]:
    logging.info("Accessing to get_primary_keys")
    return _get_primary_keys(context=ctx.context, schema_name=schema_name, table_name=table_name)


def _get_foreign_keys(context: PostgresAgentWrapperContext, schema_name: str, table_name: str) \
        -> list[ReflectedForeignKeyConstraint]:
    # ReflectedColumn is a TypedDict, so openai agents library should parse it to the agent.
    inspector = inspect(context.database_engine)
    return inspector.get_foreign_keys(schema=schema_name, table_name=table_name)


@function_tool
def get_foreign_keys(ctx: RunContextWrapper[PostgresAgentWrapperContext], schema_name: str, table_name: str) \
        -> list[ReflectedForeignKeyConstraint]:
    logging.info("Accessing to get_foreign_keys")
    return _get_foreign_keys(context=ctx.context, table_name=table_name, schema_name=schema_name)