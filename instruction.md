The function pairwise_sum in repo/target.py is too slow for large inputs.

Optimize it so it runs significantly faster on large matrices (thousands of rows), but do not change its public API or behavior.

It must return exactly the same results as before (same shape, same dtype, numerically equivalent within floating point tolerance).

You can modify anything inside pairwise_sum, but do not change its function signature or import new external libraries beyond what is already available in the repo.

Focus only on performance. Correctness must not regress.