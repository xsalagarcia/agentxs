from typing import Literal

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Grid, Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Select, Label, Input, OptionList
from textual.widgets._option_list import Option

from agentxs.myagents.agentwrapper import AgentWrapper, AvailableModels, AgentMemory


class CommonOptions(Container):

    def __init__(self, agent: AgentWrapper):
        super().__init__()
        self.agent = agent

    def compose(self) -> ComposeResult:
        yield Button("Save thread", id="save_thread_btn")
        yield Button("Clear thread", id="clear_thread_btn")
        yield Button("Saved threads", id="saved_threads_btn")
        widget: Select = Select.from_values(values=AvailableModels, value=self.agent.current_model,
                                            allow_blank=False,
                                            id="available_models_select", classes="bordered_option")
        widget.border_title = "Model"
        yield widget
        widget: Select = Select.from_values(values=AgentMemory, value=self.agent.agent_memory, allow_blank=False,
                                            id="agent_memory_select", classes="bordered_option")
        widget.border_title = "Agent memory"
        yield widget

    @on(message_type=Button.Pressed, selector="#save_thread_btn")
    def save_thread(self):
        """
        Save thread button handler.
        :return:
        """

        def manage_result(result: tuple[str] | None):
            """
            Callback for modal dialog. Called when dialog is dismissed.
            :param result: A tuple with name and description. Otherwise, (Cancel pressed), None.
            """
            if result is not None:
                self.agent.save_historical(name=result[0], description=result[1])

        self.app.push_screen(ModalGetNameDesc("Type a name and description"), manage_result)

    @on(message_type=Button.Pressed, selector="#clear_thread_btn")
    def clear_thread(self):
        """
        Clear thread button handler.
        :return:
        """

        def manage_result(result: bool):
            if result:
                self.app.clear_dialog()

        self.app.push_screen(ModalConfirm("Confirm"), manage_result)

    @on(message_type=Button.Pressed, selector="#saved_threads_btn")
    def manage_saved_threads(self):
        """
        Load saved thread.
        :return:
        """

        def manage_result(result: tuple[int, str]):
            if result[1] == "Load":
                self.agent.load_historical(id=result[0])
                self.app.load_historical()
            elif result[1] == "Delete":
                self.agent.delete_saved_historical(id=result[0])

        saved_historical = self.agent.list_saved_historical()
        self.app.push_screen(ModalSelectFromList(message="Select a thread",
                                                 options=[(f"{chat.name}: {chat.description}", chat.id) for chat in
                                                          saved_historical],
                                                 buttons=[("Load", "primary"),
                                                          ("Delete", "warning"),
                                                          ("Cancel", "default")]
                                                 ),
                             manage_result)

    @on(message_type=Select.Changed, selector="#agent_memory_select")
    def change_agent_memory(self, select_changed: Select.Changed):
        self.agent.agent_memory = select_changed.value

    @on(message_type=Select.Changed, selector="#available_models_select")
    def change_agent_model(self, select_changed: Select.Changed):
        self.agent.current_model = select_changed.value

class ModalGetNameDesc(ModalScreen[tuple[str, str] | None]):
    """
    Modal screen for saving the chat. Shows a message, two inputs, accept and cancel buttons.
    """

    def __init__(self, message):
        """
        :param message: Message to show at modal dialog.
        """
        super().__init__(classes="compact_modal")
        self.message = message

    def compose(self):
        yield Vertical(
            Label(self.message),
            Input(placeholder="Thread name", id="modal_get_name_desc_name_input"),
            Input(placeholder="Type a little description...", id="modal_get_name_desc_desc_input"),
            Button("OK", variant="primary", id="ok_modal_get_name_desc_btn"),
            Button("Cancel", id="cancel_modal_get_name_desc_btn")
        )

    @on(message_type=Button.Pressed, selector="#ok_modal_get_name_desc_btn")
    def ok_handler(self):
        """Handler for OK button. If input has a name dismisses the dialog returning name and description."""
        name = str(self.query_one("#modal_get_name_desc_name_input").value)
        if name == "":
            self.notify("Type a name at least!", timeout=2)
            return

        description = str(self.query_one("#modal_get_name_desc_desc_input").value)
        self.dismiss((name, description))

    @on(message_type=Button.Pressed, selector="#cancel_modal_get_name_desc_btn")
    def cancel_handler(self):
        """Handler for Cancel button. Dismisses the dialog returning None."""
        self.dismiss(None)


class ModalConfirm(ModalScreen[bool]):
    """
    Modal screen that shows a message, OK and Cancell buttons. True is returned when is dismissed pressing Accept button.
    """

    def __init__(self, message):
        """

        :param message: Message to show at modal dialog.
        """
        super().__init__(classes="compact_modal")
        self.message = message

    def compose(self):
        yield Vertical(
            Label(self.message),
            Button("OK", variant="primary", id="ok_modal_get_name_desc_btn", action="screen.button_pressed(True)"),
            Button("Cancel", id="cancel_modal_get_name_desc_btn", action="screen.button_pressed(False)")
        )

    def action_button_pressed(self, value_to_return: bool):
        self.dismiss(value_to_return)


class ModalSelectFromList(ModalScreen[tuple[int, str]]):
    def __init__(self, message: str, options: list[tuple[str, int]],
                 buttons: list[tuple[str, Literal["default", "primary", "success", "warning", "error"]]]):
        super().__init__(classes="compact_modal")
        self.options = options
        self.message = message
        self.buttons = buttons

    def compose(self):
        with Vertical():
            yield Label(self.message, classes="title")
            yield OptionList(*[Option(option[0], id=option[1]) for option in self.options])
            with Horizontal():
                for button in self.buttons:
                    yield Button(button[0], action=f"screen.handle_option('{button[0]}')", variant=button[1])

    def action_handle_option(self, option: str):
        ol: OptionList = self.query_one("OptionList")

        self.dismiss((ol.get_option_at_index(ol.highlighted).id, option))

