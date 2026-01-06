#!/usr/bin/env python3

import argparse
import os
from bioblend import galaxy
from dotenv import load_dotenv
import rich.progress
import re
import sys
import datetime
import rich.table


def create_table(histories=[]):
    """
    Create a Rich table displaying a list of history records.

    Parameters
    ----------
    histories : list of dict, optional
        A list of history objects. Each dictionary is expected to contain:
        - "id": Unique identifier for the record (str)
        - "name": Display name of the record (str)
        - "update_time": ISO‑formatted timestamp string (e.g., "2024-01-15T12:34:56")

    Returns
    -------
    rich.table.Table
        A Rich Table object with columns for ID, name, and last modified time.
    """
    # Table setup
    table = rich.table.Table()
    table.add_column("id", style="cyan", no_wrap=True)
    table.add_column("name", style="green")
    table.add_column("last modified", style="dark_orange")

    # Add rows
    for history in histories:
        table.add_row(history["id"], history["name"], datetime.datetime.fromisoformat(history["update_time"]).strftime("%Y-%m-%d %H:%M:%S"))

    return table


def history_exists(gi, history_id):
    """
    Check whether a history entry with the given ID exists.

    Parameters
    ----------
    gi : object
        An object that provides access to histories through
        `gi.histories.get_histories()`, which must return an iterable
        of dictionaries containing an "id" field.
    history_id : str
        The ID of the history record to search for.

    Returns
    -------
    bool
        True if a history with the specified ID exists, otherwise False.
    """
    return any(history["id"] == history_id for history in gi.histories.get_histories())


def filter_histories(gi, history_name=None, ignore_case=False):
    """
    Return Galaxy histories whose names match a given pattern.

    Parameters
    ----------
    gi : object
        A GalaxyInstance-like object exposing `gi.histories.get_histories()`.
    history_name : str, optional
        A substring or regular expression to match against history names.
        If None, all histories are returned.
    ignore_case : bool, optional
        If True, matching is case-insensitive.

    Returns
    -------
    list of dict
        Histories whose "name" field matches the pattern.
    """
    histories = gi.histories.get_histories()

    if not history_name:
        return histories

    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(history_name, flags=flags)

    return [history for history in histories if pattern.search(history["name"])]


def handle_find_history(gi, history_name=None, ignore_case=False):
    """
    Locate Galaxy histories and handle ambiguous or missing matches.

    This function searches for histories using `filter_histories` and then
    handles three cases:

    1. **No matches** — prints an error message and exits.
    2. **Multiple matches** — displays a table of histories, prints guidance
       on how to disambiguate, and exits.
    3. **Exactly one match** — returns the matching history.

    Parameters
    ----------
    gi : object
        A GalaxyInstance-like object providing access to histories.
    history_name : str, optional
        A substring or regular expression used to filter history names.
        If None, all histories are considered.
    ignore_case : bool, optional
        If True, performs case-insensitive matching.

    Returns
    -------
    list of dict
        A list containing exactly one matching history. The function will
        terminate the program if zero or multiple histories are found.

    Side Effects
    ------------
    - Prints tables and error messages using `rich.console.Console`.
    - Calls `sys.exit(1)` when no valid single match is found.
    """
    msg = None
    console = rich.console.Console()

    histories = filter_histories(gi, history_name, ignore_case)

    if not histories:
        msg = f"No histories matching [italic yellow]{history_name}[/italic yellow] found!"

    if len(histories) > 1:
        table = create_table(histories=histories)
        console.print(table)

        if not history_name:
            msg = (
                "Multiple histories found!\n"
                "Select one by specifying an id with [italic green]--history-id[/italic green] "
                "or a name with [italic green]--history-name[/italic green]."
            )
        else:
            msg = (
                f"Multiple histories matching [italic yellow]{history_name}[/italic yellow] found!\n"
                "Select one by specifying an id with [italic green]--history-id[/italic green]."
            )

    if msg:
        console.print(f"\n[bold red]ERROR[/bold red]: {msg}")
        sys.exit(1)

    return histories


def create_argparser():
    """
    Create and configure the command‑line argument parser.

    Returns
    -------
    argparse.ArgumentParser
        A fully configured argument parser ready for use by the CLI.
    """
    parser = argparse.ArgumentParser(
        prog="galaxy-history",
        description="UseGalaxy history utility.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-e",
        "--envfile",
        default=".env",
        help="Configuration environment file",
    )

    parser.add_argument(
        "--ask-api-key",
        default=False,
        action="store_true",
        help="Prompt for Galaxy API key",
    )

    parser.add_argument("--url", default=None, help="Galaxy URL endpoint")

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        default=True,
        help="List user histories",
    )

    parser.add_argument(
        "-n",
        "--history-name",
        default=None,
        help="History name to filter on",
    )

    parser.add_argument(
        "--history-id",
        "--check-history-id",
        dest='history_id',
        default=None,
        help="History id to filter on",
    )

    parser.add_argument(
        "-i",
        "--ignore-case",
        default=False,
        action="store_true",
        help="Search for histories by ignoring case",
    )

    parser.add_argument(
        "--recent",
        default=False,
        action="store_true",
        help="Display most recent history (not deleted)",
    )

    return parser


def main(args=create_argparser().parse_args()):
    """
    Entry point.
    """

    # read .env and set environment if envfile exists
    load_dotenv(args.envfile)

    if args.ask_api_key:
        from getpass import getpass
        os.environ["GALAXY_API_KEY"] = getpass("UseGalaxy API key: ")

    if args.url:
        os.environ["GALAXY_URL"] = args.url

    gi = galaxy.GalaxyInstance(
        url=os.environ["GALAXY_URL"],
        key=os.environ["GALAXY_API_KEY"],
    )

    console = rich.console.Console()

    if args.history_id:
        end_msg = "[green]exists[/green]" if history_exists(gi, args.history_id) else "[yellow]does not exists[/yellow]"
        console.print(f"History with id [italic cyan]{args.history_id}[/italic cyan] {end_msg}")
    else:
        histories = []

        if args.recent:
            histories = [gi.histories.get_most_recently_used_history()]

        elif args.list and args.history_name is None:
            histories = filter_histories(gi)  # filter on nothing -> list all

        elif args.history_name:
            histories = filter_histories(gi, args.history_name, args.ignore_case)

        table = create_table(histories)
        console.print(table)


if __name__ == "__main__":
    main()
