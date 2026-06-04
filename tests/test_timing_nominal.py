"""FM-01 — Inference latency budget.

Validates that AI event detector inference completes within the host latency
threshold defined in config/thresholds/latency.yaml (<= 20 ms nominal).
"""
import pytest


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_inference_latency_within_budget():
    raise NotImplementedError
