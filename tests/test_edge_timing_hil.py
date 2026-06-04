"""FM-08 — STM32 micro-ROS latency exceeds budget.

Validates that the STM32 edge node inference and communication latency
stays within the thresholds in config/thresholds/latency.yaml
(<= 50 ms nominal, <= 75 ms stressed).
"""
import pytest


@pytest.mark.skip(reason="Step 9 — STM32 HIL required")
def test_edge_inference_latency_nominal():
    raise NotImplementedError


@pytest.mark.skip(reason="Step 9 — STM32 HIL required")
def test_edge_inference_latency_stressed():
    raise NotImplementedError
