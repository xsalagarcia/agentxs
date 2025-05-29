import unittest
from typing import TypedDict, get_origin, is_typeddict

from sqlalchemy import create_engine
from sqlalchemy.engine.interfaces import ReflectedColumn

from agentxs.myagents.custompostgrestools import _get_available_tables_from_database, _get_columns_and_basic_properties, \
    _get_primary_keys, _get_foreign_keys
from agentxs.myagents.postgresagent import PostgresAgentWrapperContext

_database_credentials = {
    "username": "tester",
    "password": "tester",
    "host": "localhost",
    "port": 5432,
    "database": "agents_test"
}

context = PostgresAgentWrapperContext(database_engine=create_engine(f'postgresql+psycopg://'
                                                                    f'{_database_credentials["username"]}:'
                                                                    f'{_database_credentials["password"]}@'
                                                                    f'{_database_credentials["host"]}:'
                                                                    f'{_database_credentials["port"]}/'
                                                                    f'{_database_credentials["database"]}'))

class TestCustomPostgresTools(unittest.TestCase):
    def test_get_available_tables_from_database(self):

        result = _get_available_tables_from_database(context)

        expected_tables = {"artist", "album", "track", "genre"}
        for table in result:
            self.assertEqual(table.table_schema, "public")
            self.assertIn(table.table_name, expected_tables)

    def test_get_columns_and_basic_properties(self):

        result = _get_columns_and_basic_properties(context=context, schema_name="public", table_name="track")

        cols_at_track = {"id", "title", "len", "rating", "count", "album_id", "genre_id"}
        for col in result:
            self.assertIn(col["name"], cols_at_track)

    def test_get_primary_keys(self):
        self.assertTrue(_get_primary_keys(context=context, schema_name="public", table_name="track")[0], "id")

    def test_get_foreign_keys(self):
        for fk in _get_foreign_keys(context=context, schema_name="public", table_name="track"):
            print(fk)
