# One Dimensional Derivative Free Optimization

Individual programming project for **Methods of Optimization and Decision Making**.

The project implements uniform search, a sequential grid scan, dichotomy,
golden section, and Fibonacci search. All five receive an arbitrary Python
function, interval, and tolerance. No optimizer library or derivative is used.

## Quick start on Windows CMD

Extract the ZIP first. Open CMD in the extracted `optimization_project` folder
(the folder that contains `main.py`). Run:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
python research.py
python -m unittest -v
```

Python 3.10 or newer is required. The supplied results were generated with
Python 3.12.14. Matplotlib is needed only for figures; the algorithms and
validation tests use the Python standard library.

For numerical results without installing plotting packages:

```bat
python main.py --no-plots
```

## What to open for the presentation

- `report/Optimization_Report.pdf` or the editable Word version.
- `results/objective.png` for the graph.
- `results/results.txt` for both experiment tables.
- `problem.py` to show the replaceable problem definition.
- `algorithms.py` to explain the five methods and evaluation counter.
- `Presentation_Guide_FA.md` for Persian explanations and a short English script.
- `Optimization_Demo.ipynb` for an optional step-by-step notebook in VS Code.

The notebook imports the same code as the command-line application. Select
your Python environment as its kernel, and run the cells from the top. If
VS Code requests a kernel package, run `python -m pip install ipykernel` in
the activated environment.

## Live change in class

Edit only `problem.py`: `objective_function`, `A`, `B`, `DELTAS`, and the
display label `DESCRIPTION`. Set `REFERENCE_X` and `REFERENCE_F` to `None`
unless the exact answer for the new objective is known. These two values are
used only for validation and figures; the algorithms never read them.

Save the file and run:

```bat
python main.py --output results_live
```

You may also change the interval or requested accuracies from CMD:

```bat
python main.py --a -2 --b 5 --delta 0.1 0.01 0.001 --output results_live
```

Example of a different problem to rehearse:

```python
def objective_function(x):
    return (x - 0.37)**2 + 2.0

A = -1.0
B = 2.0
DELTAS = (0.1, 0.01, 0.001)
DESCRIPTION = "f(x) = (x - 0.37)^2 + 2"
REFERENCE_X = 0.37
REFERENCE_F = 2.0
```

Restore the original example before presenting the supplied report. Running
the program regenerates numerical outputs and plots, but does not rewrite
the Word/PDF report automatically.

## Accuracy and counting conventions

`delta` is an absolute tolerance in the **location x**, not in the objective
value. Each method returns a bracket `[left, right]` of width at most
`2*delta`, then reports its midpoint. Under strict unimodality and reliable
function comparisons, the midpoint error is at most `delta`.

Uniform and sequential search use a grid step no larger than `delta`.
Dichotomy uses two probes separated by `0.1*delta`. Fibonacci uses
`F[0]=0, F[1]=1` and a final perturbation of `0.01*initial_width/F[n]`;
the selected horizon includes this extra width in its stopping guarantee.

`N search` counts actual objective evaluations during the search.
`N total = N search + 1` includes one final evaluation at the reported
midpoint, consistently for every method. This reporting call is deliberately
counted even when the midpoint was sampled earlier. Plotting, validation,
and independent runs use separate evaluations outside these counters.
Golden and Fibonacci reuse stored values inside their search loops.

The output rounds x according to delta, with one guard decimal. The
guarantee applies to the unrounded midpoint. `results.json` retains full
precision for reproducibility. Printed equal values of f(x) can hide small
differences; consult the error or bracket before drawing a conclusion.

## Sequential search convention

Here, "sequential scan" means a left-to-right scan of the same grid as
uniform search, stopping at the first non-decreasing value and retaining
the neighboring bracket. It is not an expanding-step bracketing algorithm.
Check this definition against the lecturer's exact slide or pseudocode.

## Additional research

`python main.py` compares one long Fibonacci run with restarted searches
whose maximum stage indices are 6 and 8. A restart continues on the retained
interval and discards previously stored values. The last stage can use a
shorter horizon. Only the final midpoint is evaluated for reporting.

`python research.py` compares golden section, one F15 pass, and two F8
passes, each with exactly 14 search evaluations. Results are stored in
`results/fixed_budget.json`. This separates interval efficiency from lucky
closeness of an estimate to the exact answer.

## Validation and limits

`python -m unittest -v` runs five test groups, including 269 full accuracy
and accounting scenarios, 65 Fibonacci budget checks, boundary minima,
nonsmooth objectives, symmetric ties, invalid inputs, and a very short
initial interval. Every retained bracket is checked against a known answer.

The guarantees assume a deterministic, finite, strictly unimodal objective.
A graph supports the example but cannot prove an arbitrary function is
unimodal. Multimodal or noisy functions need a different analysis. Extremely
small tolerances can fail because different function values become
indistinguishable in floating-point arithmetic. An evaluation cap prevents
accidentally requesting a grid with millions of samples.

## Sources

1. University of Illinois Urbana-Champaign, CS 357, *Optimization*, Spring 2023.
   https://courses.physics.illinois.edu/cs357/sp2023/notes/ref-15-opt_nd.html
2. E. Bertolazzi, University of Trento, *One-Dimensional Minimization*, May 2008.
   https://e.bertolazzi.dii.unitn.it/corso-PHD/AA2007_2008_UOPT/lucidi/slides-m1D-1x2.pdf
3. M. Avriel and D. J. Wilde, *Optimality Proof for the Symmetric Fibonacci
   Search Technique*, The Fibonacci Quarterly 4(3), 1966, pp. 265-269.
   https://www.fq.math.ca/Scanned/4-3/avriel.pdf

The formulas for the selected objective, the error convention, the terminal
perturbation bound, and all numerical tables are derived or computed in this
project. The implementation is written directly in Python, without copying
an optimizer library implementation.

Suggested commit message if you add this project to your archive:

```text
Add derivative-free one-dimensional optimization project and report
```
