import argparse
import os
import sys

import rich.console
from rich.progress import track

from .dataset import (
    DatasetNotFoundError,
    filter_datasets,
)


class DownloadError(Exception):
    """Raised when an error occured on download."""


def register_subcommand(subparser):
    """Create the arguments parser."""
    parser = subparser.add_parser(
        name="download",
        description="UseGalaxy file download utility.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--history-id",
        default=None,
        help="History id to download datasets from.",
    )

    parser.add_argument(
        "--dataset-id",
        default=None,
        help="Dataset id to download",
    )

    parser.add_argument(
        "--dataset-name",
        default=None,
        help="Dataset name (regex) to filter on",
    )

    parser.add_argument(
        "--path",
        default=os.getcwd(),
        help="Output directory or file name to write to.",
    )

    parser.add_argument(
        "-i",
        "--ignore-case",
        default=False,
        action="store_true",
        help="Search for datasets ignoring case",
    )

    parser.set_defaults(func=handle_download)

    return parser


def download_dataset(gi, dataset_id, path):
    """Download dataset to disk at file path."""
    print("Downloading:", gi.datasets.show_dataset(dataset_id)['name'])
    gi.datasets.download_dataset(
        dataset_id=dataset_id,
        file_path=path,
        use_default_filename=os.path.isdir(path),
    )


def handle_download(args):
    """Main section, to be called as main script, or callable script."""

    console = rich.console.Console()

    try:
        if args.dataset_id:
            # Single dataset download by id
            download_dataset(args.gi, args.dataset_id, args.path)

        elif args.dataset_name:
            # Single dataset by name, or multiple by regex
            datasets = filter_datasets(args.gi, args.dataset_name, args.ignore_case, args.history_id)

            if not datasets:
                raise DatasetNotFoundError(args.dataset_name)

            for dataset in track(datasets, description="Downloading matching datasets"):
                download_dataset(args.gi, dataset['id'], args.path)

        elif args.history_id:
            # Download all datasets from history
            datasets = filter_datasets(args.gi, ignore_case=args.ignore_case, history_id=args.history_id)

            if not datasets:
                raise DownloadError(f"No datasets found for the given history [italic yellow]{args.history_id}[/italic yellow].")
          
            for dataset in track(datasets, description="Downloading history datasets"):
                download_dataset(args.gi, dataset['id'], args.path)

    except (DownloadError, DatasetNotFoundError) as ex:
        console.print(f"\n[bold red]ERROR[/bold red]: {ex}")
        sys.exit(1)




