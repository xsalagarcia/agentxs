import re

from rich.console import Console
from rich.markdown import Markdown

from agentxs.myagents.agentwrapper import AgentWrapper, AvailableModels, AgentMemory

console = Console()


def request_user_reply(message: str = "\nYour question (empty reply will finish; type help for help): ") -> str:
    return console.input(f"[bold red]{message}[/bold red]").strip()


def save_thread(user_input: str, agent: AgentWrapper) -> str:
    matches = re.match(
        r'(?P<command>/save_thread)\s+"(?P<thread_name>[\w\s.,]+)"\s+"(?P<thread_description>[\w\s.,]+)"', user_input)
    if matches is None:
        console.print("Couldn't understand the order. Ensure you type the thread name and description in double "
                      "quotes each one.")
    else:
        agent.save_historical(name=matches.group("thread_name"), description=matches.group("thread_description"))
        console.print("Thread saved!")
    return request_user_reply()


def clear_thread(_, agent: AgentWrapper) -> str:
    agent.clear_historical()
    console.print("Thread cleared. The agent don't remember previous chat.")
    return request_user_reply()


def show_saved_threads(_, agent: AgentWrapper) -> str:
    saved_historical = agent.list_saved_historical()
    options = set()
    saved_threads = ""
    for historical in saved_historical:
        saved_threads += f"- {historical.id:4}: **{historical.name}** -> {historical.description}\n"
        options.add(historical.id)
    console.print(Markdown(saved_threads))
    user_input = input(
        "\nSelect one thread typing the number or continue the chat (i.e: `1`) or remove the chat using `-n` (i.e: `-1`), : ")
    try:
        option = int(user_input)
        if option in options:
            agent.load_historical(id=option)
            console.print("New thread loaded!", style="bold red")
            for interaction in agent.historical:
                role = interaction.get("role")
                content = interaction.get("content")
                if role is not None and content is not None:
                    console.print(
                        f"[{'bold red]Your reply:[/bold red' if role == 'user' else 'bold magenta]Assistant:[/bold magenta'}]")
                    console.print(Markdown(content))
            return request_user_reply()
        elif option * -1 in options:
            agent.delete_saved_historical(id=option * -1)
            console.print("Deleted {")
        else:
            console.print("\nThread id not available.")
    except ValueError:
        return user_input
    return request_user_reply()


def show_model(_, agent: AgentWrapper) -> str:
    print(f"Used model is {agent.current_model}")
    return request_user_reply()


def show_models_list(_, ) -> str:
    print(AvailableModels.get_help())
    return request_user_reply()


def set_model(user_input: str, agent: AgentWrapper) -> str:
    matches = re.match(r'(?P<command>/set_model)\s+"(?P<model>[\w-]+)"', user_input)
    if matches is None:
        console.print("Couldn't understand the order. Ensure you type the path in double quotes.")
    else:
        model = matches.group("model")
        try:
            agent.current_model = AvailableModels(model)
        except ValueError:
            new_input = request_user_reply(
                "Your proposed model is not in the list. Type `yes` to confirm. Otherwise, continue chatting: ")
            if new_input.lower() == "yes":
                agent.current_model = model
                console.print(f"New model has been set: {model}")
            else:
                return new_input

    return request_user_reply()


def show_agent_memory(_, agent: AgentWrapper) -> str:
    print(f"Used model is {agent.agent_memory}")
    return request_user_reply()


def show_agent_memory_options(_) -> str:
    print(AgentMemory.get_help())
    return request_user_reply()


def set_agent_memory(user_input: str, agent: AgentWrapper) -> str:
    matches = re.match(r'(?P<command>/set_model)\s+"(?P<memory>[\w-]+)"', user_input)
    if matches is None:
        console.print("Couldn't understand the order. Ensure you type the path in double quotes.")
    else:
        memory = matches.group("memory")
        try:
            agent.agent_memory = AgentMemory(memory)
            console.print(f"The agent now is set to {memory} mode.")
        except ValueError:
            console.print(f'"{memory}" is not an available option')

    return request_user_reply()


options = {
    "/save_thread": {
        "function": save_thread,
        "text": """- Type `/save_thread "<thread-name>" "<thread-description>"` for saving the current thread. i.e. `/save_thread "my thread" "This is the description"`."""
    },
    "/clear_thread": {
        "function": clear_thread,
        "text": """- Type `/clear_thread` to clean the thread memory."""
    },
    "/show_saved_threads": {
        "function": show_saved_threads,
        "text": """- Type `/show_saved_threads` to list (and pick a saved thread to watch it or continue)."""
    },
    "/show_model": {
        "function": show_model,
        "text": """- Type `/show_model` for getting the used model."""
    },
    "/show_models_list": {
        "function": show_models_list,
        "text": """- Type `/show_models_list` for getting some suggested models."""
    },
    "/set_model": {
        "function": set_model,
        "text": """- Type `/set_model "<model>"` for setting the model (Could be one of the models list, but also other compatibles)."""
    },
    "/show_agent_memory": {
        "function": show_agent_memory,
        "text": """- Type `/show_agent_memory` for getting the agent memory mode."""
    },
    "/show_agent_memory_options": {
        "function": show_agent_memory_options,
        "text": """- Type `/show_agent_memory_options` for getting agent memory modes available."""
    },
    "/set_agent_memory": {
        "function": set_agent_memory,
        "text": """- Type `/set_agent_memory "<option>"` for setting the agent memory mode."""
    }
}
