from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Input, Static, Switch, Label
from agentxs.myagents.postgresagent import postgres_agent


class PostgreSQLOptions(Container):
    def compose(self) -> ComposeResult:
        yield Label("Database settings")
        widget = Input(placeholder="Password", classes="bordered_option", id="password_input", password=True)
        widget.border_title = "Password"
        yield widget
        widget = Input(placeholder="Username", classes="bordered_option", id="username_input")
        widget.border_title = "Username"
        yield widget
        widget = Input(placeholder="host", classes="bordered_option", id="host_input")
        widget.border_title = "Host"
        yield widget
        widget = Input(placeholder="port", classes="bordered_option", id="port_input", type="integer")
        widget.border_title = "Port"
        yield widget
        widget = Input(placeholder="database", classes="bordered_option", id="database_input")
        widget.border_title = "Database"
        yield widget
        widget = Switch(value=postgres_agent.ssl_mode, classes="bordered_option", id="ssl_switch")
        widget.border_title = "SSL mode"
        widget.styles.width = "100%"
        yield widget


    @on(message_type=Input.Submitted)
    @on(message_type=Input.Blurred)
    def set_engine_param(self, event: Input.Submitted | Input.Blurred):
        match event.input.id:
            case "password_input":
                postgres_agent.password = event.value
            case "username_input":
                postgres_agent.username = event.value
            case "host_input":
                postgres_agent.host = event.value
            case "port_input":
                postgres_agent.port = event.value
            case "database_input":
                postgres_agent.database = event.value
        if postgres_agent.has_db_engine:
            if postgres_agent.test_db_engine():
                self.notify("Engine instantiated and connection working!")

            else:
                self.notify("Engine instantiated but connection not working!\nReview params")

