from dataclasses import dataclass
from typing import List
from dataclasses_json import dataclass_json
from pathlib import Path

@dataclass_json
@dataclass
class BenchmarkDataclass:
    """Class designed to save data about runs"""

    identifier:  str # an Identifier for a given run aka -> Name of algo, Name of Benchmark
    timestamp: str # The timestamp associated with the run
    sequence: str # If this belongs to some particular sequence/descriptor
    config: dict # The config that this run was made with
    benchmark: int # the benchmark this run was made on
    scale_factor: int # the scale factor at which the run was made
    db_system: int
    algorithm: str # name of the algorithm
    budget_in_bytes: int # The budget this run was made with, in bytes
    queries: list[str] # list of all queries this run is associated with.
    selected_indexes: list[str] # all the indexes this algorithm chose
    algorithm_indexes_by_query: dict # The dictionary that describes indexes by query as according to the algorithm
    optimizer_indexes_by_query: dict # The indexes chosen by the optimizer when running a given query
    overall_costs: int # The overall costs according to the algorithm.
    costs_by_query: dict
    time_run_total: float # how long the algorithm ran
    time_run_by_component: dict # if the algorithm produces different runtime components they can be saved here
    what_if_time: float # all the information we have about what if times
    what_if_cache_hits: int # All the information we have about cache hits
    description: str = "" # Optional particular discription, should more info be necessary

def convert_csv_to_dataclass(identifier: str, timestamp: str, sequence: str, ) -> BenchmarkDataclass:

    data = BenchmarkDataclass(
        identifier,

    )


    return dataclass

def convert_timestamp_to_line() -> List[str]:
    pass
