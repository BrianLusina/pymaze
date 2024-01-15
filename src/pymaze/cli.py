"""
Defines the CLI command arguments
"""
import sys
import argparse
from argparse import Namespace


def get_command_line_args() -> Namespace:
    """
    Creates a parser and adds arguments for the parser returning the namespace for the argument parser to use in a CLI
    Returns:
        Namespace: populated namespace object
    """
    parser = argparse.ArgumentParser(
        prog="pytree",
        description="Gets weather and temperature information for a city",
        epilog="Thank you for using PyTree CLI",
    )

    # Argument to get the version name
    parser.add_argument(
        "-v",
        "--version",
        action="version",
    )

    # Argument to get the directory name
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        type=str,
        default=".",
        help="Generate full directory tree starting at ROOT_DIR",
    )

    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="Generate a directory-only tree",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        nargs="?",
        default=sys.stdout,
        help="Generate a full directory tree and save it to a file",
    )

    return parser.parse_args()
