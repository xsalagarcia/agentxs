import os
from unittest.mock import patch, Mock

from agentxs.settings.settings import settings

os.environ["IN_MEMORY_DB"] = "Yes"

from agentxs.data import restart_db, historical as data
from agentxs.models.historical import HistoricalChats



from sqlalchemy.orm.exc import DetachedInstanceError
import unittest


class TestHistorical(unittest.TestCase):
    def tearDown(self):
        restart_db()

    def test_create_historical(self):
        historical = HistoricalChats(agent_name="Python agent", name="name", description="A nice chat")
        self.assertTrue(data.create_historical(historical=historical))
        self.assertEqual(1, data.count_historical())

        historical2 = HistoricalChats(agent_name="Python agent", name="name2", description="Another nice chat")
        self.assertEqual(2, data.create_historical(historical=historical2, get_id=True))



    def test_update_historical(self):
        historical = HistoricalChats(agent_name="Python agent", name="name", description="A nice chat")
        self.assertTrue(data.create_historical(historical=historical))

        self.assertEqual(1, data.update_historical(id=1, values={"description": "It was a nice night..."}))
        self.assertEqual(data.get_historical()[0].description, "It was a nice night...")

    def test_get_historical(self):
        [data.create_historical(HistoricalChats(agent_name=f"Agent {i}", name="name", description=f"Description number {i}"))
         for i in range(1, 10)]

        historical_chats = data.get_historical()
        self.assertEqual(9, len(historical_chats))
        for i, hx in enumerate(historical_chats, 1):
            self.assertEqual(f"Agent {i}", hx.agent_name)

        historical_chats = data.get_historical(offset=0, limit=4, ordered_by=HistoricalChats.agent_name)
        self.assertEqual(4, len(historical_chats))
        for i, hx in enumerate(historical_chats, 1):
            self.assertEqual(f"Agent {i}", hx.agent_name)

        historical_chats = data.get_historical(offset=0, limit=4, ordered_by=HistoricalChats.agent_name, order_desc=True)
        self.assertEqual(4, len(historical_chats))
        for i, hx in enumerate(historical_chats, 1):
            self.assertEqual(f"Agent {10-i}", hx.agent_name)

    @patch("os.remove")
    def test_delete_historical(self, *args: Mock):
        historical = HistoricalChats(agent_name="Python agent", name="name", description="A nice chat")
        self.assertTrue(data.create_historical(historical=historical))

        self.assertEqual(1, data.delete_historical(1))
        args[0].assert_called_once_with(path=settings.data_folder.joinpath("1.json"))




