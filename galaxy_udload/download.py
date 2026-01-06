#!/usr/bin/env python3

import argparse
import os
from bioblend import galaxy
import logging


LOG_LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]


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
        help="History id to filter on",
    )

    parser.add_argument(
        "--dataset-id",
        default=None,
        help="Dataset id to filter on",
    )

    parser.add_argument(
        "--dataset-name",
        default=None,
        help="Exact dataset name to filter on",
    )

    parser.add_argument(
        "--path",
        default=os.getcwd(),
        help="Output directory or file name to write to.",
    )

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Enable verbosity"
    )

    parser.set_defaults(func=handle_download)

    return parser


def download_dataset(dc, dataset_id, path):
    """Download dataset to disk at file path."""
    logging.info(
        f"Downloading dataset with id `{dataset_id}` at {os.path.relpath(path)}"
    )
    dc.download_dataset(
        dataset_id=dataset_id,
        file_path=path,
        use_default_filename=os.path.isdir(path),
    )


def handle_download(args):
    """Main section, to be called as main script, or callable script."""
    dc = galaxy.datasets.DatasetClient(args.gi)

    if args.dataset_id:
        download_dataset(dc, args.dataset_id, args.path)
    elif args.dataset_name:
        # get a list of recent datasets, filtered on given name, and history (if provided)
        datasets = dc.get_datasets(
            name=args.dataset_name,
            history_id=args.history_id,
            visible=True,
            deleted=False,
            purged=False,
            state="ok",
        )

        for dataset in datasets:
            download_dataset(dc, dataset["id"], args.path)
