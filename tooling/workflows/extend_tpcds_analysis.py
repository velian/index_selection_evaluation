"""The main file to handle all the analysis function"""
import json
import os

from tooling.data_extraction.benchmark_data_parser import convert_normal_csvs
from tooling.plotting.visualization import plot_overall_costs, plot_runtime
from tooling.plotting.plot_helper import get_plot_helper


def construct_budgets(min, max, step):
    value = min
    budgets = []
    while value <= max:
        budgets.append(value)
        value += step
    return budgets


data = convert_normal_csvs(
    [
        "/Users/Julius/masterarbeit/Masterarbeit-JStreit/data/measures_3/tpcds/results_extend_tpcds_90_queries.csv",
    ],
    "/Users/Julius/masterarbeit/Masterarbeit-JStreit/data/plans3/",
)

plot_helper = get_plot_helper()


# TPCH =46164891.51 TPCDS=121150974.81
algorithm_ignores = []
nu_data = [x for x in data if x.sequence not in algorithm_ignores]
plot_overall_costs(nu_data, [], 121150974, plot_helper)


algorithm_ignores = []
nu_data = [x for x in data if x.sequence not in algorithm_ignores]
plot_runtime(data, plot_helper)


os.makedirs("dataclasses", exist_ok=True)
for item in data:
    with open(
        f"dataclasses/{item.sequence}_{item.budget_in_bytes}.json",
        "w+",
        encoding="utf-8",
    ) as file:
        file.write(item.to_json(indent=4, sort_keys=True))
