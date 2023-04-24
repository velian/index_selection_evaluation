from pathlib import Path
from typing import Dict
from tooling.ilp_solving.decomposition_templates import template, template2

import json
import subprocess


def get_number_of_index_combinations(file_name):
    with open(file_name) as f:
        data = json.loads(f.read())
        return data['number_of_index_combinations']

def get_single_index_combinations(file_name):
    print(file_name)
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        index_combinations = data['index_combinations']
        single_index_combinations = []
        for combination in index_combinations:
            if len(combination['index_ids']) < 2:
                single_index_combinations.append(combination['combination_id'])
    return single_index_combinations

def decomposition_solve(
        benchmark,
        solve_name: str,
        json_file: Path,
        ampl_file: Path,
        number_of_chunks,
        config: Dict[str, str]
        ) -> None:
    ampl = config['ampl_path']
    print(ampl)
    solver = config['solver_path']

    ampl_data_file = ampl_file
    json_data_file = json_file
    fixed_combinations = get_single_index_combinations(json_data_file)
    number_of_combinations = get_number_of_index_combinations(json_data_file)
    print(benchmark, ampl_data_file)
    print(number_of_combinations, fixed_combinations)

    budgets = range(500, 15001, 500)

    if number_of_chunks == 1:
        suffix = '_solution'
    else:
        suffix = ''

    fixed_combination_str = '{' + ', '.join(map(str, fixed_combinations)) + '}'

    for budget in budgets:
        file_name = f'{benchmark}_decomposition_{solve_name}_budget{budget}_chunks{number_of_chunks}{suffix}.txt'
        cmd_file = f'{benchmark}_decomposition_{solve_name}_budget{budget}_chunks{number_of_chunks}_solve_chunks.cmd'


        with open(cmd_file, 'w+') as f:
            f.write(template.substitute(
                solver=solver,
                ampl_data_file=ampl_data_file,
                ilp_model_file=config["decomp_model_path"],
                storage_budget=budget,
                fixed_combinations=fixed_combination_str,
                number_of_combinations=number_of_combinations,
                number_of_chunks=number_of_chunks,
                file_name=file_name
                )
            )
        p = subprocess.Popen([ampl, f'{cmd_file}'])


        if number_of_chunks == 1:
            # no step 3 required
            continue

        overall_time = 0
        combinations = set()
        for i in fixed_combinations:
            combinations.add(str(i))
        with open(file_name, 'r') as f:
            for line in f.read().split('\n'):
                if line.startswith('___'):
                    tokens =line.strip('_').split()
                    memory = int(tokens[0]) / 1000**3
                    costs = float(tokens[1])
                    time_ = float(tokens[2])

                    overall_time += time_
                if line.startswith('combinations:'):
                    tokens = line.strip('combinations:').split()
                    if benchmark == 'tpch':
                        assert len(tokens) == 19
                    else:
                        assert len(tokens) == 90
                    for token in tokens:
                        combinations.add(token)
        combination_string = ', '.join(combinations)

        file_name2 = f'{benchmark}_decomposition_{solve_name}_budget{budget}_chunks{number_of_chunks}_solution.txt'
        cmd_file2 = f'{benchmark}_decomposition_{solve_name}_budget{budget}_chunks{number_of_chunks}_solve.cmd'


        with open(cmd_file2, 'w') as f:
            f.write(template2.substitute(
                solver=solver,
                ampl_data_file=ampl_data_file,
                ilp_model_file=config["decomp_model_path"],
                overall_time=overall_time,
                storage_budget=budget,
                combination_string=combination_string,
                file_name2=file_name2
                )
            )
        p = subprocess.Popen([ampl, f'{cmd_file2}'])
        p.wait()


if __name__ == '__main__':
    pass
    # Examples

    # TPC-H
    # main('tpch', 'extend_2_cache', number_of_chunks=2)
    # main('tpch', 'extend_3_cache', number_of_chunks=2)
    # main('tpch', 'cophy__width2__per_query2__query-based', number_of_chunks=5)

    # TPC-DS
    # main('tpcds', 'extend_2_cache', number_of_chunks=20)
    # main('tpcds', 'extend_3_cache', number_of_chunks=20)
    # main('tpcds', 'cophy__width2__per_query2__query-based', number_of_chunks=100)
