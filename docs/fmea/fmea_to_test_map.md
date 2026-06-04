# FMEA to Test Map

Traceability from each failure mode to its test file, validator module, and
YAML scenario.

| FM ID | Test File | Validator | Scenario |
| --- | --- | --- | --- |
| FM-01 | `tests/test_timing_nominal.py` | `validation/timing_validator.py` | — |
| FM-02 | `tests/test_quantization_divergence.py` | `validation/divergence_analyzer.py` | `scenarios/quantization_stress.yaml` |
| FM-03 | `tests/test_false_critical.py` | `validation/contract_validator.py` | `scenarios/nominal_steady_state.yaml` |
| FM-04 | `tests/test_contract_confidence.py` | `validation/contract_validator.py` | — |
| FM-05 | `tests/test_fault_dropped_input.py` | `validation/fault_propagation.py` | `scenarios/comms_dropout.yaml` |
| FM-06 | `tests/test_critical_event_miss.py` | `validation/mode_transition_validator.py` | `scenarios/critical_event.yaml` |
| FM-07 | `tests/test_fault_ood_input.py` | `validation/fault_propagation.py` | `scenarios/ood_input.yaml` |
| FM-08 | `tests/test_edge_timing_hil.py` | `validation/timing_validator.py` | — |
| FM-09 | `tests/test_critical_terminal.py` | `validation/mode_transition_validator.py` | `scenarios/critical_event.yaml` |

<!-- TODO: add coverage gap analysis column -->
