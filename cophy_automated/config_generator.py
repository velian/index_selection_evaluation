import json
import os
from typing import List


def generate_cophy_config_files(
    benchmark_name: str,
    scale_factor: str,
    max_index_width: int,
    max_indexes_per_query: int,
    path: str,
    database: str = "postgres",
    timeout: int = 300,
) -> None:
    """
    Benchmark Name -> One of tpch, tpcds
    Scale Factor -> Scale for Benchmark
    max_index_width -> max width of generated index
    max_indexes_per_query -> Kdoy?
    Path -> the folder into which the resulting file should be written to.
    Database -> Which database to set
    """

    match benchmark_name:
        case "tpch":
            # TPCH has 22 queries
            queries = generate_queries(22)
        case "tpcds":
            # TPCDS has 99 queries
            queries = generate_queries(99)
        case _:
            queries = []
            raise RuntimeError(
                "Currently only tpc-h and -ds are supported for config gen."
            )

    config_dict = {}
    config_dict["database_system"] = database
    config_dict["benchmark_name"] = benchmark_name
    config_dict["scale_factor"] = scale_factor
    config_dict["algorithms"] = [
        {
            "name": "cophy",
            "parameters": {
                "max_index_width": max_index_width,
                "max_indexes_per_query": max_indexes_per_query,
                "target_path": path,
                "benchmark": benchmark_name #this is exclusively for naming the result files. I have not found a good place to get that info from the overall ocnfig within the algorithm
            },
            "timeout": timeout,
        }
    ]
    config_dict["queries"] = queries

    os.makedirs(path + '/configs', exist_ok=True)

    with open(path + f'/configs/{benchmark_name}_{max_index_width}_{max_indexes_per_query}_config.json', 'w+') as file:
        file.write(json.dumps(config_dict, indent=4))

def generate_queries(number: int) -> List[int]:
    queries = []
    for i in range(0, number):
        # +1 ensures that its 1 - number
        if i + 1 in [2, 17, 20]:
            continue
        queries.append(i + 1)
    return queries
