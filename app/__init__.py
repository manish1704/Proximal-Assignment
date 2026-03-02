"""App package for the perf-optimization task."""

from . import target
from . import reference_fast
from . import reference_slow

__all__ = [
    "target",
    "reference_fast",
    "reference_slow",
]
