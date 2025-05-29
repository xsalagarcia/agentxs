import logging
import os
from pathlib import Path

from agents import function_tool, RunContextWrapper

from agentxs.myagents.agentwrapper import AgentWrapperContext

logger = logging.getLogger(__name__)


def _get_available_files_impl(context: AgentWrapperContext) -> list[str]:
    """Necessary for testing"""
    result = []
    if context.available_path is None:
        return result

    for dirpath, _, filenames in os.walk(context.available_path):
        for filename in filenames:
            if filename.endswith(context.available_extensions):
                result.append(str(Path(dirpath).relative_to(context.available_path).joinpath(filename)))
    return result


@function_tool
def get_available_files(ctx: RunContextWrapper[AgentWrapperContext]) -> list[str]:
    """
    Returns the whole list of paths representing all available files to study their contents if necessary.
    :return:
    """
    logging.info("Accessing to get_available_files.")
    return _get_available_files_impl(ctx.context)


def _get_file_content_impl(path: str) -> str:
    with open(path) as file:
        return file.read()


@function_tool
def get_file_content(ctx: RunContextWrapper[AgentWrapperContext], path: str) -> str:
    """
    Returns the content of the file.
    :param path: The path to the file.
    :return:
    """
    logging.info(f"Accessing to get_file_content with path: {path}.")
    return _get_file_content_impl(path=path)


def _get_paths_from_filename_impl(context: AgentWrapperContext, filename: str) -> list[str]:
    return [str(file) for file in Path(context.available_path).rglob(filename) if
            str(file).endswith(context.available_extensions) and file.is_file()]


@function_tool
def get_paths_from_filename(ctx: RunContextWrapper[AgentWrapperContext], filename: str) -> list[str]:
    """Given a filename or pattern returns a list of available paths that match it."""
    logging.info(f"Accessing to get_paths_from_filename with filename: {filename}.")
    logging.info(f"available path is {ctx.context.available_path}")
    return _get_paths_from_filename_impl(context=ctx.context, filename=filename)
