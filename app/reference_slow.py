"""Reference slow implementation (copy of initial naive version).

This file contains the original naive implementation. The verifier uses it
as the baseline to compute how much improvement an agent achieved.
"""
from typing import Sequence, Tuple


def pairwise_sum(points: Sequence[Tuple[float, float]]) -> float:
    total = 0.0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            total += (dx * dx + dy * dy) ** 0.5
    return total
