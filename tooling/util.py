"""Util functions for thee tooling_ma module"""
from typing import Dict, List, Union
from pathlib import Path

from tooling.benchmark_dataclass import BenchmarkDataclass


def convert_mb_to_b(mb_value: int) -> int:
    """Converts a value from mb to b"""
    return mb_value * 10**6


def convert_b_to_mb(b_value: int) -> int:
    """Converts a value from b to mb"""
    return b_value / 10**6


def convert_b_to_gb(b_value: int) -> int:
    """Covnerts a value from b to gb"""
    return b_value / 10**9


def convert_gb_to_b(gb_value: int) -> int:
    """Converts a value from gb to b"""
    return gb_value * 10**9


def fuzzy_equality(
    value1: Union[float, int], value2: Union[float, int], threshold: Union[float, int]
) -> bool:
    """
    If two values are within threshold percent of each other, they will be treated as the same.
    Remember float inaccuracy.
    """
    return ((1 - (min(value1, value2) / max(value1, value2))) * 100) <= threshold


def organize_dataclasses_by_sequence(
    data: List[BenchmarkDataclass],
) -> Dict[str, BenchmarkDataclass]:
    """
    Reorganizes the dataclasses so that each sequence has its own list,
    and that list is sorted by budget.
    """
    organized_dict: Dict[str, List[BenchmarkDataclass]] = {}
    for benchmark in data:
        if benchmark.sequence not in organized_dict:
            organized_dict[benchmark.sequence] = []
        organized_dict[benchmark.sequence].append(benchmark)

    for _, benchmark_list in organized_dict.items():
        benchmark_list.sort(key=lambda x: x.budget_in_bytes)
    return organized_dict


def get_files_in_folder(
    folder_path: str,
    file_extension: str,
    white_list: List[str] = None,
    black_list: List[str] = None,
) -> List[Path]:
    """
    Get a list of all files in a given folder that are of a given filetype, and optionally meet
    a whitelist and/or blacklist criteria.

    Parameters:
    folder_path (str): The path to the folder to search.
    file_extension (str): The file extension to search for (e.g. ".txt").
    white_list (List[str], optional): A list of substrings that must be present in the filename.
    black_list (List[str], optional): A list of substrings that must not be present in the filename.

    Returns:
    List[str]: A list of all files in the folder that match the criteria.
    """
    folder_path = Path(folder_path)
    matching_files = []

    for file_path in folder_path.glob(f"*{file_extension}"):
        file_name = file_path.name
        if white_list is not None and not all(
            substring in file_name for substring in white_list
        ):
            continue
        if black_list is not None and any(
            substring in file_name for substring in black_list
        ):
            continue
        matching_files.append(Path(file_path))

    return matching_files
