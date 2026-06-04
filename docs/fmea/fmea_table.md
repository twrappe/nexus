# FMEA Table

Full failure mode and effects analysis for NEXUS.

See README.md for the summary table and RPN rationale. This document provides
extended analysis including detection method detail, test linkage, and notes.

---

| ID | Failure Mode | Autonomous Consequence | S | O | D | RPN | Test | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FM-01 | Inference exceeds latency budget | Mode switch delayed N cycles, system in wrong mode | 8 | 3 | 4 | 96 | `test_timing_nominal` | 📋 |
| FM-02 | INT8 quantization changes classification | Edge hardware makes different mode decisions than simulation | 7 | 4 | 6 | 168 | `test_quantization_divergence` | 📋 |
| FM-03 | NOMINAL input → CRITICAL_EVENT output | Unnecessary safe stop, mission abort, operator reset required | 8 | 2 | 3 | 48 | `test_false_critical` | 📋 |
| FM-04 | Output confidence outside contract range | Mode controller receives invalid confidence, undefined behavior | 7 | 2 | 5 | 70 | `test_contract_confidence` | 📋 |
| FM-05 | Dropped input → stale output propagated | System acts on outdated classification, sensor failure undetected | 8 | 3 | 5 | 120 | `test_fault_dropped_input` | 📋 |
| FM-06 | CRITICAL_EVENT input → NOMINAL output | Critical condition undetected, system continues unsafe operation | 10 | 2 | 6 | 120 | `test_critical_event_miss` | 📋 |
| FM-07 | OOD input → silent confident NOMINAL | No uncertainty signal, system proceeds on bad inference | 9 | 3 | 6 | 162 | `test_fault_ood_input` | 📋 |
| FM-08 | micro-ROS latency exceeds budget | Edge node mode decisions lag simulation baseline | 7 | 3 | 4 | 84 | `test_edge_timing_hil` | 📋 |
| FM-09 | Autonomous recovery from CRITICAL state | System resumes operation without operator reset | 9 | 1 | 3 | 27 | `test_critical_terminal` | 📋 |

*S = Severity, O = Occurrence, D = Detection (higher = harder to detect), RPN = S × O × D*

**Highest RPN:** FM-07 (162) — OOD input, silent confident NOMINAL, no uncertainty signal.  
**Highest Severity:** FM-06 (S=10) — critical event missed entirely.

---

## Unconditional Failures

- **FM-06** — any single critical event miss, regardless of pass rate
- **FM-09** — any single autonomous CRITICAL recovery

## Notes

<!-- TODO: extend with per-FM detection method, coverage gaps, and residual risk notes -->
