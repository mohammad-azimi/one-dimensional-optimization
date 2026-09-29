"""Run: python main.py [--delta 0.01] [--a -2 --b 5] [--no-plots]."""
import argparse
import json
import math
from pathlib import Path
import sys

import problem
from algorithms import METHODS, restarted_fibonacci


def decimals(delta):
    return max(0, math.ceil(-math.log10(delta))) + 1


def table(results):
    rows = []
    for r in results:
        p = decimals(r.delta)
        rows.append([f"{r.delta:g}", r.method, f"{r.x:.{p}f}",
                     f"{r.fx:.{p + 1}f}", str(r.search_evaluations),
                     str(r.total_evaluations), f"{r.error_bound:.2g}"])
    headers = ["delta", "Method", "x estimate", "f(x)",
               "N search", "N total", "Error bound"]
    widths = [max(len(v) for v in col) for col in zip(headers, *rows)]
    line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
    divider = "-+-".join("-" * w for w in widths)
    body = [" | ".join(v.ljust(w) for v, w in zip(row, widths))
            for row in rows]
    return "\n".join([line, divider, *body])


def run_experiments(a, b, deltas, output, plots=True):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    results = [method(problem.objective_function, a, b, delta)
               for delta in deltas for method in METHODS]
    research = []
    for delta in deltas:
        research.append(METHODS[-1](problem.objective_function, a, b, delta))
        for index in (6, 8):
            research.append(restarted_fibonacci(
                problem.objective_function, a, b, delta, index))
    metadata = {"description": problem.DESCRIPTION, "a": a, "b": b,
                "deltas": list(deltas), "reference_x": problem.REFERENCE_X,
                "reference_f": problem.REFERENCE_F,
                "python": sys.version.split()[0],
                "tolerance": "absolute x error; bracket width <= 2*delta",
                "counting": "search calls plus one reporting call"}
    payload = {"problem": metadata,
               "results": [r.to_dict() for r in results],
               "research": [r.to_dict() for r in research]}
    (output / "results.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8")
    text = (problem.DESCRIPTION + f"\nInterval: [{a:g}, {b:g}]\n\n"
            + table(results) + "\n\nFIBONACCI RESTART EXPERIMENT\n"
            + table(research) + "\n\nN total = N search + 1 reporting call.\n"
            + "Error bound applies to the unrounded midpoint.\n")
    (output / "results.txt").write_text(text, encoding="utf-8")
    print(text)
    if problem.REFERENCE_X is not None:
        reference = problem.REFERENCE_X
        passed = all(r.left - 1e-12 <= reference <= r.right + 1e-12
                     and abs(r.x - reference) <= r.delta * (1 + 1e-10)
                     for r in results + research)
        print("Reference check:", "PASS" if passed else "FAIL")
        if not passed:
            print("Check the interval and reference metadata in problem.py.")
    if plots:
        from plots import make_plots
        make_plots(problem.objective_function, payload, output)
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a", type=float, default=problem.A)
    parser.add_argument("--b", type=float, default=problem.B)
    parser.add_argument("--delta", type=float, nargs="+", default=problem.DELTAS)
    parser.add_argument("--output", default="results")
    parser.add_argument("--no-plots", action="store_true")
    args = parser.parse_args()
    try:
        run_experiments(args.a, args.b, args.delta, args.output,
                        plots=not args.no_plots)
    except (ValueError, ArithmeticError) as error:
        parser.exit(2, f"Input or numerical error: {error}\n")
    except ImportError:
        parser.exit(2, "Plotting needs matplotlib. Install requirements.txt "
                    "or run with --no-plots.\n")


if __name__ == "__main__":
    main()
