from dataclasses import dataclass
import os
from typing import Dict, List
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BenchmarkDataclass:
    """
    Class designed to save data about Benchmarking Runs.
    To avoid confusion the "Benchmark" is the workload and the "run" is one specific iteration of it
    timestamp: The timestamp associated with the run.
    sequence: The name of this run.
    config: The config the run was executed with.
    benchmark: The name of the benchmarking workload (e.g. TPCDS)
    scale_factor: The scale factor the benchmark was set to.
    db_system: The DB system the run was made on.
    algorithm: The executed algorithm.
    budget_in_bytes: The budget in bytes
    queries: The list of queries.
    selected_indexes: The list of selected indexes
    algorithm_indexes_by_query: The indexes selected by the algorithm for the queries
    optimizer_indexes_by_query: The indexes the optimizer selected per query.
    overall_costs: The overall costs calculated for the workload.
    costs_by_query: Costs for each query
    time_run_total: How long the overall runtime was
    time_run_by_component:  If the run has distinct components this is
                            where the lengths will be noted.
    what_if_time: the time spent on what if calls
    cost_requests: how many cost request were made
    what_if_cache_hits: What if cache hits
    description: AN additional optional description
    """

    timestamp: str
    sequence: str
    config: dict
    benchmark: int
    scale_factor: int
    db_system: str
    algorithm: str
    budget_in_bytes: int
    budget_in_mb: int
    queries: list[str]
    selected_indexes: list[str]
    algorithm_indexes_by_query: dict[str, List[str]]
    overall_costs: int
    costs_by_query: dict[str, Dict[str, str]]
    time_run_total: float
    time_run_by_component: dict
    what_if_time: float
    cost_requests: int
    what_if_cache_hits: int
    description: str = ""


def load_benchmark_dataclasses_from_files(
    sequence: str, budgets: List[int], dataclass_folder: str = "dataclasses"
) -> list[BenchmarkDataclass]:
    """
    This generates a list of benchmark dataclasses based on a sequence name.
    Budgets should be given in b.
    """
    dataclasses = []

    for budget in budgets:
        file_candidate = f"{dataclass_folder}/{sequence}_{budget}.json"
        if os.path.isfile(file_candidate):
            with open(file_candidate, "r", encoding="utf-8") as file:
                dataclasses.append(BenchmarkDataclass.from_json(file.read()))
        else:
            raise IOError(f"file {file_candidate} does not exist.")

    return dataclasses


def load_benchmark_dataclass_from_file(
    sequence: str, budget: str, dataclass_folder: str = "dataclasses"
) -> BenchmarkDataclass:
    """
    Loads a BenchmarkDataclass from Json.
    """
    file_candidate = f"{dataclass_folder}/{sequence}_{budget}.json"
    if os.path.isfile(file_candidate):
        with open(file_candidate, "r", encoding="utf-8") as file:
            return BenchmarkDataclass.from_json(file.read())
    else:
        raise IOError(f"file {file_candidate} does not exist.")


def save_benchmark_dataclasses(
    data: List[BenchmarkDataclass], dataclass_folder: str = "dataclasses"
) -> None:
    """Saves a list of benchmark dataclasses to Json."""
    os.makedirs(dataclass_folder, exist_ok=True)
    for item in data:
        with open(
            f"{dataclass_folder}/{item.sequence}_{item.budget_in_bytes}.json",
            "w+",
            encoding="utf-8",
        ) as file:
            file.write(item.to_json(indent=4, sort_keys=True))
