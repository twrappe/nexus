# Validation Specification

Top-level validation specification for NEXUS.
Source of truth: `config/validation_spec.yaml`.

<!-- TODO: auto-generate or expand from config/validation_spec.yaml -->

## Scope

NEXUS validates an AI-driven mode switching pipeline across:

1. Classification correctness under nominal conditions
2. Mode controller response correctness
3. Timing budget compliance
4. Fault injection and graceful degradation
5. Critical event detection (highest priority)
6. False critical rate
7. Quantization divergence (STM32 HIL)
8. Operational scenario correctness

## Thresholds

See `config/thresholds/latency.yaml` and `config/thresholds/rates.yaml`.

| Parameter | Threshold | FM |
| --- | --- | --- |
| Inference latency — host | ≤ 20 ms | FM-01 |
| Inference latency — STM32 nominal | ≤ 50 ms | FM-08 |
| Inference latency — STM32 stressed | ≤ 75 ms | FM-08 |
| Mode transition latency | ≤ 10 ms | FM-01 |
| INT8 vs FP32 agreement | ≥ 98% | FM-02 |
| Critical event miss rate | **0%** — unconditional failure | FM-06 |
| False critical rate | ≤ 1% | FM-03 |
| Output contract compliance | 100% | FM-04 |
| Autonomous CRITICAL recovery | **0 occurrences** — unconditional failure | FM-09 |
