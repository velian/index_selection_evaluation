"""
This module deals with generating information from Benchmark dataclasses.
Largely deprecated at this stage.
"""
from typing import Dict, List
from tooling.benchmark_dataclass import BenchmarkDataclass


def overall_costs_breakdown(
    data: List[BenchmarkDataclass],
) -> Dict[str, Dict[int, str]]:
    """
    This converts a list of data files to a dictionary, that is organized by budget
    and then again by overall costs, thus returning a dictionary where all overall costs contain the
    benchmark that had them.
    data: A list of benchmark Dataclasses
    """
    budgets: Dict[int, Dict[int, str]] = {}

    for item in data:
        if item.budget_in_bytes not in budgets:
            budgets[item.budget_in_bytes] = {}
        if item.overall_costs not in budgets[item.budget_in_bytes].keys():
            budgets[item.budget_in_bytes][item.overall_costs] = []
        budgets[item.budget_in_bytes][item.overall_costs].append(item.sequence)

    return budgets


def equal_index_configs_by_budget(data):
    """
    This function organizes dataclasses into a dictionary, first by budget then by overall costs.
    """
    budgets: Dict[int, Dict[int, str]] = {}
    for item in data:
        if item.budget_in_bytes not in budgets:
            budgets[item.budget_in_bytes] = {}
        sorted_indexes = str(sorted(item.selected_indexes))
        if sorted_indexes not in budgets[item.budget_in_bytes].keys():
            budgets[item.budget_in_bytes][sorted_indexes] = []
        budgets[item.budget_in_bytes][sorted_indexes].append(item.sequence)

    return budgets


def indexes_by_budget(data: List[BenchmarkDataclass]):
    """
    This function finds all selected indexes for a given budget and the algorithms that selected it.
    """
    budgets = {}
    for item in data:
        if item.budget_in_bytes not in budgets:
            budgets[item.budget_in_bytes] = {}
        for index in item.selected_indexes:
            if index not in budgets[item.budget_in_bytes].keys():
                budgets[item.budget_in_bytes][index] = []
            budgets[item.budget_in_bytes][index].append(item.sequence)

    return budgets


def costs_by_query(data: List[BenchmarkDataclass]):
    """For every Budget, for every query, what were the costs that an algorithm had for it."""
    budgets = {}
    for item in data:
        if item.budget_in_bytes not in budgets:
            budgets[item.budget_in_bytes] = {}
        for query_id in item.costs_by_query:
            if query_id not in budgets[item.budget_in_bytes].keys():
                budgets[item.budget_in_bytes][query_id] = {}
            budgets[item.budget_in_bytes][query_id].update(
                {item.sequence: item.costs_by_query[query_id]["Cost"]}
            )
    return budgets
