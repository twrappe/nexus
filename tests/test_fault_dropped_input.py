"""FM-05 — Dropped input → stale output propagated.

Validates that when /sensor/stream is absent for N cycles the AI node
flags its output as stale and does not silently republish.
"""
import pytest


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_stale_output_flagged_on_dropped_input():
    raise NotImplementedError


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_no_silent_republish_on_dropped_input():
    raise NotImplementedError
