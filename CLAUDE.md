# NEXUS — Claude Code Context

## What This Project Is

NEXUS is a system-level validation framework for AI inference nodes in ROS2-based autonomous systems. It validates AI-driven operational mode switching (NORMAL → DEGRADED → CRITICAL) from sensor input through inference through downstream action, on both host (Python/ROS2) and edge (STM32/micro-ROS/TFLite-Micro) hardware.

This is safety-critical validation work. Incorrect classifications change what the system does — they are not advisory.

## Architecture in One Sentence

`nexus_stimulus_node` publishes sensor windows → AI Event Detector classifies them → `nexus_monitor_node` validates contracts/timing/propagation → `mode_controller_node` acts → `nexus_reporter_node` produces pass/fail results mapped to FMEA failure modes.

## Topic Map

| Topic | Direction |
|---|---|
| `/sensor/stream` | stimulus_node → AI Event Detector |
| `/ai/event_class` | AI Event Detector → monitor_node, mode_controller |
| `/system/mode` | mode_controller → monitor_node |
| `/nexus/results` | reporter_node → (output) |

## Mode and Event Class Mapping

| AI Output | Mode | Notes |
|---|---|---|
| `NOMINAL` | `NORMAL` | Stay or recover |
| `ANOMALY` | `DEGRADED` | Reduce output, alert |
| `CRITICAL_EVENT` | `CRITICAL` | Safe stop — terminal, requires operator reset |

CRITICAL is a **terminal state** under autonomous operation. Any autonomous recovery from CRITICAL is an unconditional failure (FM-09).

## Highest-Priority Failure Modes

These must never be treated as soft failures:

- **FM-06** (S=10): `CRITICAL_EVENT` input → `NOMINAL` output — system operates unsafely. Any single miss is an unconditional test failure.
- **FM-07** (RPN=162): OOD input → silent confident `NOMINAL` — no uncertainty signal.
- **FM-02** (RPN=168): INT8 quantization changes classification vs. FP32 host model.

## Key Validation Thresholds

| Parameter | Threshold |
|---|---|
| Inference latency — host | ≤ 20ms |
| Inference latency — STM32 HIL nominal | ≤ 50ms |
| Inference latency — STM32 HIL stressed | ≤ 75ms |
| Mode transition latency | ≤ 10ms |
| INT8 vs FP32 agreement | ≥ 98% |
| Critical event miss rate | **0%** — unconditional failure |
| False critical rate | ≤ 1% on nominal distribution |
| Output contract compliance | 100% |
| Autonomous CRITICAL recovery | **0 occurrences permitted** |

## Project Layout

```
nexus/nodes/          — stimulus, monitor, reporter ROS2 nodes
nexus/validation/     — contract, timing, mode transition, fault propagation, divergence validators
nexus/stimulus/       — stream generator, fault injector, scenario player
nexus/reporting/      — FMEA mapper, pass/fail evaluator, report writer
system_under_test/    — reference AI event detector + mode controller (replaceable)
config/               — YAML thresholds, contracts, stimulus profiles
scenarios/            — named end-to-end scenario definitions
tests/                — pytest suite, one file per FMEA failure mode
firmware/             — STM32 micro-ROS node (C), TFLite-Micro inference
launch/               — ROS2 launch files for full, timing, fault, HIL, scenario runs
```

## Tech Stack

- **Host:** Python, ROS2 (Humble or Jazzy), pytest
- **Edge:** STM32 Nucleo-F446RE, micro-ROS, TFLite-Micro (INT8)
- **Comms:** USART2/USB-UART for micro-ROS agent ↔ STM32
- **Build:** colcon (ROS2), STM32CubeIDE or arm-none-eabi-gcc

## Working Rules

- The AI Event Detector node is the **system under test** — NEXUS wraps around it, it does not live inside NEXUS logic.
- Fault injection happens at the stimulus layer (`nexus/stimulus/fault_injector.py`), not inside the nodes under test.
- Each test file maps to one or more FMEA IDs — keep that traceability intact.
- Contract definitions are in both human-readable (`docs/contracts/`) and machine-readable (`config/contracts/`) form — keep them in sync.
- FMEA RPN scores are not arbitrary; changing severity/occurrence/detection values requires rationale.

## Related Projects

| Project | Role |
|---|---|
| [SENTINEL](https://github.com/twrappe/sentinel) | Pillars 1 & 2 — input and model validation |
| [PRISM](https://github.com/twrappe/prism) | Pillar 3 — cross-component integration validation |
| **NEXUS** | Pillar 4 — system HIL validation |
