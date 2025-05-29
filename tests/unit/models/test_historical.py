import unittest
from datetime import datetime
from time import sleep

from sqlalchemy import inspect

from agentxs.models.historical import HistoricalChats


class TestHistorical(unittest.TestCase):

    def test_get_dict(self):
        historical = HistoricalChats(agent_name="agent name", name="name", description="description about", last_modification=datetime.now())

        ma = inspect(historical)
        my_dict = {attr.key: getattr(historical, attr.key) for attr in inspect(historical).attrs }
        print(my_dict)
