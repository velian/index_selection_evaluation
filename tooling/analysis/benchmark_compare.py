"""
Compares different benchmarks.
"""
from typing import Any, Dict, List
from tooling.benchmark_dataclass import BenchmarkDataclass


def compare_benchmarks(
    bench1: BenchmarkDataclass, bench2: BenchmarkDataclass
) -> Dict[str, Any]:
    """
    Compares two benchmarks and returns a dictionary containing the comparison results.

    Args:
        bench1 (BenchmarkDataclass): The first benchmark to compare.
        bench2 (BenchmarkDataclass): The second benchmark to compare.

    Returns:
        A dictionary containing the comparison results.

    Raises:
        ValueError: If the benchmarks have different queries.

    """
    if set(bench1.algorithm_indexes_by_query.keys()) != set(
        bench2.algorithm_indexes_by_query.keys()
    ):
        raise ValueError("Benchmarks have different queries")

    results = {
        "queries": {},
        "shared_indexes": [],
        "1only": [],
        "2only": [],
        "comparison_meta": {
            "budget1": bench1.budget_in_bytes,
            "budget2": bench2.budget_in_bytes,
            "sequence1": bench1.sequence,
            "sequence2": bench2.sequence,
        },
    }

    for query, algorithm_indexes1 in bench1.algorithm_indexes_by_query.items():
        algorithm_indexes2 = bench2.algorithm_indexes_by_query[query]

        results["queries"][query] = {
            "equal": sorted(algorithm_indexes1) == sorted(algorithm_indexes2),
            "shared": list(
                set(algorithm_indexes1).intersection(set(algorithm_indexes2))
            ),
            "1only": list(set(algorithm_indexes1).difference(set(algorithm_indexes2))),
            "2only": list(set(algorithm_indexes2).difference(set(algorithm_indexes1))),
            "cost_difference": bench2.costs_by_query[query]["Cost"]
            - bench1.costs_by_query[query]["Cost"],
            "q2_cost_percentage": bench2.costs_by_query[query]["Cost"]
            / bench1.costs_by_query[query]["Cost"]
            * 100,
        }

    results["shared_indexes"] = list(
        set(bench1.selected_indexes).intersection(set(bench2.selected_indexes))
    )
    results["1only"] = list(
        set(bench1.selected_indexes).difference(set(bench2.selected_indexes))
    )
    results["2only"] = list(
        set(bench2.selected_indexes).difference(set(bench1.selected_indexes))
    )
    results["cost_requests_difference"] = bench2.cost_requests - bench1.cost_requests
    results["index_config_1"] = bench1.selected_indexes
    results["index_config_2"] = bench2.selected_indexes

    # Calculate overall cost difference and percentage
    results["overall_costs_diff"] = bench2.overall_costs - bench1.overall_costs
    results["overall_costs_percentage"] = (
        bench2.overall_costs / bench1.overall_costs * 100
    )

    return results


def compare_benchmark_sequence(benchmarks: List[BenchmarkDataclass]) -> List[dict]:
    """Compares a sequence of benchmarks, and returns their comparison dicts"""

    comparisons = []
    for i in range(1, len(benchmarks)):
        comparisons.append(compare_benchmarks(benchmarks[i - 1], benchmarks[i]))
    return comparisons


def compare_benchmark_sequence_with_single(
    benchmark: BenchmarkDataclass, benchmarks: List[BenchmarkDataclass]
) -> List[dict]:
    """
    Compares a sequence of benchmarks against a single other benchmark.
    Mostly intended to get values vs 'no index'.
    """
    comparisons = []
    for compare in benchmarks:
        comparisons.append(compare_benchmarks(benchmark, compare))
    return comparisons


def comparison_affected_queries(comparison_dict: Dict[str, Any]) -> List[str]:
    """This takes a comparison dict as upstairs and returns a dict of only the affected queries"""
    affected_queries = {}

    for query in comparison_dict["queries"]:
        if not comparison_dict["queries"][query]["equal"]:
            affected_queries[query] = comparison_dict["queries"][query]

    return affected_queries
