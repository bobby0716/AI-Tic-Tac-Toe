"""
AI Tic-Tac-Toe - Main Application Entrypoint
Supports both Desktop GUI and Terminal CLI modes.
"""

import sys
import argparse
from src.gui import launch_gui
from src.cli import play_cli


def main():
    parser = argparse.ArgumentParser(description="AI Tic-Tac-Toe with Minimax Algorithm")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run game in Terminal CLI mode instead of Desktop GUI",
    )
    args = parser.parse_args()

    if args.cli:
        play_cli()
    else:
        launch_gui()


if __name__ == "__main__":
    main()