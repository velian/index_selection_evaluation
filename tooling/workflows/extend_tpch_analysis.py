"""The main file to handle all the analysis function"""
import json
import os

from data_handler import convert_normal_csvs
from visualisation import (
    plot_overall_costs,
    plot_runtime,
    plot_number_indexes,
    generate_index_comparison_table,
)
from plot_helper import get_plot_helper
from benchmark_dataclass import save_benchmark_dataclasses
from util import organize_dataclasses_by_sequence, convert_b_to_mb


def construct_budgets(min, max, step):
    value = min
    budgets = []
    while value <= max:
        budgets.append(value)
        value += step
    return budgets


data = convert_normal_csvs(
    [
        "/Users/Julius/masterarbeit/Masterarbeit-JStreit/data/measures_3/tpch/results_extend_tpch_19_queries.csv",
    ],
    "/Users/Julius/masterarbeit/Masterarbeit-JStreit/data/plans3/",
)
save_benchmark_dataclasses(data)
data = organize_dataclasses_by_sequence(data)
generate_index_comparison_table(
    data["extend-1"],
    file_name="/Users/Julius/Dropbox/Apps/Overleaf/Masterarbeit/tables/tpch_changes_table.tex",
)
exit()
plot_helper = get_plot_helper()

# TPCH =46164891.51 TPCDS=121150974.81
algorithm_ignores = []
plot_overall_costs(data, 46164891, plot_helper, save_path="costs_extend_tpch.pdf")

# Different Scales
plot_overall_costs(
    data,
    46164891,
    plot_helper,
    budget_removes=[
        x for x in range(int(5.5 * 1000**3), 20 * 1000**3 + 1, int(0.5 * 1000**3))
    ],
    save_path="costs_extend_tpch_early.pdf",
)

removes = [x for x in range(0 * 1000**3, 5 * 1000**3, int(0.5 * 1000**3))]
removes.extend(
    [x for x in range(10 * 1000**3, 20 * 1000**3 + 1, int(0.5 * 1000**3))]
)

plot_overall_costs(
    data,
    46164891,
    plot_helper,
    budget_removes=removes,
    save_path="costs_extend_tpch_late.pdf",
)
plot_runtime(data, plot_helper)
plot_number_indexes(data, plot_helper)
