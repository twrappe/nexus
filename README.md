# NEXUS README — Four Revised Sections

## REPLACE: Status (early in document, after lede)

---

### Status

This repository contains the **design specification, FMEA, and validation architecture** for NEXUS. Implementation has not yet begun.

| Component | State |
| --- | --- |
| Validation methodology & FMEA | ✅ Designed |
| System architecture & interface contracts | ✅ Designed |
| Operational mode state machine | ✅ Designed |
| Host-side validation harness (Python / ROS2) | 📋 Planned |
| pytest + HTML reporting scaffold | 📋 Planned |
| STM32 micro-ROS firmware (FreeRTOS) | 📋 Planned |
| Hardware-in-the-loop integration | 📋 Planned |
| Quantization divergence testing (INT8 vs FP32) | 📋 Planned |

The README sections below describe the **full designed system**. See [`PROGRESS.md`](PROGRESS.md) for current development status.

---

## REPLACE: Quickstart (late in document)

---

### Quickstart

Quickstart instructions are planned for when the host-side validation harness and STM32 firmware are complete.

**Currently runnable:** Host-side latency validation harness against a mock embedded publisher. This validates the test architecture without requiring hardware.

```bash
# Planned for future: full build and test suite
# ros2 launch nexus nexus_full_validation.launch.py
# pytest tests/ -v --html=results/report.html --self-contained-html

# See PROGRESS.md for current development milestones
```

For now, refer to [`PROGRESS.md`](PROGRESS.md) to track implementation status.

---

## REPLACE: Repository State → Current / Planned sections

---

### Repository State

#### Current

```
nexus/
├── README.md                       # This file
├── PROGRESS.md                     # Development log
├── CLAUDE.md                       # Working notes
├── LICENSE                         # Apache 2.0
├── requirements.txt                # Python dependencies (host)
├── config/                         # Configuration scaffolding
├── src/                            # Source scaffolding
└── docs/
    └── fmea/
        └── fmea_table.md           # Extracted FMEA detail
```

#### Planned

**Python ROS2 Package:** Complete validation harness with five validation modules (contract validation, timing, mode transitions, fault propagation, quantization analysis). Seven ROS2 nodes: stimulus generator, monitor, reporter, mode controller, and reference system-under-test implementations. Pytest suite with 12 tests mapped to FMEA failure modes. HTML test report generation.

**STM32 Firmware:** micro-ROS node running on STM32F4 Discovery under FreeRTOS. Subscribes to sensor input topic, runs TFLite-Micro quantized inference, publishes classifications with timing metadata. GPIO timing probes for latency measurement. Flashing and micro-ROS agent orchestration scripts.

**Configuration & Scenarios:** YAML-based validation thresholds, mode definitions, hardware contracts. Six operational scenario definitions: nominal operation, gradual degradation, sudden critical, recovery sequence, sensor dropout, sustained fault injection. ROS2 launch files for full validation suite, timing-only, fault injection, HIL, and scenario execution.

**Documentation:** Detailed validation specification, architecture deep-dive, autonomous behavior specification, interface contracts, and FMEA-to-test-case traceability matrix.

---

## REPLACE: Status columns on FMEA table

---

### FMEA

Full table and RPN rationale in [`docs/fmea/fmea_table.md`](docs/fmea/fmea_table.md).

**Status: All 9 failure modes designed. 0 of 9 tests implemented. See [`PROGRESS.md`](PROGRESS.md) for implementation timeline.**

| ID | Failure Mode | Autonomous Consequence | S | O | D | RPN | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FM-01 | Inference exceeds latency budget | Mode switch delayed N cycles, system in wrong mode | 8 | 3 | 4 | 96 | `test_timing_nominal` |
| FM-02 | INT8 quantization changes classification | Edge hardware makes different mode decisions than simulation | 7 | 4 | 6 | 168 | `test_quantization_divergence` |
| FM-03 | NOMINAL input → CRITICAL_EVENT output | Unnecessary safe stop, mission abort, operator reset required | 8 | 2 | 3 | 48 | `test_false_critical` |
| FM-04 | Output confidence outside contract range | Mode controller receives invalid confidence, undefined behavior | 7 | 2 | 5 | 70 | `test_contract_confidence` |
| FM-05 | Dropped input → stale output propagated | System acts on outdated classification, sensor failure undetected | 8 | 3 | 5 | 120 | `test_fault_dropped_input` |
| FM-06 | CRITICAL_EVENT input → NOMINAL output | Critical condition undetected, system continues unsafe operation | 10 | 2 | 6 | 120 | `test_critical_event_miss` |
| FM-07 | OOD input → silent confident NOMINAL | No uncertainty signal, system proceeds on bad inference | 9 | 3 | 6 | 162 | `test_fault_ood_input` |
| FM-08 | micro-ROS latency exceeds budget | Edge node mode decisions lag simulation baseline | 7 | 3 | 4 | 84 | `test_edge_timing_hil` |
| FM-09 | Autonomous recovery from CRITICAL state | System resumes operation without operator reset | 9 | 1 | 3 | 27 | `test_critical_terminal` |

*S = Severity, O = Occurrence, D = Detection (higher = harder to detect), RPN = S × O × D*

**Highest RPN:** FM-07 (162) — OOD input, silent confident NOMINAL output, no uncertainty signal.
**Highest Severity:** FM-06 (S=10) — critical event missed entirely, system operates unsafely.

---

## REPLACE: Status column on Validation Specification Summary

---

### Validation Specification Summary

**Status: All 10 thresholds designed. 0 thresholds validated. See [`PROGRESS.md`](PROGRESS.md) for implementation timeline.**

| Parameter | Threshold |
| --- | --- |
| Inference latency — host (nominal) | ≤ 20 ms |
| Inference latency — STM32 HIL (nominal) | ≤ 50 ms |
| Inference latency — STM32 HIL (stressed) | ≤ 75 ms |
| Mode transition latency (AI output → mode change) | ≤ 10 ms |
| INT8 vs FP32 classification agreement | ≥ 98% |
| Critical event miss rate | 0% — any miss is unconditional failure |
| False critical rate | ≤ 1% on nominal input distribution |
| Output contract compliance | 100% |
| OOD input — uncertainty signal present | 100% |
| Autonomous CRITICAL recovery | 0 occurrences permitted |

---
