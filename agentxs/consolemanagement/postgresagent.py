import re

from agentxs.consolemanagement.common import options as common_options, console, request_user_reply
from agentxs.myagents.postgresagent import PostgresAgentWrapper


def _give_feedback(param_set: str, agent):
    missing_connection_params = agent.get_missing_connection_params()
    console.print(f"Set {param_set}!"
                  f"\n{'No more parameters needed. Engine is set.' if len(missing_connection_params) == 0 else f'There are missing params: {missing_connection_params}'}")


def set_password(_, agent: PostgresAgentWrapper):
    password = console.input("Type the password and press enter: ", password=True)

    agent.password = password
    _give_feedback(param_set="password", agent=agent)
    return request_user_reply()


def set_username(user_input: str, agent: PostgresAgentWrapper):
    matches = re.match(r'(?P<command>/set_username)\s+"(?P<username>.+)"', user_input)
    if matches is None:
        console.print("Couldn't understand the order. Ensure you type the username in double quotes.")
    else:
        agent.username = matches.group("username")
        _give_feedback(param_set="username", agent=agent)
    return request_user_reply()


def get_username(_, agent: PostgresAgentWrapper):
    console.print(f"Username is {agent.username}"
                  if agent.username is not None else "There is no username.")
    return request_user_reply()


def set_host(user_input: str, agent: PostgresAgentWrapper):
    matches = re.match(r'(?P<command>/set_host)\s+"(?P<host>.+)"', user_input)
    if matches is None:
        console.print("Couldn't understand the order. Ensure you type the host in double quotes.")
    else:
        agent.host = matches.group("host")
        _give_feedback(param_set="host", agent=agent)
    return request_user_reply()


def get_host(_, agent: PostgresAgentWrapper):
    console.print(f"Host is {agent.host}"
                  if agent.host is not None else "There is no host.")
    return request_user_reply()


def set_port(user_input: str, agent: PostgresAgentWrapper):
    matches = re.match(r'(?P<command>/set_port)\s+(?P<port>\d+)', user_input)
    if matches is None:
        console.print("Couldn't understand the order. Ensure you type the port as an integer, not double quoted.")
    else:
        agent.port = matches.group("port")
        _give_feedback(param_set="port", agent=agent)
    return request_user_reply()


def get_port(_, agent: PostgresAgentWrapper):
    console.print(f"Port is {agent.port}"
                  if agent.port is not None else "There is no port.")
    return request_user_reply()


def set_database(user_input: str, agent: PostgresAgentWrapper):
    matches = re.match(r'(?P<command>/set_database)\s+"(?P<database>.+)"', user_input)
    if matches is None:
        console.print("Couldn't understand the order. Ensure you type the database name in double quotes.")
    else:
        agent.database = matches.group("database")
        _give_feedback(param_set="database", agent=agent)
    return request_user_reply()


def get_database(_, agent: PostgresAgentWrapper):
    console.print(f"Database is {agent.database}"
                  if agent.database is not None else "There is no database.")
    return request_user_reply()


options = common_options | {
    "/set_password": {
        "function": set_password,
        "text": """- Type `/set_password <password>"` for setting the password for creating a database connection."""
    },
    "/set_username": {
        "function": set_username,
        "text": """- Type `/set_username "<username>"` for setting the username for creating a database connection."""
    },
    "/get_username": {
        "function": get_username,
        "text": """- Type `/get_username` to watch the set username for the database connection."""
    },
    "/set_host": {
        "function": set_host,
        "text": """- Type `/set_host "<host>"` for setting the host for creating a database connection."""
    },
    "/get_host": {
        "function": get_host,
        "text": """- Type `/get_host` for watching the host for the database connection."""
    },
    "/set_port": {
        "function": set_port,
        "text": """- Type `/set_port <n>` for setting the port for creating a database connection."""
    },
    "/get_port": {
        "function": get_port,
        "text": """- Type `/get_port` for watching the port for the database connection."""
    },
    "/set_database": {
        "function": set_database,
        "text": """- Type `/set_database <database-name>` for setting the database name for creating a database connection."""
    },
    "/get_database":  {
        "function": get_database,
        "text": """- Type `/get_database` for watching the database name for the database connection."""
    }
}
