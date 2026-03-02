#!/bin/bash

# Use this file to install test dependencies and run the tests.
# It will be copied to /tests/test.sh and run from the working directory.

set -euo pipefail

# Update package manager
apt-get update
apt-get install -y --no-install-recommends curl python3-pip python3-dev

# ensure numpy is available for the reference implementation
pip3 install --no-cache-dir numpy pytest==8.4.1 pytest-json-ctrf==0.3.5

# Create logs directory
mkdir -p /logs/verifier

# run pytest (will write /logs/verifier/score.txt)
if pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA; then
  TEST_PASSED=1
else
  TEST_PASSED=0
fi

# If the verifier wrote a numeric score, pass that through to reward.txt
if [ -f /logs/verifier/score.txt ]; then
  SCORE=$(cat /logs/verifier/score.txt | tr -d '\n')
  # clamp to [0,1]
  CLAMPED=$(python3 -c "s = float('$SCORE') if '$SCORE' else 0.0; print(f'{max(0.0, min(1.0, s)):.6f}')")
  echo "$CLAMPED" > /logs/verifier/reward.txt
else
  # test failed before producing a score
  echo 0.0 > /logs/verifier/reward.txt
fi

echo "Test completed. Score: $(cat /logs/verifier/reward.txt)"

exit 0

