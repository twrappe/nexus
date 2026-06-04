"""FM-09 — Autonomous recovery from CRITICAL state.

Validates that the mode controller never autonomously transitions out of
CRITICAL without operator intervention. Zero occurrences permitted.
"""
import pytest


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_critical_state_is_terminal():
    raise NotImplementedError


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_no_autonomous_recovery_from_critical():
    """Any autonomous recovery is an unconditional failure."""
    raise NotImplementedError
