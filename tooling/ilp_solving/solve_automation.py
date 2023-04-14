"""
This module contains functions to automate solving ILP files.
"""
import json
import subprocess
import time
from pathlib import Path
from typing import Dict


def model_gen(model_path: str, budget: int):
    """Generates an AMPL model"""
    model_string = """
set QUERIES;
param NUMBER_OF_INDEXES integer;
param NUMBER_OF_INDEX_COMBINATIONS integer;

set INDEXES = 1 .. NUMBER_OF_INDEXES;
# 0 represents no index
set COMBINATIONS = 0 .. NUMBER_OF_INDEX_COMBINATIONS;
"""
    model_string += f"param storage_budget:= {budget};"
    model_string += """
    set indexes_per_combination {COMBINATIONS};

param size {INDEXES}; # size of index
param costs {QUERIES, COMBINATIONS} default 99999999999999; # costs of combination for query

var x {INDEXES} binary; # index is created
var y {COMBINATIONS} binary; # combination is applicable
var z {COMBINATIONS, QUERIES} binary; # combination is used for query


minimize overall_costs_of_queries: sum {c in COMBINATIONS, q in QUERIES} costs[q, c] * z[c, q];

subject to one_combination_per_query {q in QUERIES}: 1 = sum {c in COMBINATIONS} z[c, q];
subject to applicable_combination {c in COMBINATIONS}: sum {i in indexes_per_combination[c]} x[i] >= card(indexes_per_combination[c]) * y[c];
subject to usable_combination {c in COMBINATIONS, q in QUERIES}: z[c, q] <= y[c];
subject to memory_consumption: sum {i in INDEXES} x[i] * size[i] <= storage_budget;
"""
    with open(model_path, "w+", encoding="utf-8") as file:
        file.write(model_string)
    return model_string


def generate_run_file(run_path: str, solver_path: str):
    """Generates the run File"""
    run_string = f"""option solver '{solver_path}';
solve;
option display_1col 10000000000000000000000000;
display x;
display y;
display z;"""
    with open(run_path, "w+", encoding="utf-8") as file:
        file.write(run_string)
    return run_string


def solve(
    input_file_path: Path,
    config: Dict[str, str],
    budget: int,
):
    """Solves a given data file."""
    print(f"started {input_file_path.name} {budget}")
    model_gen(config["model_path"], budget)
    with open(
        f"{config['solves_path']}/{input_file_path.name}-{budget}-out.solve",
        "w+",
        encoding="utf-8",
    ) as outfile:
        start = time.time()
        subprocess.run(
            [
                config["ampl_path"],
                config["model_path"],
                input_file_path,
                config["run_file_path"],
            ],
            check=False,
            stdout=outfile,
        )
        outfile.write(f"\nTime: {time.time() - start}")

    print(f"completed {input_file_path.name} {budget}")


def load_solver_config(
    config_file=Path("tooling/ilp_solving/solve_automation_config.json"),
) -> Dict[str, str]:
    """
    loads the config.
    """
    config_template = {
        "model_path": "",
        "run_file_path": "",
        "ampl_path": "",
        "solver_path": "",
        "solves_path": "",
    }

    if not config_file.is_file():
        raise FileNotFoundError(f"{config_file} cannot be found.")

    with open(config_file, "r", encoding="utf-8") as file:
        config: Dict[str, str] = json.load(file)

    if config.keys() != config_template.keys():
        raise ValueError(
            f"Config file {str(config_file.resolve())} does not contain the correct keys."
        )

    for target in ['ampl_path', 'solver_path']:
        path = Path(config[target])
        if not path.is_file():
            raise FileNotFoundError(f'{target} : {str(path)} does not exist.')


    for target in ['solves_path', 'model_path', 'run_file_path']:
        path = Path(config[target])
        if not path.exists():
            if path.suffix:
                # if it has a file extension, try to create the parent folder
                path.parent.mkdir(parents=True, exist_ok=True)
                # then create the file with touch()
                path.touch()
            else:
                # if it doesn't have a file extension, create the folder with mkdir()
                path.mkdir(parents=True, exist_ok=True)
    generate_run_file(config['run_file_path'], config['solver_path'])

    return config
