# NEXUS — Progress Tracker

> Last updated: 2026-05-01

## Status Summary

**Step 1 of the build order is complete.** All config files — contracts, thresholds, mode definitions, and the top-level validation spec — now exist and are the authoritative source of truth for all validation criteria. Source code has been reset to a clean scaffold; domain enumerations and the HIL validator node remain to be rebuilt on top of the config foundation.

---

## What Exists

### Build & Package Infrastructure — Complete
- [src/nexus/package.xml](src/nexus/package.xml) — ROS2 package manifest
- [src/nexus/setup.py](src/nexus/setup.py) — ament_python setup
- [src/nexus/setup.cfg](src/nexus/setup.cfg)
- micro-ROS agent and message packages built (artifacts in `build/` and `install/`)

### Config Layer — Complete
- [config/validation_spec.yaml](config/validation_spec.yaml) — top-level manifest; full FM registry; links all contracts and thresholds; marks FM-06 and FM-09 as unconditional failures
- [config/mode_definitions.yaml](config/mode_definitions.yaml) — canonical event class and operational mode integer values; `event_class_to_mode` mapping; terminal states
- [config/contracts/event_class_output.yaml](config/contracts/event_class_output.yaml) — `/ai/event_class` message contract; field types, valid values, confidence bounds (FM-01, FM-05)
- [config/contracts/system_mode_output.yaml](config/contracts/system_mode_output.yaml) — `/system/mode` message contract; propagation correctness; CRITICAL terminal constraint (FM-06, FM-09)
- [config/thresholds/latency.yaml](config/thresholds/latency.yaml) — host inference <= 20 ms; STM32 nominal <= 50 ms, stressed <= 75 ms; mode transition <= 10 ms (FM-03, FM-04, FM-11)
- [config/thresholds/rates.yaml](config/thresholds/rates.yaml) — INT8/FP32 agreement >= 98%; critical miss rate = 0; false critical rate <= 1%; contract compliance = 100%; autonomous CRITICAL recovery = 0 (FM-02, FM-06, FM-07, FM-08, FM-09)

---

## What Does Not Exist Yet

### Source Code (`src/nexus/nexus/`)
| File | Purpose | Step |
|------|---------|------|
| `nodes/common/mode.py` | `EventClass`, `OperationalMode`, `EVENT_CLASS_TO_MODE` — mirrors config values | 2 |
| `nodes/stimulus_node.py` | Publishes sensor windows to `/sensor/stream` | 4 |
| `nodes/monitor_node.py` | Orchestrates validator chain | 6 |
| `nodes/reporter_node.py` | Aggregates results, publishes to `/nexus/results` | 6 |
| `stimulus/stream_generator.py` | Synthetic sensor window generation | 4 |
| `stimulus/fault_injector.py` | Injects fault scenarios at stimulus layer | 4 |
| `stimulus/scenario_player.py` | Drives named scenario sequences | 4 |
| `validation/hil_validator.py` | Subscribes to event class + mode; checks FM-04, FM-06, FM-09 | 5 |
| `validation/contract_validator.py` | Output contract compliance (FM-01, FM-05) | 5 |
| `validation/timing_validator.py` | Inference and transition latency (FM-03, FM-04) | 5 |
| `validation/mode_transition_validator.py` | State machine correctness | 5 |
| `validation/fault_propagation_validator.py` | End-to-end fault propagation | 5 |
| `validation/divergence_validator.py` | INT8 vs FP32 agreement (FM-02) | 7 |
| `reporting/fmea_mapper.py` | Maps validation results to FMEA IDs | 6 |
| `reporting/pass_fail_evaluator.py` | Loads thresholds from config; emits pass/fail | 6 |
| `reporting/report_writer.py` | Writes structured test reports | 6 |

### System Under Test (`system_under_test/`) — None exist
| File | Purpose | Step |
|------|---------|------|
| `ai_event_detector_node.py` | Reference AI event detector; subscribes `/sensor/stream`, publishes `/ai/event_class` | 3 |
| `mode_controller_node.py` | Deterministic mode controller; subscribes `/ai/event_class`, publishes `/system/mode` | 3 |

### Tests (`tests/`) — None exist
| File | Failure Mode |
|------|-------------|
| `test_fm01_output_contract.py` | FM-01 |
| `test_fm02_quantization_divergence.py` | FM-02 |
| `test_fm03_inference_latency.py` | FM-03 |
| `test_fm04_mode_transition_latency.py` | FM-04 |
| `test_fm05_silent_degradation.py` | FM-05 |
| `test_fm06_critical_miss.py` | FM-06 |
| `test_fm07_ood_nominal.py` | FM-07 |
| `test_fm08_false_critical.py` | FM-08 |
| `test_fm09_critical_recovery.py` | FM-09 |
| `test_fm10_comms_dropout.py` | FM-10 |
| `test_fm11_stm32_latency.py` | FM-11 |
| `test_fm12_watchdog.py` | FM-12 |

### Config (`config/`) — Partial
| Item | Status |
|------|--------|
| `stimulus_profiles/` subdirectory | Not started |

### Scenarios (`scenarios/`) — None exist
- `nominal_steady_state.yaml`
- `anomaly_recovery.yaml`
- `critical_event.yaml`
- `ood_input.yaml`
- `comms_dropout.yaml`
- `quantization_stress.yaml`

### Launch Files (`launch/`) — None exist
- `nexus_full.launch.py`
- `nexus_timing.launch.py`
- `nexus_fault.launch.py`
- `nexus_hil.launch.py`
- `nexus_scenario.launch.py`

### Firmware (`firmware/`) — None exist
STM32 Nucleo-F446RE micro-ROS + TFLite-Micro C source, headers, and INT8 model files.

### Docs (`docs/`) — None exist
- `docs/fmea/fmea_table.md`
- `docs/contracts/`
- `docs/validation_spec.md`

---

## Build Order

| Step | What | Status |
|------|------|--------|
| 1 | Config — contracts, thresholds, mode definitions, validation spec | **Complete** |
| 2 | Domain enumerations — `mode.py` | Not started |
| 3 | System under test stubs — AI event detector + mode controller | Not started |
| 4 | Stimulus layer — stream generator, fault injector, stimulus node | Not started |
| 5 | First validator end-to-end — FM-06 through reporter | Not started |
| 6 | Reporter node — results aggregation, pass/fail, FMEA mapping | Not started |
| 7 | Remaining host validators — FM-01 through FM-09 | Not started |
| 8 | pytest suite — one file per FM | Not started |
| 9 | STM32 firmware layer — micro-ROS, TFLite-Micro, FM-02, FM-11 | Not started |

---

## Key Validation Thresholds

All thresholds are now in `config/thresholds/`. Authoritative values:

| Parameter | Threshold | File |
|-----------|-----------|------|
| Inference latency — host | <= 20 ms | `latency.yaml` |
| Inference latency — STM32 nominal | <= 50 ms | `latency.yaml` |
| Inference latency — STM32 stressed | <= 75 ms | `latency.yaml` |
| Mode transition latency | <= 10 ms | `latency.yaml` |
| INT8 vs FP32 agreement | >= 98% | `rates.yaml` |
| Critical event miss rate | **0%** — unconditional failure | `rates.yaml` |
| False critical rate | <= 1% | `rates.yaml` |
| Output contract compliance | 100% | `rates.yaml` |
| Autonomous CRITICAL recovery | **0 occurrences** — unconditional failure | `rates.yaml` |
