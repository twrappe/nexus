"""FM-07 — OOD input → silent confident NOMINAL output.

Validates that out-of-distribution inputs produce an explicit uncertainty
signal rather than a silent, confident NOMINAL classification.
"""
import pytest


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_ood_input_produces_uncertainty_signal():
    raise NotImplementedError


@pytest.mark.skip(reason="Step 5 — not yet implemented")
def test_ood_input_not_silently_nominal():
    raise NotImplementedError
