#!/usr/bin/env python3

import argparse
import os
from bioblend import galaxy, ConnectionError
from dotenv import load_dotenv
import rich.progress
from tusclient.fingerprint import fingerprint
import rich.table
from .history import filter_histories, create_table, HistoryAmbiguousError, HistoryNotFoundError
import sys


def progress_bar(file, total=None):
    """Create a progress bar for the current transfer."""
    bar = rich.progress.Progress(
        rich.progress.TextColumn("[progress.description]{task.description}"),
        rich.progress.BarColumn(),
        rich.progress.DownloadColumn(),
        rich.progress.TransferSpeedColumn(),
        rich.progress.TextColumn("eta"),
        rich.progress.TimeRemainingColumn(),
    )

    task_id = bar.add_task(file, total=total)

    return bar, task_id


def create_argparser():
    """Create the arguments parser."""
    parser = argparse.ArgumentParser(
        prog="galaxy-upload",
        description="UseGalaxy file upload utility.",
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
        "--history-id",
        default=None,
        help="History id to filter on",
    )

    parser.add_argument(
        "--history-name",
        default=None,
        help="History name to filter on",
    )

    parser.add_argument(
        "-i",
        "--ignore-case",
        default=False,
        action="store_true",
        help='Search for histories by ignoring case'
    )

    parser.add_argument(
        "--file",
        nargs="+",
        required=True,
        help="Input files path to upload.",
    )

    parser.add_argument(
        "--checkpoints",
        default=os.path.join(os.getcwd(), ".checkpoints"),
        help="Checkpoints file",
    )

    return parser


def upload_file(gi, path, history_id, storage):
    filename = os.path.basename(path)

    try:
        uploader = gi.get_tus_uploader(
            path=path,
            storage=storage,
        )
        filesize = os.path.getsize(path)

        progress, task_id = progress_bar(filename, total=filesize)
        with progress:
            last_offset = 0
            while uploader.offset < filesize:
                uploader.upload_chunk()
                progress.update(task_id, advance=(uploader.offset - last_offset))
                last_offset = uploader.offset

        gi.tools.post_to_fetch(path, history_id, uploader.session_id, auto_decompress=True, file_name=filename)

    except ConnectionError as ex:
        if ex.status_code == 404 and storage:
            with open(storage, "rb") as fh:
                fingerprinter = fingerprint.Fingerprint()
                fp_hash = fingerprinter.get_fingerprint(fh)
            print(
                f"Unable to resume, previous upload may have been removed from server (hint: remove {fp_hash} from {storage} or change storage to reupload from the start: {ex}"
            )
        else:
            print(ex)


def find_history(gi, history_name=None, ignore_case=False):
    """ Find an history based on name."""

    histories = filter_histories(gi, history_name, ignore_case)

    if not histories:
        raise HistoryNotFoundError(history_name)

    if len(histories) > 1:
        raise HistoryAmbiguousError(history_name, histories)

    return histories[0]['id']


def main(args=None):
    """Main section, to be called as main script, or callable script."""

    if not args:
        args = create_argparser().parse_args()

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

    try:
        history_id = args.history_id if args.history_id else find_history(gi, args.history_name, args.ignore_case)
    except HistoryAmbiguousError as ex:
        table = create_table(ex.histories)
        console.print(table)
        console.print(f"\n[bold red]ERROR[/bold red]: {ex}")
        sys.exit(1)

    except HistoryNotFoundError as ex:
        console.print(f"\n[bold red]ERROR[/bold red]: {ex}")
        sys.exit(1)

    for file in args.file:
        if os.path.exists(file):
            upload_file(gi, file, history_id, args.checkpoints)
        else:
            print(f"{file} does not exists...skipping!")


if __name__ == "__main__":
    main()
