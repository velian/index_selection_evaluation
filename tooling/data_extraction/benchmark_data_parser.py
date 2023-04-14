"""Contains the functions that """
import csv
from pathlib import Path
from typing import List

from tooling.benchmark_dataclass import BenchmarkDataclass
from tooling.data_extraction.parse_ampl_benchmark import extract_cophy_entries
from tooling.data_extraction.parse_normal_benchmark import (
    calculate_overall_costs,
    extract_entries,
    retrieve_query_dicts,
)


def convert_normal_csvs(
    data_paths: List[Path],
    plans_path: Path,
    comment: str = "",
) -> List[BenchmarkDataclass]:
    """
    This gets a list of normal CSV files for selection
    benchmarks and turns them into Benchmark Dataclasses
    """
    data: List[BenchmarkDataclass] = []

    for item in data_paths:
        data += extract_entries(item, comment, plans_path)
    data.sort(key=lambda x: x.budget_in_bytes)
    return data


def convert_cophy_csvs(
    data_paths: List[Path], budgets: List[int], comment: str = ""
) -> List[BenchmarkDataclass]:
    """
    This gets COPHY style CSVs and converts them into benchmark Dataclasses
    """
    data: List[BenchmarkDataclass] = []

    for item in data_paths:
        data += extract_cophy_entries(item, comment, budgets)
    return data


def no_index_costs(path):
    """Gets the costs for a no index run."""
    # Hacky but less annoying than the alternative
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        reader.next()
        return calculate_overall_costs(retrieve_query_dicts(reader.next()))
