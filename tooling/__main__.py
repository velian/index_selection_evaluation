from tooling.ilp_solving.solve_automation import solve, load_solver_config
from tooling.util import convert_gb_to_b
from pathlib import Path

solve(
    Path(
        "/Users/Julius/masterarbeit/J-Index-Selection/ILP/500_tpch_db2advis_3_cache_input.txt"
    ),
    load_solver_config(),
    convert_gb_to_b(10),
)
