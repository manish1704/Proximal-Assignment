Perf-optimization eval task

Goal
----
Create a performance-engineering evaluation task for coding agents. The agent's job is
to optimize a provided Python function for speed without breaking correctness.

What lives in this repo
-----------------------
- `app/target.py` -- the function to optimize (naive nested-loop implementation)
- `app/reference_fast.py` -- a vectorized numpy gold implementation used by the verifier
- `app/reference_slow.py` -- the baseline naive implementation used to compute possible improvement
- `tests/test_outputs.py` -- verifier: checks correctness and writes a numeric score
- `tests/test.sh` -- installs deps, runs pytest, and writes `/logs/verifier/reward.txt` with the numeric score

How scoring works
-----------------
1. Verifier ensures the agent's output matches the fast reference (correctness required).
2. The verifier measures runtimes for the slow baseline, the reference fast, and the agent's implementation.
3. Score is the fraction of the possible improvement (slow->fast) achieved by the agent. Value in [0,1].

How to test locally
-------------------
1. Create a Python venv and activate it.
2. Install `numpy` and `pytest`.
3. Run `pytest tests/test_outputs.py`.

How to run in Harbor
---------------------

1. Ensure Harbor is installed and configured.
