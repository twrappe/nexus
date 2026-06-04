"""FM-06 — Critical event miss: CRITICAL_EVENT input → NOMINAL output.

Highest severity failure (S=10). Any single miss is an unconditional test
failure regardless of overall pass rate. Maps to FM-06.
"""
import pytest


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_critical_event_never_classified_as_nominal():
    """Any miss here is an unconditional failure — no pass-rate tolerance."""
    raise NotImplementedError
