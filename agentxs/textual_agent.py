from typing import Literal

from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Static, TextArea, Button, Label, LoadingIndicator, Markdown
from agentxs.textualmanagement.common import CommonOptions
from agentxs.textualmanagement.pythonagent import PythonOptions
from agentxs.textualmanagement.postgresqlagent import PostgreSQLOptions


class WaitingModal(ModalScreen):
    def compose(self):
        yield LoadingIndicator()


class TextualAgentUI(App):
    CSS_PATH = "assets/agent.tcss"

    def __init__(self, *args, agent_option: Literal["python", "postgres"] = "python", **kwargs):
        super().__init__(*args, **kwargs)

        if agent_option == "python":
            from agentxs.myagents.pythonagent import python_agent as agent
        elif agent_option == "postgres":
            from agentxs.myagents.postgresagent import postgres_agent as agent
        self.agent = agent

    def compose(self) -> ComposeResult:
        with Horizontal():
            # Left aside with options
            with Container(id="sidebar"):
                yield Static("Agent settings", classes="title")

                with Container(classes="scrollable"):
                    yield CommonOptions(self.agent)
                    if self.agent.agent.name == "Python agent":
                        yield PythonOptions()
                    elif self.agent.agent.name == "PostgreSQL agent":
                        yield PostgreSQLOptions()

            # Main content area
            with Vertical(id="main-content"):
                self._dialog_container = Container(classes="scrollable", id="dialog_container")
                yield self._dialog_container
                with Container(id="input-container"):
                    self._text_area = TextArea(tooltip="Type here...")
                    yield self._text_area
                    yield Button("Submit", variant="primary", id="submit_btn")

    @on(message_type=Button.Pressed, selector="#submit_btn")
    async def submit_handler(self):
        """
        Submit button handler.
        Shows a loading indicator, asks the agent and shows the result to _dialog_container.
        :return:
        """
        question = self._text_area.text.strip()
        if not question:
            return

        loading_indicator = LoadingIndicator()
        await self._dialog_container.mount(loading_indicator)
        answer = await self.agent.ask_agent(input=question)

        label = Label(question, classes="dialog user")
        label.border_title = "You"
        await self._dialog_container.mount(label)
        self._dialog_container.scroll_end(speed=7)
        await loading_indicator.remove()
        markdown = Markdown(answer, classes="dialog model")
        markdown.border_title = "Agent"
        await self._dialog_container.mount(markdown)
        self._text_area.text = ""
        self._text_area.focus()

    async def on_mount(self) -> None:
        self._text_area.focus()

    def clear_dialog(self):
        """Removes all children from _dialog_container"""
        [children.remove() for children in self._dialog_container.children]

    def load_historical(self):
        self.clear_dialog()
        for interaction in self.agent.historical:
            role = interaction.get("role")
            content = interaction.get("content")
            widget = None
            if role is not None and content is not None:
                if role == "user":
                    widget = Label(content, classes="dialog user")
                    widget.border_title = "You"
                else:
                    widget = Markdown(content, classes="dialog model")
                    widget.border_title = "Agent"
            self._dialog_container.mount(widget)
        self._dialog_container.scroll_end()


if __name__ == "__main__":
    app = TextualAgentUI()
    app.run()


def run_textual(agent: Literal["python", "postgres"]):
    app = TextualAgentUI(agent_option=agent)
    app.run()
