"""FM-04 — Output confidence outside contract range.

Validates that every /ai/event_class message satisfies the confidence bounds
defined in config/contracts/event_class_output.yaml.
Contract compliance must be 100%.
"""
import pytest


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_confidence_within_contract_bounds():
    raise NotImplementedError


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_contract_compliance_is_100_percent():
    raise NotImplementedError
