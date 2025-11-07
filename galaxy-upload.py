#!/usr/bin/env python3

import argparse
import os
from bioblend import galaxy
from dotenv import load_dotenv
from rich.progress import track
from tusclient.fingerprint import fingerprint


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
        required=True,
        help="History id to filter on",
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


def upload_file(gi, file, history_id, storage):
    try:
        gi.tools.upload_file(
            path=file,
            history_id=history_id,
            storage=storage,
            auto_decompress=True,
        )
    except ConnectionError as ex:
        if ex.status_code == 404 and storage:
            with open(file, "rb") as fh:
                fingerprinter = fingerprint.Fingerprint()
                fp_hash = fingerprinter.get_fingerprint(fh)
            print(
                f"Unable to resume, previous upload may have been removed from server (hint: remove {fp_hash} from {storage} or change storage to reupload from the start: {ex}"
            )
        else:
            print(ex)


if __name__ == "__main__":
    # parse cli arguments
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

    for file in track(args.file, description="[cyan]Uploading..."):
        if os.path.exists(file):
            upload_file(gi, file, args.history_id, args.checkpoints)
        else:
            print(f"{file} does not exists...skipping!")
