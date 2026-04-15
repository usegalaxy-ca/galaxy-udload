#!/usr/bin/env python3

import argparse
import os
from bioblend import galaxy
from dotenv import load_dotenv
from . import upload, download, history, dataset


def create_argparser():
    """Create the arguments parser."""
    parser = argparse.ArgumentParser(
        prog="galaxy",
        description="UseGalaxy file upload download utility.",
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

    parser.add_argument(
        "--url",
        default=None,
        help="Galaxy URL endpoint"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    upload.register_subcommand(subparsers)
    download.register_subcommand(subparsers)
    history.register_subcommand(subparsers)
    dataset.register_subcommand(subparsers)

    return parser


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

    args.gi = galaxy.GalaxyInstance(
        url=os.environ["GALAXY_URL"],
        key=os.environ["GALAXY_API_KEY"],
    )

    args.func(args) # call subcommand


if __name__ == "__main__":
    main()
