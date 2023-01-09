from dataclasses import dataclass
from typing import Dict, List
from dataclasses_json import dataclass_json
from pathlib import Path
import csv
import ast

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
    db_system: str
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

def convert_csv_to_dataclass(identifier: str, timestamp: str, path: str, sequence: str, descritpion: str) -> BenchmarkDataclass:
    datarow = convert_timestamp_to_line(path, timestamp)
    data = BenchmarkDataclass(
        identifier,
        timestamp,
        sequence,
        ast.literal_eval(datarow[3]),
        datarow[5],
        datarow[4],
        datarow[6],
        datarow[2],
        convert_budget(ast.literal_eval(datarow[3])),
        [],
        datarow[-1],
        {},
        {},
        calculate_overall_costs(retrieve_query_dicts(datarow)),
        retrieve_query_dicts(datarow),
        datarow[7],
        {},
        0,
        0,
        description=descritpion
    )
    return data

def convert_timestamp_to_line(path: str, timestamp: str) -> List[str]:
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] == timestamp:
                return row

def convert_budget(config: Dict) -> int:
    if "budget_MB" in config.keys():
        return int(config['budget_MB']) * 1000 * 1000
    else:
        return int(config['budget']) * 1000 * 1000

def retrieve_query_dicts(line: List) -> List[Dict]:
    old = line[16:-1]
    new = []
    for item in old:
        new.append(ast.literal_eval(item))
    return new

def calculate_overall_costs(row: List[Dict]) -> int:
    total = 0
    for costs in row:
        total += float(costs['Cost'])
    return total

dtat_object = convert_csv_to_dataclass('extend', '2023-01-08 16:38:24', '/Users/Julius/masterarbeit/J-Index-Selection/benchmark_results/results_extend_tpch_19_queries.csv', 'baseline', 'Baseline Run for extend')