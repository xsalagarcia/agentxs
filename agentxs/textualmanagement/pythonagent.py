import os.path
import re

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Input, Label

from agentxs.myagents.pythonagent import python_agent


class PythonOptions(Container):

    def compose(self) -> ComposeResult:
        yield Label("Project settings")
        input = Input(placeholder="The path of your project", classes="bordered_option",
                      id="path_input")
        input.border_title = "Project path"
        yield input
        input = Input(placeholder="I.e: .py, .tcss", classes="bordered_option",
                      id="extensions_input")
        input.border_title = "File extensions"
        yield input

    @on(message_type=Input.Submitted, selector="#path_input")
    @on(message_type=Input.Blurred, selector="#path_input")
    def set_path(self, event: Input.Submitted | Input.Blurred):
        if os.path.isdir(event.value):
            event.input.add_class("ok")
            python_agent.context.available_path = event.value
        else:
            python_agent.context.available_path = None
            self.notify("Not a valid path!", timeout=2)
            event.input.add_class("ko")

    @on(message_type=Input.Submitted, selector="#extensions_input")
    @on(message_type=Input.Submitted, selector="#extensions_input")
    def set_extensions(self, event: Input.Submitted | Input.Blurred):
        python_agent.context.available_extensions = tuple(re.split(r"\s*,\s*", event.value))
        event.input.add_class("ok")
        self.notify(str(python_agent.context.available_extensions))

