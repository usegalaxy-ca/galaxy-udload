#!/usr/bin/env python3

import argparse
import os
from bioblend import galaxy
from dotenv import load_dotenv
import logging


LOG_LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]


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
        "--filepath",
        default=os.getcwd(),
        help="Output directory or file name to write to.",
    )

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Enable verbosity"
    )

    return parser


def download_dataset(dc, dataset_id, filepath):
    """Download dataset to disk at file path."""
    logging.info(
        f"Downloading dataset with id `{dataset_id}` at {os.path.relpath(filepath)}"
    )
    dc.download_dataset(
        dataset_id=dataset_id,
        file_path=filepath,
        use_default_filename=os.path.isdir(filepath),
    )


if __name__ == "__main__":
    # parse cli arguments
    args = create_argparser().parse_args()

    # read .env and set environment if envfile exists
    load_dotenv(args.envfile)

    logging.basicConfig(level=LOG_LEVELS[min(args.verbose, len(LOG_LEVELS) - 1)])

    if args.ask_api_key:
        from getpass import getpass

        logging.debug("Asking UseGalaxy API key.")
        os.environ["GALAXY_API_KEY"] = getpass("UseGalaxy API key: ")
        logging.debug("Setting GALAXY_API_KEY variable.")

    if args.url:
        os.environ["GALAXY_URL"] = args.url
        logging.debug("Set GALAXY_URL variable.")

    gi = galaxy.GalaxyInstance(
        url=os.environ["GALAXY_URL"],
        key=os.environ["GALAXY_API_KEY"],
    )
    dc = galaxy.datasets.DatasetClient(gi)

    if args.dataset_id:
        download_dataset(dc, args.dataset_id, args.filepath)
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
            download_dataset(dc, dataset["id"], args.filepath)
