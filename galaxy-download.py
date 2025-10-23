#!/usr/bin/env python3

import argparse
import os
import yaml
from bioblend import galaxy


def check_exists(path):
    """Check that a given file path exists, or raise an ArgumentTypeError."""
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"Path does not exists: {path}")


def read_configuration(filepath):
    """Read YAML configuration file."""
    with open(filepath) as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {filepath}: {e}")

    return None


def create_argparser():
    """Create the arguments parser."""
    parser = argparse.ArgumentParser(
        prog="galaxy-upload",
        description="UseGalaxy file upload utility.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Positional argument
    parser.add_argument(
        "-c",
        "--config-file",
        type=check_exists,
        default=".config.yaml",
        help="Configuration file",
    )

    # parser.add_argument(
    #     "--ask-api-key",
    #     default=None,
    #     help='Prompt for Galaxy API key'
    # )

    # parser.add_argument(
    #     "--url",
    #     default=None,
    #     help='Galaxy URL endpoint'
    # )

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
    args = create_argparser().parse_args()
    config = read_configuration(args.config_file)

    gi = galaxy.GalaxyInstance(
        url=config["GALAXY_URL"],
        key=config["GALAXY_API_KEY"],
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
