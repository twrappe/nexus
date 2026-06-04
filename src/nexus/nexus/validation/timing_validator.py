"""Inference and mode transition latency validator — FM-01, FM-08.

Thresholds loaded from config/thresholds/latency.yaml.
Step 5 of build order.
"""
# TODO: implement


def validate_inference_latency(latency_ms: float) -> bool:
    """Return True if inference latency is within the host budget."""
    raise NotImplementedError


def validate_transition_latency(latency_ms: float) -> bool:
    """Return True if mode transition latency is within budget."""
    raise NotImplementedError
