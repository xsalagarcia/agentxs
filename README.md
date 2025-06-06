
# Intro Agentxs

This is a simple agent wrapper for playing with openai-agents library. Contains
two examples that create an agent to help with python projects or PostgreSQL database.

The agent wrappers are defined in `agentxs.myagents` package. This package contains modules
that defines tools for the agents and two agent wrappers.
- `agentwrapper.py` module contains `AgentWrapper` class that interacts with agent and allows some
extra functionalities such as memory management or save-load-delete chats in a local storage.
- `postgresagent.py` module contains a subclass of `AgentWrapper`, `PostgresAgentWrapper` with specific
management of postgres connection. Agent never sees connection parameters, and only can have access to
the specified tools (database exploring mainly).
- `pythonagent.py` module manages the python agent directly using `AgentWrapper`, just passing specific
instructions and tools. To use the tools, is necessary to set the project path and the available file
extensions.

In any case, the connection for postgres agent or the path and file extensions are set in agent context.
Agent context is never sent to the LLM (OpenAI agents library doc).

## About the run context

The [run context](https://openai.github.io/openai-agents-python/ref/run_context/) is set into the AgentWrapper object,
and can be modified anytime. This can be, as openai agents docs says, any dependency or data that never is sent to
the LLM, is only passed to functions, callbacks, hooks. 

When a function tool is called and the first argument is `ctx: RunContextWrapper[Any]` the context is passed. The
context object can be retrieved referencing the context attribute (`ctx.context`).

# API Key and available models

The module `agentxs.settings.settings` tries to read a `.env` file at the root of the project that should
contain something like this:

```python
API_KEY_OPENAI = sk-proj-thisistheapikeyblahblahblah...
```

If this file (`.env`) doesn't exist, an environment variable `API_KEY_OPENAI` should exist. `.env_sample` shows 
how `.env` should be.

OpenAI API key is set in `agentxs.myagents.__init__.py`, and the used model is set when `agents.Agent` is
instantiated at `agentxs.myagents` package, on modules `postgresagent.py` or `pythonagent.py`, when `postgres_agent`
or `python_agent` are created. This can be changed there or while using the agent wrapper. A list of suggested
models is in `agentxs.myagents.agentwrapper.py` module, at `AvailableModels` enum. But can be changed using other
OpenAI compatible strings (adding this strings in `AvailableModels` enum is a good idea).

Other models than OpenAI can be added using
[LiteLLM](https://openai.github.io/openai-agents-python/models/litellm/).

# UI

## CLI agents: cli_python_agent.py and cli_postgres_agent.py

This is just experimental. It's better to use [CLI Textual agents](#cli-textual-agents-textual_agentpy-through-console-script).

A very basic CLI is available through these modules (`agentxs.cli_python_agent.py` and `cli_postgres_agent.py`).

If run cli_postgres_app.py or cli_python_agent.py without activating virtual environment is wanted, with
the virtual environment activated install the package in dev mode (`pip install -e .`)
and insert the shebang line pointing to the python runner at virtual environment. When these modules are called,
cli params and flags can be used.

Once the package is installed (i.e. in dev mode with `pip install -e .`),
you can run this module like this:

```shell
agentxs_cli {python | postgres}
```

## CLI Textual agents: textual_agent.py through console script

This module (`agentxs.textual_agent.py`) uses a more evolved non-graphical UI through 
[textual library](https://textual.textualize.io/). When the app class (`TextualAgentUI`) is instantiated 
an option

Once the package is installed (i.e. in dev mode with `pip install -e .`),
you can run this module using some of these options:

```shell
agentxs {pyton | postgres}
```
or 
```shell
python -m agentxs {python | postgres}
```

### Select, copy, paste on textual UI

When textual UI is running some problems can appear when you try to select and copy text. The solution is posted 
[here](https://textual.textualize.io/FAQ/#how-can-i-select-and-copy-text-in-a-textual-app). That is, i.e. in
Gnome Terminal just use the mouse holding SHIFT key to select and copy text.

# Installing the package

## As application

You can use [`pipx`](https://pipx.pypa.io/stable/) to install the package if only calls to entry points are
desired, even with the url of the repo.

## As dev mode

Or you can clone the repo, create the virtual environment and add the dependencies listed on `requirements.txt`, and 
for running entry points install the package in dev mode (`pip install -e .`)

