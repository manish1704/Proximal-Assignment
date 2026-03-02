#!/bin/bash

# Use this file to install test dependencies and run the tests.
# It will be copied to /tests/test.sh and run from the working directory.

set -euo pipefail

# Update package manager
apt-get update
apt-get install -y --no-install-recommends curl python3-pip python3-dev

# ensure numpy is available for the reference implementation
# Use the virtualenv's pip to ensure packages go to the right location
/opt/venv/bin/pip install --no-cache-dir numpy pytest==8.4.1 pytest-json-ctrf==0.3.5

# Create logs directory
mkdir -p /logs/verifier

# Use the virtualenv's python to ensure all imports work correctly
if /opt/venv/bin/python -m pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA; then
  TEST_PASSED=1
else
  TEST_PASSED=0
fi

# If the verifier wrote a numeric score, pass that through to reward.txt
if [ -f /logs/verifier/reward.txt ]; then
  SCORE=$(cat /logs/verifier/reward.txt | tr -d '\n')
  # clamp to [0,1]
  CLAMPED=$(python3 -c "s = float('$SCORE') if '$SCORE' else 0.0; print(f'{max(0.0, min(1.0, s)):.6f}')")
  echo "$CLAMPED" > /logs/verifier/reward.txt
else
  # test failed before producing a score
  echo 0.0 > /logs/verifier/reward.txt
fi

# Fix permissions on session files to ensure they're readable by the host
# This addresses issues where Docker container creates files with restrictive permissions
if [ -d "/app/jobs" ]; then
  chmod -R 755 /app/jobs || true
  find /app/jobs -type f -exec chmod 644 {} \; || true
fi

echo "Test completed. Score: $(cat /logs/verifier/reward.txt)"

exit 0

