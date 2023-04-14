"""Plotting functions for analysis"""
import re
from typing import Any, Dict, List, Union

import matplotlib.pyplot as plt

from tooling.analysis.benchmark_compare import (
    compare_benchmark_sequence,
    comparison_affected_queries,
)
from tooling.benchmark_dataclass import BenchmarkDataclass
from tooling.plotting.plot_helper import PlotHelper
from tooling.util import convert_b_to_gb


def _texify_string(string: str) -> str:
    """surrounds numbers with $ symbols. Badly implemented but does the thing."""
    string = string.replace("_", "\\_")
    return re.sub(r"(\d+)", r"$\1$", string)


def shorten_index_string(string: str) -> str:
    """Shortens an index string by removing the table identifier."""
    return string[string.find(".") + 1 :]


def _convert_cell_to_sub_table(cell: List[str]) -> str:
    """Converts a list to a sub table for linebreaks."""
    cell_string = "\\\\ ".join(cell)
    return "\\begin{tabular}[c]{@{}l@{}}" + cell_string + "\\end{tabular}"


def _texify_table(table: List[Union[List[List[str]], List[List[str]]]]) -> str:
    preamble = """\\begin{table}[htbp]
	\\centering
		\\begin{tabularx}{\\textwidth}{|X|X|X|X|X|}
		\\hline
"""
    suffix = """		\\end{tabularx}
\\end{table}"""

    # converts cells into string
    for row_index, row in enumerate(table):
        for column_index, cell in enumerate(row):
            if isinstance(cell, list):
                table[row_index][column_index] = _convert_cell_to_sub_table(cell)

    table_string = preamble

    for row in table:
        table_string += f"""\t\t{' & '.join(row)} \\\\
        \\hline
"""

    table_string += suffix
    table_string = _texify_string(table_string)

    return table_string


def plot_runtime(
    data: Dict[str, List[BenchmarkDataclass]],
    plot_helper: PlotHelper,
    algorithm_removes: List[str] = None,
    budget_removes: List[str] = None,
    save_path: str = "run_times.pdf",
) -> None:
    """
    Plots the run times of algorithms vs the budget of the algorithm.
    """
    if not algorithm_removes:
        algorithm_removes = []

    if not budget_removes:
        budget_removes = []

    for algorithm, benchmarks in data.items():
        if algorithm in algorithm_removes:
            continue

        # The generator magic here basically creates a list of
        # overall costs, divided by a "no index cost"
        overall_costs = [
            benchmark.time_run_total
            for benchmark in filter(
                lambda x: x.budget_in_bytes not in budget_removes, benchmarks
            )
        ]
        budgets = [
            convert_b_to_gb(benchmark.budget_in_bytes) for benchmark in benchmarks
        ]
        plt.step(
            budgets,
            overall_costs,
            where="mid",
            label=algorithm,
            marker=plot_helper.get_symbol(algorithm),
            color=plot_helper.get_color(algorithm),
            fillstyle="none",
        )

    plt.xlabel("Index Storage Budget (GB)")
    plt.ylabel("Runtime Algorithm (sec)")
    # pylint: disable=undefined-loop-variable
    plt.title(f"Algorithm Runtime on {benchmarks[0].benchmark}")
    plt.legend()
    plt.plot()
    plt.savefig(save_path)
    plt.show()


def plot_overall_costs(
    data: Dict[str, List[BenchmarkDataclass]],
    no_index_cost: float,
    plot_helper: PlotHelper,
    algorithm_removes: List[str] = None,
    budget_removes: List[str] = None,
    save_path: str = "run_times.pdf",
) -> None:
    """Plots the overall costs of a dictionary of algorithms with benchmark lists"""

    if not algorithm_removes:
        algorithm_removes = []

    if not budget_removes:
        budget_removes = []

    for algorithm, benchmarks in data.items():
        if algorithm in algorithm_removes:
            continue

        filtered_benchmarks = list(
            filter(lambda x: x.budget_in_bytes not in budget_removes, benchmarks)
        )
        overall_costs = [
            benchmark.overall_costs / no_index_cost for benchmark in filtered_benchmarks
        ]
        budgets = [
            convert_b_to_gb(benchmark.budget_in_bytes)
            for benchmark in filtered_benchmarks
        ]
        plt.step(
            budgets,
            overall_costs,
            where="mid",
            label=algorithm,
            marker=plot_helper.get_symbol(algorithm),
            color=plot_helper.get_color(algorithm),
            fillstyle="none",
        )
    plt.xlabel("Index Storage Budget (GB)")
    plt.ylabel("Estimated Costs Algorithm (% vs no index)")
    # pylint: disable=undefined-loop-variable
    plt.title(f"Algorithm relative total costs on {benchmarks[0].benchmark}")
    plt.legend()
    plt.savefig(save_path)
    plt.show()


def plot_number_indexes(
    data: Dict[str, List[BenchmarkDataclass]],
    plot_helper: PlotHelper,
    algorithm_removes: List[str] = None,
    budget_removes: List[str] = None,
    save_path: str = "number_indexes.pdf",
) -> None:
    """Plots the number of indexes selected vs budget"""

    if not algorithm_removes:
        algorithm_removes = []

    if not budget_removes:
        budget_removes = []

    for algorithm, benchmarks in data.items():
        if algorithm in algorithm_removes:
            continue

        filtered_benchmarks = list(
            filter(lambda x: x.budget_in_bytes not in budget_removes, benchmarks)
        )
        overall_costs = [
            len(benchmark.selected_indexes) for benchmark in filtered_benchmarks
        ]
        budgets = [
            convert_b_to_gb(benchmark.budget_in_bytes)
            for benchmark in filtered_benchmarks
        ]
        plt.step(
            budgets,
            overall_costs,
            where="mid",
            label=algorithm,
            marker=plot_helper.get_symbol(algorithm),
            color=plot_helper.get_color(algorithm),
            fillstyle="none",
        )
    plt.xlabel("Index Storage Budget (GB)")
    plt.ylabel("Number of Indexes Selected")
    # pylint: disable=undefined-loop-variable
    plt.title(f"Algorithm relative total costs on {benchmarks[0].benchmark}")
    plt.legend()
    plt.savefig(save_path)
    plt.show()


def _convert_affected_queries(
    affected_queries_dict: Dict[str, Dict[str, Any]]
) -> List[str]:
    """Turns an affected query string into a pretty string for a table."""
    return_list = []
    for query, value in affected_queries_dict.items():
        index_config_list = []
        if len(value["shared"]) > 0:
            shared_list = list([shorten_index_string(x) for x in value["shared"]])
            index_config_list.append(_convert_cell_to_sub_table(shared_list))
        if len(value["2only"]) > 0:
            only_2_list = list(
                [
                    "{\\color{green}+" + shorten_index_string(x) + "}"
                    for x in value["2only"]
                ]
            )
            index_config_list.append(_convert_cell_to_sub_table(only_2_list))
        if len(value["1only"]) > 0:
            only_1_list = list(
                [
                    "{\\color{red}-" + shorten_index_string(x) + "}"
                    for x in value["1only"]
                ]
            )
            index_config_list.append(_convert_cell_to_sub_table(only_1_list))

        index_config_string = _convert_cell_to_sub_table(index_config_list)

        percentage_change = int(100 - value["q2_cost_percentage"])
        if percentage_change > 0:
            color = "green"
        else:
            color = "red"
        cost_change = "{\\color{" + color + "}" + str(percentage_change) + "}"
        conversion_string = f"{query} ({cost_change}): {index_config_string}"

        return_list.append(conversion_string)

    return return_list


def generate_index_comparison_table(
    benchmarks: List[BenchmarkDataclass],
    file_name: str = "benchmark_comparison_table.tex",
    remove_equals: bool = True,
    index_configuration_row_name: str = "Config",
    show_index_configuration_row: bool = True,
    indexes_added_row_name: str = "Indexes Added",
    show_indexes_added_row: bool = True,
    indexes_removed_row_name: str = "Indexes Removed",
    show_indexes_removed_row: bool = True,
    queries_affected_row_name: str = "Queries Affected",
    show_queries_affected_row: bool = True,
) -> str:
    """
    Takes a list of benchmarks and returns their changes as a latex table.
    It is recommended to prepend a "no index" dataclass to the benchmarks to properly capture
    the 'first' change.
    """
    compares = compare_benchmark_sequence(benchmarks)
    #
    if remove_equals:
        compares = list(filter(lambda x: not x["overall_costs_diff"] == 0, compares))

    # sets up metadata
    table_rows = [
        [
            "Comparison",
            index_configuration_row_name,
            indexes_added_row_name,
            indexes_removed_row_name,
            queries_affected_row_name,
        ]
    ]

    for comparison in compares:
        row = []
        row.append(
            (
                f"{comparison['comparison_meta']['sequence1']}-"
                f"{convert_b_to_gb(comparison['comparison_meta']['budget1'])}"
                f"$\\rightarrow$ "
                f"{comparison['comparison_meta']['sequence2']}-"
                f"{convert_b_to_gb(comparison['comparison_meta']['budget2'])}"
            )
        )

        # generates index configuration
        if show_index_configuration_row:
            row.append(
                list([shorten_index_string(x) for x in comparison["index_config_2"]])
            )

        # generates added indexes
        if show_indexes_added_row:
            row.append(list([shorten_index_string(x) for x in comparison["2only"]]))

        # generates removed indexes
        if show_indexes_removed_row:
            row.append(list([shorten_index_string(x) for x in comparison["1only"]]))

        # generates affected queries row
        if show_queries_affected_row:
            affected_queries = comparison_affected_queries(comparison)
            row.append(_convert_affected_queries(affected_queries))

        table_rows.append(row)

    table_string = _texify_table(table_rows)

    for row_index, _ in enumerate(table_rows):
        for column_index, _ in enumerate(table_rows[row_index]):
            table_rows[row_index][column_index] = _texify_string(
                table_rows[row_index][column_index]
            )

    with open(file_name, "w+", encoding="utf-8") as file:
        file.write(table_string)

    return table_string
