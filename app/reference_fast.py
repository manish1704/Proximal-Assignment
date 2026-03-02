"""Reference fast implementation using numpy.

This module provides a vectorized implementation used by the verifier as
the gold-standard fast implementation.
"""
from typing import Sequence, Tuple
import numpy as np


def pairwise_sum(points: Sequence[Tuple[float, float]]) -> float:
    arr = np.asarray(points, dtype=float)
    # compute pairwise differences via broadcasting in a memory-efficient way
    # using (x[i]-x[j])**2 + (y[i]-y[j])**2 and summing upper triangle
    x = arr[:, 0]
    y = arr[:, 1]
    dx = x[:, None] - x[None, :]
    dy = y[:, None] - y[None, :]
    dist = np.sqrt(dx * dx + dy * dy)
    # sum only upper triangle to match the naive implementation
    return float(np.triu(dist, k=1).sum())


if __name__ == "__main__":
    import random
    pts = [(random.random(), random.random()) for _ in range(1000)]
    print(pairwise_sum(pts))
