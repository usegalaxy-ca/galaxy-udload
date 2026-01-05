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
    return any(history["id"] == history_id for history in gi.histories.get_histories())


def filter_histories(gi, history_name=None, ignore_case=False):
    pattern = None
    if history_name:
        flags = re.IGNORECASE if ignore_case else 0
        pattern = re.compile(history_name, flags=flags)

    return [
        history
        for history in gi.histories.get_histories()
        if not history_name or pattern.search(history["name"])
    ]


def handle_find_history(gi, history_name=None, ignore_case=False):
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
    """Create the arguments parser."""
    parser = argparse.ArgumentParser(
        prog="galaxy-history",
        description="UseGalaxy history utility.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Positional argument
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
        help='Search for histories by ignoring case'
    )

    parser.add_argument(
        "--recent",
        default=False,
        action="store_true",
        help='Display most recent history (not deleted)'
    )

    return parser


def main(args=create_argparser().parse_args()):

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
