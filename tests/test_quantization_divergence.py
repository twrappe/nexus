"""FM-02 — INT8 vs FP32 classification divergence.

Validates that the STM32 INT8 model agrees with the host FP32 model at or
above the threshold defined in config/thresholds/rates.yaml (>= 98%).
Any NORMAL<->CRITICAL disagreement is a critical divergence.
"""
import pytest


@pytest.mark.skip(reason="Step 7 — STM32 HIL required")
def test_quantization_agreement_rate():
    raise NotImplementedError


@pytest.mark.skip(reason="Step 7 — STM32 HIL required")
def test_no_critical_normal_divergence():
    raise NotImplementedError
