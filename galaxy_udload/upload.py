#!/usr/bin/env python3

import argparse
import os
from bioblend import ConnectionError
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


def register_subcommand(subparser):
    """Create the arguments parser."""
    parser = subparser.add_parser(
        name="upload",
        description="UseGalaxy file upload utility.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

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

    parser.set_defaults(func=handle_upload)

    return parser


def upload_file(gi, path, history_id, storage):
    filename = os.path.basename(path)

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


def find_history(gi, history_name=None, ignore_case=False):
    """ Find an history based on name."""

    histories = filter_histories(gi, history_name, ignore_case)

    if not histories:
        raise HistoryNotFoundError(history_name)

    if len(histories) > 1:
        raise HistoryAmbiguousError(history_name, histories)

    return histories[0]['id']


def handle_upload(args):
    """Main section, to be called as main script, or callable script."""

    console = rich.console.Console()

    try:
        history_id = args.history_id if args.history_id else find_history(args.gi, args.history_name, args.ignore_case)
    except HistoryAmbiguousError as ex:
        table = create_table(ex.histories)
        console.print(table)
        console.print(f"\n[bold red]ERROR[/bold red]: {ex}")
        sys.exit(1)

    except HistoryNotFoundError as ex:
        console.print(f"\n[bold red]ERROR[/bold red]: {ex}")
        sys.exit(1)

    try:
        for file in args.file:
            if os.path.exists(file):
                upload_file(args.gi, file, history_id, args.checkpoints)
            else:
                console.print(f"[italic yellow]{file}[/italic yellow] does not exists...skipping!")
    except ConnectionError as ex:
        if ex.status_code == 404 and args.checkpoints:
            with open(args.checkpoints, "rb") as fh:
                fingerprinter = fingerprint.Fingerprint()
                fp_hash = fingerprinter.get_fingerprint(fh)
            console.print(
                f"Unable to resume, previous upload may have been removed from server (hint: remove {fp_hash} from {args.checkpoints} or change storage to reupload from the start: {ex}"
            )
        else:
            console.print(ex)
