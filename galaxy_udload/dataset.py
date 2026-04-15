#!/usr/bin/env python3

import argparse
import rich.console
import rich.table
import re
import datetime


class DatasetNotFoundError(Exception):
    """Raised when no Galaxy datasets match the query."""
    def __init__(self, dataset_name):
        super().__init__(f"No datasets matching [italic yellow]{dataset_name}[/italic yellow] found!")


class DatasetAmbiguousError(Exception):
    """Raised when multiple Galaxy datasets match the query."""
    def __init__(self, dataset_name, datasets):
        if not dataset_name:
            msg = (
                "Multiple datasets found!\n"
                "Select one by specifying an id with [italic green]--dataset-id[/italic green] "
                "or a name with [italic green]--dataset-name[/italic green]."
            )
        else:
            msg = (
                f"Multiple datasets matching [italic yellow]{dataset_name}[/italic yellow] found!\n"
                "Select one by specifying an id with [italic green]--dataset-id[/italic green]."
            )
        super().__init__(msg)
        self.datasets = datasets


def create_table(datasets=[]):
    """
    Create a Rich table displaying a list of dataset records.

    Parameters
    ----------
    datasets : list of dict, optional
        A list of dataset objects. Each dictionary is expected to contain:
        - "id": Unique identifier for the record (str)
        - "name": Display name of the record (str)
        - "updated_time": ISO-formatted timestamp string (e.g., "2024-01-15T12:34:56")

    Returns
    -------
    rich.table.Table
        A Rich Table object with columns for ID, name, updated time.
    """
    table = rich.table.Table()
    table.add_column("dataset id", style="cyan", no_wrap=True)
    table.add_column("dataset name", style="green")
    table.add_column("last updated", style="dark_orange")
    table.add_column("history id", style="magenta")
    

    for ds in datasets:
        table.add_row(
            ds.get("id", ""),
            ds.get("name", ""),
            datetime.datetime.fromisoformat(ds["update_time"]).strftime("%Y-%m-%d %H:%M:%S"),
            ds.get("history_id", ""),
        )

    return table


def get_datasets(gi, history_id=None):
    """
    Retrieve a list of datasets from a Galaxy instance.

    Args:
        gi: A Galaxy instance object used to interact with the Galaxy API.
        history_id: Optional string representing the ID of a specific history
            to filter datasets. If None, datasets from all histories are returned.

    Returns:
        A list of dataset dictionaries containing information about visible,
        non-deleted, and non-purged datasets, ordered by history_id, update_time,
        and hid.
    """
    kwargs = dict(
        visible=True,
        deleted=False, 
        purged=False, 
        history_id=history_id,
        order="history_id,update_time,hid"
    )
    return list(gi.datasets.get_datasets(**kwargs))


def dataset_exists(gi, dataset_id, history_id=None):
    """
    Check whether a dataset with the given ID exists.

    Parameters
    ----------
    gi : object
        An object that provides access to datasets through
        `gi.datasets.get_datasets()`, which must return an iterable
        of dictionaries containing an "id" field.
    dataset_id : str
        The ID of the dataset to search for.
    history_id : str, optional
        If provided, restricts the search to datasets within this history.

    Returns
    -------
    bool
        True if a dataset with the specified ID exists, otherwise False.
    """
    datasets = get_datasets(gi, history_id)

    return any(ds["id"] == dataset_id for ds in datasets)


def filter_datasets(gi, dataset_name=None, ignore_case=False, history_id=None):
    """
    Return Galaxy datasets whose names match a given pattern.

    Parameters
    ----------
    gi : object
        A GalaxyInstance-like object exposing `gi.datasets.get_datasets()`.
    dataset_name : str, optional
        A substring or regular expression to match against dataset names.
        If None, all datasets are returned.
    ignore_case : bool, optional
        If True, matching is case-insensitive.
    history_id : str, optional
        If provided, restricts the search to datasets within this history.

    Returns
    -------
    list of dict
        Datasets whose "name" field matches the pattern.
    """
    datasets = get_datasets(gi, history_id)

    if not dataset_name:
        return datasets

    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(dataset_name, flags=flags)

    return [ds for ds in datasets if ds.get("name") and pattern.search(ds["name"])]


def register_subcommand(subparser):
    """
    Create and configure the dataset sub-command argument parser.

    Returns
    -------
    argparse.ArgumentParser
        A fully configured argument parser ready for use by the CLI.
    """
    parser = subparser.add_parser(
        name="dataset",
        description="UseGalaxy dataset utility.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        default=True,
        help="List user datasets",
    )

    parser.add_argument(
        "-n",
        "--dataset-name",
        default=None,
        help="Dataset name to filter on",
    )

    parser.add_argument(
        "--dataset-id",
        "--check-dataset-id",
        dest="dataset_id",
        default=None,
        help="Dataset id to check existence of",
    )

    parser.add_argument(
        "-i",
        "--ignore-case",
        default=False,
        action="store_true",
        help="Search for datasets ignoring case",
    )

    parser.add_argument(
        "--history-id",
        dest="history_id",
        default=None,
        help="Restrict datasets to a specific history id",
    )

    parser.set_defaults(func=handle_dataset)

    return parser


def handle_dataset(args):
    """
    Sub-entry point.
    """
    console = rich.console.Console()

    if args.dataset_id:
        end_msg = "[green]exists[/green]" if dataset_exists(args.gi, args.dataset_id, args.history_id) else "[yellow]does not exist[/yellow]"
        console.print(f"Dataset with id [italic cyan]{args.dataset_id}[/italic cyan] {end_msg}")
    else:
        datasets = []

        if args.list and args.dataset_name is None:
            datasets = filter_datasets(args.gi, history_id=args.history_id)

        elif args.dataset_name:
            datasets = filter_datasets(args.gi, args.dataset_name, args.ignore_case, args.history_id)

        table = create_table(datasets)
        console.print(table)