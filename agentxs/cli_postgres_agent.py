#!/home/xevi/Documents/Projectes/cli-llm/venv/bin/python
import logging
import re
from pathlib import Path

import typer
from rich.markdown import Markdown
from rich.progress import TextColumn, Progress, SpinnerColumn

from agentxs.consolemanagement.common import console, request_user_reply
from agentxs.consolemanagement.postgresagent import options
from agentxs.myagents.agentwrapper import AgentMemory

from agentxs.myagents.postgresagent import postgres_agent


def get_help() -> str:
    content = "- Type `help` to show this message.\n"
    for option in options.values():
        content += f'{option.get("text")}\n'
    content += "- Type empty message to exit.\n"
    console.print(Markdown(content))
    return request_user_reply()


def main(user_input: str = typer.Argument(help="Type your question", default="help"),
         thread_memory: AgentMemory = typer.Option(default=AgentMemory.JUST_ANSWERS, help=AgentMemory.get_help())):
    #logging.basicConfig(level=logging.INFO)

    postgres_agent.agent_memory = thread_memory

    while user_input != "":
        if user_input.lower() == "help":
            user_input = get_help()
            continue
        try:
            user_input = options[user_input.split()[0]]["function"](user_input, postgres_agent)
            continue
        except KeyError:
            pass
        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
        ) as progress:
            progress.add_task(description="waiting for the agent...", total=None)
            answer = postgres_agent.ask_agent(input=user_input)
        console.print(Markdown(answer))

        user_input = request_user_reply()


if __name__ == "__main__":
    typer.run(main)
