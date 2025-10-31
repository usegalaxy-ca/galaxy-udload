#!/usr/bin/env python3

import argparse
import os
import yaml
from bioblend import galaxy
from dotenv import load_dotenv


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
        default='.env',
        help="Configuration environment file",
    )

    parser.add_argument(
        "--ask-api-key",
        default=False,
        action='store_true',
        help='Prompt for Galaxy API key'
    )

    parser.add_argument(
        "--url",
        default=None,
        help='Galaxy URL endpoint'
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
        "--filepath",
        default=os.getcwd(),
        help="Output directory or file name to write to.",
    )

    return parser


def download_dataset(dc, dataset_id, filepath):
    """Download dataset to disk at file path."""
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

    if args.ask_api_key:
        from getpass import getpass
        os.environ["GALAXY_API_KEY"] = getpass("UseGalaxy API key: ")

    if args.url:
        os.environ["GALAXY_URL"] = arg.url

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
