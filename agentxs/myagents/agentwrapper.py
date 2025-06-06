from dataclasses import dataclass
from enum import StrEnum, Enum
from pathlib import Path
from typing import Any

from agents import Agent, Runner, AgentsException
from openai import BadRequestError

from agentxs.service import historical as historical_service


class AgentMemory(StrEnum):
    NONE = "none"
    JUST_ANSWERS = "just_answers"
    WHOLE_MEMORY = "whole_memory"

    __descriptions = {
        NONE: "The agent operates without remembering previous interventions.",
        JUST_ANSWERS: "The agent operates remembering user text and agent definitive answer for each turn.",
        WHOLE_MEMORY: "The agent operates remembering user text and the whole agent result for each turn (i.e. Function calling and their results are incorporated)."
    }

    @property
    def description(self):
        return self.__descriptions[self]  # AgentMemory.NONE.description will return the description.

    @classmethod
    def get_help(cls) -> str:
        help = "Options are:\n"
        for option in AgentMemory:
            help += f'- "{option}": {option.description}\n'
        return help


class AvailableModels(StrEnum):
    GPT_4_1 = "gpt-4.1"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_1_MINI = "gpt-4.1-mini"
    CODEX_MINI_LATEST = "codex-mini-latest"

    __descriptions = {
        GPT_4_1: "Flagship GPT model for complex tasks. Input: Text | Image. Output: Text. https://platform.openai.com/docs/models/gpt-4.1",
        GPT_4O_MINI: "Fast and cheap. Input: Text | Image. Output: Text. https://platform.openai.com/docs/models/gpt-4o-mini",
        GPT_4_1_MINI: "Balanced for intelligence, speed and cost. Input: Text | Image. Output: Text. https://platform.openai.com/docs/models/gpt-4.1-mini",
        CODEX_MINI_LATEST: "Fast reasoning model optimized for the Codex CLI. Input: Text | Image. Output: Text. https://platform.openai.com/docs/models/codex-mini-latest"
    }

    @property
    def description(self):
        return self.__descriptions[self]

    @classmethod
    def get_help(cls) -> str:
        help = "Some registered options are:\n"
        for model in AvailableModels:
            help += f'- "{model}": {model.description}\n'
        help += "But you could type any model string compatible with agents OpenAI API."
        return help


@dataclass
class AgentWrapperContext:
    available_path: str | None = None
    """Root path that allows agent listing and accessing files and directories."""
    available_extensions: tuple[str, ...] | None = None
    """Extensions that agent is allowed to access."""


class AgentWrapper:
    """
    Contains the agent and some functions to manage chat memory and others.
    """

    def __init__(self, agent: Agent, agent_memory: AgentMemory,
                 context: AgentWrapperContext()):
        self.agent = agent
        self.agent_memory = agent_memory
        self.__historical = []
        self.context = context

    async def ask_agent(self, input: str) -> Any:

        self.__historical.append({"role": "user", "content": input})

        try:
            run_result = await Runner.run(starting_agent=self.agent,
                                          input=self.__historical,
                                          context=self.context)
        except BadRequestError | AgentsException as e:
            return f"**{e.message}**"

        match self.agent_memory:
            case AgentMemory.WHOLE_MEMORY:
                self.__historical = run_result.to_input_list()
            case AgentMemory.JUST_ANSWERS:
                self.__historical.append({"role": "assistant", "content": run_result.final_output})
            case AgentMemory.NONE:
                self.__historical.clear()

        return run_result.final_output

    @property
    def historical(self) -> list:
        """
        List that contains the chat memory.
        :return:
        """
        return self.__historical

    def clear_historical(self):
        self.__historical.clear()

    @property
    def current_model(self) -> str:
        return self.agent.model

    @current_model.setter
    def current_model(self, model: str | AvailableModels):
        self.agent.model = model

    def save_historical(self, name: str, description: str):
        """
        Sends historical to the service layer to be saved.
        :param name:
        :param description:
        :return:
        """
        historical_service.create_historical(agent_name=self.agent.name,
                                             name=name,
                                             description=description,
                                             chat=self.historical)

    def list_saved_historical(self):
        return historical_service.list_historical_by_agent_name(agent_name=self.agent.name)

    def load_historical(self, id: int):
        self.__historical = historical_service.get_historical(id=id)

    @classmethod
    def delete_saved_historical(cls, id: int) -> int:
        return historical_service.delete_saved_historical(id=id)
