"""Entry point for cli agents (rich)"""

import argparse

from agentxs import cli_postgres_agent, cli_python_agent


def main():
    parser = argparse.ArgumentParser(
        prog="textualRunner",
        description="Use it for running textual UI"
    )
    subparsers = parser.add_subparsers(dest="agent", required=True,
                                       help="Type the option for running a textual UI.")
    subparsers.add_parser("python", help="Runs python agent in textual UI.")
    subparsers.add_parser("postgres", help="Runs PostgreSQL agent in textual UI.")

    args = parser.parse_args()
    match args.agent:
        case "python":
            cli_python_agent.run_typer()
        case "postgres":
            cli_postgres_agent.run_typer()

