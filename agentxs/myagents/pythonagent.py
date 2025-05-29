from agents import Agent, TResponseInputItem, Runner, RunResult

from agentxs.myagents import customfiletools
from agentxs.myagents.agentwrapper import AgentWrapper, AgentMemory, AgentWrapperContext

python_agent = AgentWrapper(
    agent=Agent(
        name="Python agent",
        instructions="You provide help about python programming. Your answers are based on best practices for clean "
                     "code, security and good architecture. Use the given tools when the user asks for code that can "
                     "be in a file.",
        model="gpt-4o-mini",  # "gpt-4.1"
        tools=[customfiletools.get_available_files,
               customfiletools.get_paths_from_filename,
               customfiletools.get_file_content]
    ),
    agent_memory=AgentMemory.NONE,
    context=AgentWrapperContext(available_extensions=(".py",))
)
