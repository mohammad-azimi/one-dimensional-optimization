import math


def objective_function(x):
    """A nonquadratic, strictly unimodal example."""
    t = x - math.sqrt(2.0)
    return 1.0 + t**2 + 0.2 * t**4


A = -2.0
B = 5.0
DELTAS = (0.1, 0.01, 0.001)
DESCRIPTION = "f(x) = 1 + (x - sqrt(2))^2 + 0.2*(x - sqrt(2))^4"

# Validation metadata ONLY. Algorithms never receive these values.
# Set both to None when the new problem's exact answer is unknown.
REFERENCE_X = math.sqrt(2.0)
REFERENCE_F = 1.0