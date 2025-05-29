import re
from pathlib import Path

from agentxs.consolemanagement.common import options as common_options, console, request_user_reply
from agentxs.myagents.agentwrapper import AgentWrapper


def set_path(user_input: str, agent: AgentWrapper) -> str:
    matches = re.match(r'(?P<command>/set_path)\s+"(?P<path>[\w\s./\\-]+)"', user_input)
    if matches is None:
        console.print("Couldn't understand the order. Ensure you type the path in double quotes.")
    else:
        path = Path(matches.group("path"))
        if path.is_dir():
            agent.context.available_path = str(path)
            console.print("Path set!")
        else:
            console.print("The path is not a directory.")
    return request_user_reply()


def get_path(_, agent: AgentWrapper) -> str:
    console.print(f"The set path is {agent.context.available_path}"
                  if agent.context.available_path is not None else "There is no available path.")
    return request_user_reply()


def set_file_extensions(user_input, agent: AgentWrapper) -> str:
    matches = re.match(r'(?P<command>/set_file_extensions)\s+\((?P<extensions>[\w\s.,]+)\)', user_input)
    try:
        extensions = tuple(re.split(r",\s+", matches.group("extensions")))
        agent.context.available_extensions = extensions
        console.print(f"Available extensions set to {extensions}")
    except AttributeError:
        console.print("Couldn't understand the order. Ensure file extensions are in parenthesis and coma separated.")
    return request_user_reply()


def get_file_extensions(_, agent: AgentWrapper) -> str:
    console.print(f"The set file extensions are {agent.context.available_extensions}")
    return request_user_reply()


options = common_options | {
    "/set_path": {
        "function": set_path,
        "text": """- Type `/set_path "<absolute-path>"` for setting the directory which the agent can access. i.e. `/set_path "/home/user/projects/my-project"`."""
    },
    "/get_path": {
        "function": get_path,
        "text": """- Type `/get_path` to watch the set path which the agent can access."""
    },
    "/set_file_extensions": {
        "function": set_file_extensions,
        "text": """- Type `/set_file_extensions (.ext1, ...)` for setting file extensions which the agent can access. i.e.: `/set_file_extensions (.py, .txt, .ini)`."""
    },
    "/get_file_extensions": {
        "function": get_file_extensions,
        "text": """- Type `/get_file_extensions` for getting file extensions which the agent can access."""
    },
}