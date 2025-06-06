"""
Entry point for textual interface.
"""

import argparse
from agentxs.textual_agent import run_textual

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
    run_textual(agent=args.agent)

if __name__ == "__main__":
    main()