"""Derivative-free interval minimization using only the standard library.

Assumptions: finite deterministic values, strict decrease before the unique
minimum and strict increase after it. A boundary minimum is also allowed.
delta means absolute error in x. All methods return a bracket of width
at most 2*delta, and report its midpoint. Plotting is not counted.
"""
from dataclasses import dataclass, asdict
import math


class EvaluationCounter:
    """Count actual objective calls, including one final reporting call."""

    def __init__(self, function, limit=2_000_000):
        self.function = function
        self.calls = 0
        self.limit = limit

    def __call__(self, x):
        if self.calls >= self.limit:
            raise ValueError("Evaluation limit exceeded; increase delta.")
        self.calls += 1
        value = float(self.function(x))
        if not math.isfinite(value):
            raise ValueError(f"Objective is not finite at x={x!r}.")
        return value


@dataclass
class Result:
    method: str
    delta: float
    x: float
    fx: float
    left: float
    right: float
    search_evaluations: int
    total_evaluations: int
    stages: int
    history: list

    @property
    def error_bound(self):
        return (self.right - self.left) / 2.0

    def to_dict(self):
        return {**asdict(self), "error_bound": self.error_bound}


def _setup(function, a, b, delta):
    if not all(math.isfinite(v) for v in (a, b, delta)):
        raise ValueError("a, b and delta must be finite.")
    if a >= b or delta <= 0 or not math.isfinite(b - a):
        raise ValueError("Require a < b, delta > 0 and a finite interval.")
    if delta < 32 * max(math.ulp(a), math.ulp(b)):
        raise ValueError("delta is too small for this floating-point scale.")
    counter = EvaluationCounter(function)
    history = [(0, a, b)]  # (search calls, left endpoint, right endpoint)
    return counter, history


def _finish(name, counter, a, b, delta, history, stages=1):
    if b - a > 2 * delta * (1 + 1e-12):
        raise ArithmeticError("Requested bracket width was not reached.")
    x = a + (b - a) / 2
    search_calls = counter.calls
    fx = counter(x)  # Always one reporting call, even if x was sampled.
    return Result(name, delta, x, fx, a, b, search_calls,
                  counter.calls, stages, history)


def _grid(a, b, delta, limit):
    n = max(1, math.ceil((b - a) / delta))
    if n + 2 > limit:
        raise ValueError("Grid too large; increase delta or omit grid methods.")
    return n, (b - a) / n


def uniform_search(function, a, b, delta):
    """Sample the whole grid; bracket its best point by its neighbors."""
    f, history = _setup(function, a, b, delta)
    if b - a <= 2 * delta:
        return _finish("Uniform search", f, a, b, delta, history)
    n, h = _grid(a, b, delta, f.limit)
    best_i, best_value = 0, f(a)
    for i in range(1, n + 1):
        value = f(b if i == n else a + i * h)
        if value < best_value:
            best_i, best_value = i, value
    left = a + max(0, best_i - 1) * h
    right = min(b, a + min(n, best_i + 1) * h)
    history.append((f.calls, left, right))
    return _finish("Uniform search", f, left, right, delta, history)


def sequential_search(function, a, b, delta):
    """Scan left to right; stop at the first non-decreasing grid value."""
    f, history = _setup(function, a, b, delta)
    if b - a <= 2 * delta:
        return _finish("Sequential scan", f, a, b, delta, history)
    n, h = _grid(a, b, delta, f.limit)
    previous = f(a)
    for i in range(1, n + 1):
        x = b if i == n else a + i * h
        current = f(x)
        if current >= previous:
            left, right = a + max(0, i - 2) * h, x
            break
        previous = current
    else:
        left, right = a + (n - 1) * h, b
    history.append((f.calls, left, right))
    return _finish("Sequential scan", f, left, right, delta, history)


def dichotomy_search(function, a, b, delta):
    """Compare two points on either side of the interval midpoint."""
    f, history = _setup(function, a, b, delta)
    separation = 0.1 * delta  # FULL distance between the two probes.
    while b - a > 2 * delta:
        midpoint = a + (b - a) / 2
        x1, x2 = midpoint - separation / 2, midpoint + separation / 2
        if not a < x1 < x2 < b:
            raise ArithmeticError("Dichotomy probes cannot be represented.")
        y1, y2 = f(x1), f(x2)
        if y1 <= y2:
            b = x2
        else:
            a = x1
        history.append((f.calls, a, b))
    return _finish("Dichotomy", f, a, b, delta, history)


def golden_section_search(function, a, b, delta):
    """Reuse one old function value after each interval reduction."""
    f, history = _setup(function, a, b, delta)
    if b - a <= 2 * delta:
        return _finish("Golden section", f, a, b, delta, history)
    ratio = (math.sqrt(5) - 1) / 2
    x1, x2 = b - ratio * (b - a), a + ratio * (b - a)
    y1, y2 = f(x1), f(x2)
    while b - a > 2 * delta:
        if y1 <= y2:
            b, x2, y2 = x2, x1, y1
            history.append((f.calls, a, b))
            if b - a <= 2 * delta:
                break  # Do not evaluate a point that will not be used.
            x1 = b - ratio * (b - a)
            if not a < x1 < x2 < b:
                raise ArithmeticError("Golden-section probes collapsed.")
            y1 = f(x1)
        else:
            a, x1, y1 = x1, x2, y2
            history.append((f.calls, a, b))
            if b - a <= 2 * delta:
                break
            x2 = a + ratio * (b - a)
            if not a < x1 < x2 < b:
                raise ArithmeticError("Golden-section probes collapsed.")
            y2 = f(x2)
    return _finish("Golden section", f, a, b, delta, history)


def _fibonacci_numbers(n):
    numbers = [0, 1]
    while len(numbers) <= n:
        numbers.append(numbers[-1] + numbers[-2])
    return numbers


def _fibonacci_index(length, target):
    # The final distinct probe adds at most 1% to the ideal final width.
    numbers = [0, 1, 1, 2]
    while 1.01 * length / numbers[-1] > target:
        numbers.append(numbers[-1] + numbers[-2])
    return len(numbers) - 1


def _fibonacci_pass(f, a, b, n, history):
    """Use n-1 search calls; final width <= 1.01*(initial width)/F[n]."""
    numbers = _fibonacci_numbers(n)
    unit = (b - a) / numbers[n]
    epsilon = 0.01 * unit
    if n == 3:
        retained = a + (b - a) / 2
        retained_value = f(retained)
    else:
        x1 = a + numbers[n - 2] * unit
        x2 = a + numbers[n - 1] * unit
        y1, y2 = f(x1), f(x2)
        m = n
        while m > 3:
            if y1 <= y2:
                b, x2, y2 = x2, x1, y1
                m -= 1
                history.append((f.calls, a, b))
                if m == 3:
                    retained, retained_value = x2, y2
                    break
                x1 = a + numbers[m - 2] / numbers[m] * (b - a)
                y1 = f(x1)
            else:
                a, x1, y1 = x1, x2, y2
                m -= 1
                history.append((f.calls, a, b))
                if m == 3:
                    retained, retained_value = x1, y1
                    break
                x2 = a + numbers[m - 1] / numbers[m] * (b - a)
                y2 = f(x2)
    # At the terminal Fibonacci ratio the two ideal probes coincide.
    # A distinct nearby probe is necessary; comparing x with itself is wrong.
    probe = retained + epsilon
    if not a < retained < probe < b:
        raise ArithmeticError("Fibonacci final probe cannot be represented.")
    if retained_value <= f(probe):
        b = probe
    else:
        a = retained
    history.append((f.calls, a, b))
    return a, b


def fibonacci_search(function, a, b, delta):
    """Choose one Fibonacci horizon from the requested tolerance."""
    f, history = _setup(function, a, b, delta)
    if b - a > 2 * delta:
        n = _fibonacci_index(b - a, 2 * delta)
        a, b = _fibonacci_pass(f, a, b, n, history)
    return _finish("Fibonacci", f, a, b, delta, history)


def restarted_fibonacci(function, a, b, delta, stage_index=8):
    """Research variant: restart shorter horizons on each retained bracket.

    Reuse values inside a stage, but deliberately discard them at a restart.
    Do not evaluate intermediate midpoints. Report only the final midpoint.
    """
    if not isinstance(stage_index, int) or stage_index < 3:
        raise ValueError("stage_index must be an integer >= 3.")
    f, history = _setup(function, a, b, delta)
    stages = 0
    while b - a > 2 * delta:
        n = min(stage_index, _fibonacci_index(b - a, 2 * delta))
        a, b = _fibonacci_pass(f, a, b, n, history)
        stages += 1
    name = f"Fibonacci restart F{stage_index}"
    return _finish(name, f, a, b, delta, history, stages)


METHODS = (uniform_search, sequential_search, dichotomy_search,
           golden_section_search, fibonacci_search)
