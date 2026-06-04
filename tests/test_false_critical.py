"""FM-03 — False critical: NOMINAL input → CRITICAL_EVENT output.

Validates that the AI node does not output CRITICAL_EVENT on a NOMINAL input.
False critical rate must not exceed the threshold in config/thresholds/rates.yaml (<= 1%).
"""
import pytest


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_false_critical_rate_within_threshold():
    raise NotImplementedError
