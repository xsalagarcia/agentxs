import asyncio
from pathlib import Path

import typer
from rich.markdown import Markdown
from rich.progress import TextColumn, Progress, SpinnerColumn

from agentxs.consolemanagement.common import console, request_user_reply
from agentxs.consolemanagement.pythonagent import options
from agentxs.myagents.agentwrapper import AgentMemory

from agentxs.myagents.pythonagent import python_agent


def get_help() -> str:
    content = "- Type `help` to show this message.\n"
    for option in options.values():
        content += f'{option.get("text")}\n'
    content += "- Type empty message to exit.\n"
    console.print(Markdown(content))
    return request_user_reply()


def main(user_input: str = typer.Argument(help="Type your question", default="help"),
         project_path: str | None = typer.Option(default=None, help="Path that will be available for agent tools."),
         thread_memory: AgentMemory = typer.Option(default=AgentMemory.JUST_ANSWERS, help=AgentMemory.get_help())):
    #logging.basicConfig(level=logging.INFO)

    python_agent.agent_memory = thread_memory
    assert project_path is None or Path(project_path).is_dir()
    python_agent.context.available_path = project_path

    while user_input != "":
        if user_input.lower() == "help":
            user_input = get_help()
            continue
        try:
            user_input = options[user_input.split()[0]]["function"](user_input, python_agent)
            continue
        except KeyError:
            pass
        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
        ) as progress:
            progress.add_task(description="waiting for the agent...", total=None)
            answer = asyncio.run(python_agent.ask_agent(input=user_input))
        console.print(Markdown(answer))

        user_input = request_user_reply()


if __name__ == "__main__":
    typer.run(main)

def run_typer():
    main(user_input="help", project_path=None, thread_memory=AgentMemory.JUST_ANSWERS)