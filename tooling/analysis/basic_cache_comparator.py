"""
This module contains functions to compare caches to one another.

"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

from texttable import Texttable

# number indexes
# number


def load_cache_data(caches: List[Path]) -> List[Dict[str, Any]]:
    """
    Reads the cache JSON files from a list of Paths and returns a list of dictionaries
        with additional metadata.
    Extracts name and budget from the filename if it is not present in the cache data.

    Args:
        caches (List[Path]): A list of Path objects representing the cache JSON files.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the cache data,
            with added metadata.

    Raises:
        FileNotFoundError: If a file in the `caches` list cannot be found.
    """
    cache_data_with_metadata = []
    for cache_file in caches:
        if not cache_file.is_file():
            raise FileNotFoundError(f"File {cache_file.absolute()} not found.")
        else:
            logging.info("Reading %s", str(cache_file.absolute()))
            with open(cache_file, "r", encoding="utf-8") as file:
                cache_dict = json.load(file)
                name = cache_dict.get("name")
                budget = cache_dict.get("budget")
                if not name or not budget:
                    name, budget = _convert(cache_file.stem)
                cache_dict.update(
                    {
                        "name": name,
                        "budget": budget,
                        "key": f"{name}-{budget}",
                        "num_queries": len(cache_dict.get("queries", [])),
                        "num_costs": len(cache_dict.get("query_costs", [])),
                        "same_as": [],
                    }
                )
                cache_data_with_metadata.append(cache_dict)
    return cache_data_with_metadata


def _sort_basic_data(rows: List[Dict[str, Any]], sort_keys: List[str]) -> None:
    """Sorts a List of dictionaries by the keys in sort keys."""
    for sort_key in sort_keys:
        if sort_key not in rows[0]:
            logging.error(
                "Cannot sort dictionary by key %s, as it is not in the dict.", sort_key
            )
            continue
        rows.sort(key=lambda x: x[sort_key])  # pylint: disable=cell-var-from-loop


def dict_to_row(data_dict: Dict[str, Any], keys: List[str]) -> List[Any]:
    """Converts a dict to a list of strings."""
    row = []
    for key in keys:
        row.append(data_dict[key])
    return row


def convert_rows(rows: List[Dict[str, Any]], keys: List[str]) -> List[List[Any]]:
    """Converts a List of dicts to a list of rows, based on the given keys."""
    converted_rows = []
    for row in rows:
        converted_rows.append(dict_to_row(row, keys))
    return converted_rows


def uniquify_data(data: List[Dict[str, Any]], unique_keys: List[str]) -> List[Dict]:
    """
    Makes all rows unique based on the unique keys as a whole.
    i.e. only if all data found in all unique keys is the same.
    Does nothing if no unique keys are given.
    """
    if len(unique_keys) <= 0:
        logging.info("No data was made unique as no keys were given.")
        return data
    uniquified_dicts = {}
    for row in data:
        unique_key = "".join([str(row[x]) for x in unique_keys])
        if unique_key in uniquified_dicts:
            uniquified_dicts[unique_key]["same_as"].append(row["key"])
        else:
            uniquified_dicts[unique_key] = row
    return list(uniquified_dicts.values())


def _convert(text: str) -> Tuple[str, int]:
    """
    Converts a filename to a cache.
    Newer caches add this to the JSON directly.
    """
    text = text.replace("tpch_", "").replace("_cache_input", "")
    name = text[text.find("_") + 1 :]
    budget = int(text[: text.find("_")])
    return (name, budget)


def cache_prepender(
    base_string: str, min_budget: int, max_budget: int, step: int
) -> List[str]:
    """
    Base string needs an xxx in place of budget.
    TODO Deprecate
    """
    files = []
    for budget in range(min_budget, max_budget + 1, step):
        files.append(base_string.replace("xxx", str(budget)))
    return files


def parse_into_table(
    rows: List[List[str]],
    keys: List[str],
    unique_keys: List[str],
    sort_indexes: List[str] = None,
) -> str:
    """Converts the cache data into a row format used by both texttable and latex table."""
    if sort_indexes:
        _sort_basic_data(rows, sort_indexes)

    rows = uniquify_data(
        rows,
        unique_keys,
    )
    rows = convert_rows(rows, keys)

    return rows


def rows_to_texttable(
    rows: List[List[str]],
    header: List[str],
):
    """Converts rows and a header into a texttable."""
    return (
        Texttable()
        .add_rows(rows, header=False)
        .header(header)
        .set_max_width(130)
        .draw()
    )


def tuples_to_lists(tuples: List[Tuple[str]]) -> Tuple(List[str]):
    """
    Converts a list of 2-tuples of strings into two lists of strings.
    The first list contains the first entry in the tuple and the second list
    contains the second entry.

    Args:
        tuples: A list of 2-tuples of strings, Column name then key
            i.e. (Column name, Column Key)

    Returns:
        A tuple of two lists of strings.
    """
    names, keys = [], []
    for name_key in tuples:
        names.append(name_key[0])
        keys.append(name_key[1])
    return names, keys


def print_folder_to_texttable(
    folder_path: Path,
    column_key_tuple: List[Tuple[str, str]],
    unique_keys: List[str],
    sort_keys: List[str],
) -> str:
    """
    Collects all JSON files in the specified folder path
        and formats their contents into a text table.

    Args:
        folder_path: A `Path` object representing the folder path
            containing the JSON files.
        column_key_tuple: A list of 2-tuples of strings containing the column names
            and their corresponding JSON keys.
        unique_keys: A list of JSON keys that are relevant for "uniqueness".
        sort_keys: A list of JSON keys that should be used to sort the rows in the table.

    Returns:
        A formatted string containing the contents of the text table.
    """
    # Load all JSON files in the specified folder path into memory
    caches = load_cache_data(folder_path)

    # Extract the column names and JSON keys from the specified `column_key_tuple`
    column_names, json_keys = tuples_to_lists(column_key_tuple)

    # Parse the contents of the JSON files into a table format
    table_rows = parse_into_table(caches, json_keys, unique_keys, sort_keys)

    # Convert the table rows to a formatted string containing the text table
    text_table = rows_to_texttable(table_rows, column_names)

    return text_table
