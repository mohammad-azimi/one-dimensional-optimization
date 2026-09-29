"""Independent accuracy, bracket, accounting and edge-case checks.

Run: python -m unittest -v
No third-party packages are required.
"""
import math
import random
import unittest

from algorithms import (METHODS, restarted_fibonacci, _fibonacci_pass,
                        EvaluationCounter)


class OptimizationTests(unittest.TestCase):
    def check_solution(self, method, function, a, b, delta, exact):
        actual_calls = []

        def observed(x):
            self.assertTrue(a - 1e-12 <= x <= b + 1e-12)
            actual_calls.append(x)
            return function(x)

        result = method(observed, a, b, delta)
        slack = 1e-11 * max(1, abs(a), abs(b))
        self.assertLessEqual(abs(result.x - exact), delta + slack)
        self.assertLessEqual(result.error_bound, delta + slack)
        self.assertLessEqual(result.left - slack, exact)
        self.assertGreaterEqual(result.right + slack, exact)
        self.assertEqual(result.total_evaluations, len(actual_calls))
        self.assertEqual(result.total_evaluations,
                         result.search_evaluations + 1)
        self.assertAlmostEqual(result.fx, function(result.x))
        old_left, old_right = a, b
        for _, left, right in result.history:
            self.assertTrue(old_left - slack <= left <= right <= old_right + slack)
            self.assertTrue(left - slack <= exact <= right + slack)
            old_left, old_right = left, right

    def test_known_minima_and_boundaries(self):
        cases = [
            (lambda x: (x - math.sqrt(2))**2, -2, 5, math.sqrt(2)),
            (lambda x: abs(x - 0.37), -1, 2, 0.37),
            (lambda x: x + 1 / x, 0.2, 4, 1.0),
            (lambda x: (x + 0.73)**4, -2, 3, -0.73),
            (lambda x: (x - 0.4)**2 * (1 if x < 0.4 else 7), -2, 4, 0.4),
            (lambda x: x, -2, 5, -2),
            (lambda x: -x, -2, 5, 5),
            (lambda x: x*x, -1, 1, 0),
        ]
        for method in (*METHODS, restarted_fibonacci):
            for function, a, b, exact in cases:
                for delta in (0.1, 0.01, 0.001):
                    with self.subTest(method=method.__name__, exact=exact, delta=delta):
                        self.check_solution(method, function, a, b, delta, exact)

    def test_seeded_asymmetric_objectives(self):
        rng = random.Random(20260928)
        for _ in range(25):
            exact = rng.uniform(-1.9, 4.9)
            scale = rng.uniform(0.2, 9)
            def objective(x, center=exact, weight=scale):
                t = x - center
                return t*t * (1 if t < 0 else weight) + 0.1*t**4
            for method in METHODS:
                self.check_solution(method, objective, -2, 5, 0.002, exact)

    def test_small_initial_interval(self):
        for method in METHODS:
            result = method(lambda x: x*x, -0.01, 0.01, 0.1)
            self.assertEqual(result.search_evaluations, 0)
            self.assertEqual(result.total_evaluations, 1)

    def test_fibonacci_budget_and_terminal_probe(self):
        for n in range(3, 16):
            for center in (0.0, 0.13, 0.5, 0.87, 1.0):
                seen = []
                def objective(x):
                    seen.append(x)
                    return (x - center)**2
                counter = EvaluationCounter(objective)
                history = [(0, 0.0, 1.0)]
                a, b = _fibonacci_pass(counter, 0.0, 1.0, n, history)
                self.assertEqual(counter.calls, n - 1)
                self.assertGreater(len(set(seen)), 1)
                self.assertTrue(a - 1e-12 <= center <= b + 1e-12)
                fib_a, fib_b = 0, 1
                for _ in range(n):
                    fib_a, fib_b = fib_b, fib_a + fib_b
                self.assertLessEqual(b - a, 1.01 / fib_a + 1e-12)

    def test_invalid_inputs(self):
        for method in METHODS:
            for a, b, delta in ((2, 1, .1), (1, 1, .1), (0, 1, 0),
                                (0, 1, -.1), (0, math.inf, .1),
                                (0, 1, math.nan), (1, 2, 1e-20)):
                with self.assertRaises(ValueError):
                    method(lambda x: x*x, a, b, delta)
            with self.assertRaises(ValueError):
                method(lambda x: math.nan, 0, 1, .01)


if __name__ == "__main__":
    unittest.main()
