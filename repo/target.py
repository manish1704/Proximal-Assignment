"""Target module: contains the function the agent should optimize.

The initial implementation is intentionally naive (pure Python loops).
Agents are expected to optimize this function while keeping the API the same.
"""
from typing import Sequence, Tuple


def pairwise_sum(points: Sequence[Tuple[float, float]]) -> float:
    """Compute sum of Euclidean distances between all pairs of 2D points.

    Naive O(n^2) Python implementation using nested loops. This is the
    function participants/agents should optimize.
    """
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


if __name__ == "__main__":
    # quick smoke run
    pts = [(i * 0.1, i * 0.2) for i in range(200)]
    print(pairwise_sum(pts))
