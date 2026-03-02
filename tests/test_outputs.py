"""Pytest outputs for the perf-optimization task.

Ensure the repository root is on sys.path so `import app` works when pytest
is run from different working directories.
"""
import os
import sys

# insert repo root into sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import time
import math
import random

from app import target, reference_fast, reference_slow


def mean_time(func, args, repeats=3):
    t = []
    for _ in range(repeats):
        start = time.perf_counter()
        func(*args)
        t.append(time.perf_counter() - start)
    return sum(t) / len(t)


def write_reward(score: float):
    log_root = os.environ.get("HARBOR_LOG_DIR")
    if not log_root:
        # If running inside Docker manually, /logs will exist
        if os.path.exists("/logs"):
            log_root = "/logs"
        else:
            # local pytest fallback
            log_root = "./.harbor_logs"

    verifier_dir = os.path.join(log_root, "verifier")
    os.makedirs(verifier_dir, exist_ok=True)

    reward_path = os.path.join(verifier_dir, "reward.txt")
    with open(reward_path, "w") as f:
        f.write(f"{score:.6f}\n")


def test_outputs_and_score(tmp_path):
    """Test correctness and compute performance score for the optimized function.

    Fails completely (score 0) if correctness is broken.
    Scores continuously [0,1] based on how much perf improvement was achieved.
    """
    try:
        # fixed seed for reproducibility
        random.seed(12345)
        n = 1200
        points = [(random.random(), random.random()) for _ in range(n)]

        # compute outputs
        try:
            agent_out = target.pairwise_sum(points)
        except Exception as e:
            raise AssertionError(f"Agent function raised an exception: {e}")

        try:
            fast_out = reference_fast.pairwise_sum(points)
        except Exception as e:
            raise AssertionError(f"Reference implementation failed: {e}")

        # Anti-cheat: disallow trivial delegation to reference implementations
        try:
            with open("app/target.py", "r", encoding="utf-8") as fh:
                tgt_src = fh.read()
        except Exception:
            tgt_src = ""

        banned = [
            "reference_fast",
            "reference_slow",
            "from app.reference_fast",
            "from app.reference_slow",
        ]
        for pat in banned:
            if pat in tgt_src:
                raise AssertionError(
                    f"Trivial cheating detected in app/target.py: contains '{pat}'"
                )

        # correctness checks
        if not isinstance(agent_out, (int, float)):
            raise AssertionError(
                f"Agent output must be numeric, got {type(agent_out)}"
            )

        if not math.isfinite(agent_out):
            raise AssertionError(
                f"Agent output must be finite, got {agent_out}"
            )

        if not math.isclose(agent_out, fast_out, rel_tol=1e-6, abs_tol=1e-9):
            raise AssertionError(
                f"Correctness check failed: agent output {agent_out} != "
                f"reference {fast_out} (diff: {abs(agent_out - fast_out):.2e})"
            )

        # measure runtimes
        repeats = 3
        slow_time = mean_time(reference_slow.pairwise_sum, (points,), repeats)
        fast_time = mean_time(reference_fast.pairwise_sum, (points,), repeats)
        agent_time = mean_time(target.pairwise_sum, (points,), repeats)

        # compute score
        if fast_time <= 0 or agent_time <= 0:
            score = 0.0
        else:
            possible = slow_time / fast_time
            achieved = slow_time / agent_time

            if possible <= 1.0:
                score = 1.0 if achieved >= 1.0 else 0.0
            else:
                score = (achieved - 1.0) / (possible - 1.0)
                score = max(0.0, min(1.0, score))

        write_reward(score)

        assert 0.0 <= score <= 1.0

    except AssertionError:
        write_reward(0.0)
        raise