import unittest
from unittest.mock import patch, Mock
from agentxs.consolemanagement import common
from agentxs.myagents.pythonagent import python_agent


class TestCLIApp(unittest.TestCase):

    @patch("agentxs.consolemanagement.common.console.print")
    @patch("agentxs.consolemanagement.common.request_user_reply", return_value="The user reply")
    @patch("agentxs.myagents.agentwrapper.AgentWrapper.save_historical")
    def test_save_thread(self, *args: Mock):

        user_reply = common.save_thread('/save_thread "exampl eDescription"', python_agent)

        args[0].assert_not_called()
        args[1].assert_called()
        args[2].assert_called_once_with("Couldn't understand the order. Ensure you type the thread name and description in double "
                      "quotes each one.")
        self.assertEqual(user_reply, args[1].return_value)
        for arg in args:
            arg.reset_mock()

        common.save_thread('/save_thread "this is the name" "This is de description."', python_agent)
        args[0].assert_called_once_with(name="this is the name", description="This is de description.")
        args[1].assert_called()
        args[2].assert_called_once_with("Thread saved!")