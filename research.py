"""Compare interval lengths at the same search budget of 14 calls."""
import json
import math
from pathlib import Path

import problem
from algorithms import (EvaluationCounter, _fibonacci_pass,
                        _fibonacci_numbers, golden_section_search)


def fixed_budget_experiment(output="results"):
    a, b = problem.A, problem.B
    length = b - a
    budget = 14
    ratio = (math.sqrt(5) - 1) / 2
    golden_width = length * ratio**(budget - 1)
    golden = golden_section_search(problem.objective_function, a, b,
                                    golden_width * (1 + 1e-10) / 2)
    rows = [{"strategy": "Golden section", "search_calls": golden.search_evaluations,
             "width": golden.right - golden.left, "bound": golden_width}]
    for name, stages in (("One Fibonacci F15", [15]),
                         ("Two Fibonacci F8 stages", [8, 8])):
        f = EvaluationCounter(problem.objective_function)
        left, right = a, b
        history = [(0, a, b)]
        bound = length
        for n in stages:
            left, right = _fibonacci_pass(f, left, right, n, history)
            bound *= 1.01 / _fibonacci_numbers(n)[n]
        rows.append({"strategy": name, "search_calls": f.calls,
                     "width": right - left, "bound": bound})
    if any(row["search_calls"] != budget for row in rows):
        raise AssertionError("The fixed-budget comparison is not matched.")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "fixed_budget.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8")
    for row in rows:
        print(f"{row['strategy']:<25} N={row['search_calls']:2d}  "
              f"width={row['width']:.6f}  bound={row['bound']:.6f}")
    print("All rows use 14 search calls; no extra reporting calls are compared.")
    return rows


if __name__ == "__main__":
    fixed_budget_experiment()
