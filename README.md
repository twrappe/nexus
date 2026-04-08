# NEXUS — AI Node Validation Framework for ROS2 Autonomous Systems

**AI Systems Validation | ROS2 | micro-ROS | STM32 | Event Detection | Mode Switching**

NEXUS is a system-level validation framework for AI inference nodes deployed inside ROS2-based autonomous systems. It validates a concrete autonomous behavior — **AI-driven operational mode switching based on real-time event detection** — from sensor input through inference through downstream decision, on both host and edge hardware.

Designed for safety-critical and defense-adjacent systems where an incorrect AI classification doesn't just produce a wrong answer — it changes what the system does.

---

## The Autonomous Behavior

An AI event detector node monitors a continuous sensor stream and classifies the current operational state into one of three modes:

```
NORMAL → DEGRADED → CRITICAL
```

A downstream mode controller node acts on this classification, changing system behavior accordingly:

| AI Output | Mode Controller Response |
|---|---|
| `NORMAL` | Continue nominal operation |
| `DEGRADED` | Reduce output, increase monitoring frequency, alert |
| `CRITICAL` | Execute safe stop, isolate subsystem, halt autonomous operation |

This is unambiguously autonomous behavior — the system makes decisions and changes its own operation based on AI inference output. The AI node is not advisory. It is in the loop.

**The validation question NEXUS answers:** *Does the AI event detector produce the right classification, at the right time, with the right confidence, such that the mode controller takes the right action — across nominal inputs, edge cases, degraded sensor conditions, and fault injection scenarios?*

---

## Why This Behavior Class Matters

Event detection with mode switching appears across the defense and autonomous systems domain:

- Fault detection on naval autonomous vessels (Saronic)
- Operational state monitoring on defense robotics platforms (Allen Control)
- Anomaly-triggered safe stop on autonomous ground vehicles
- Health monitoring with mode degradation on UAV systems

The validation methodology NEXUS implements is portable across all of these. The surrogate sensor stream and event classes are the only domain-specific elements.

---

## System Architecture

```
                        ROS2 SYSTEM
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌──────────────────┐                                               │
│  │ nexus_stimulus_  │   /sensor/stream                             │
│  │ node             │──────────────────────────────────────┐        │
│  │                  │                                      ▼        │
│  │ • nominal inputs │                         ┌────────────────────┐│
│  │ • fault inject   │                         │  AI Event Detector ││
│  │ • scenario play  │                         │  Node              ││
│  └──────────────────┘                         │                    ││
│                                               │  [System Under     ││
│  ┌──────────────────┐   /ai/event_class       │   Test]            ││
│  │ nexus_monitor_   │◀────────────────────────│                    ││
│  │ node             │                         └────────────────────┘│
│  │                  │                                  │             │
│  │ • contract valid │              /ai/event_class     │             │
│  │ • timing enforce │◀─────────────────────────────────┘             │
│  │ • propagation    │                                               │
│  │   detection      │   /ai/event_class                             │
│  └────────┬─────────┘──────────────────────────────────┐            │
│           │                                            ▼            │
│           │                               ┌────────────────────────┐│
│           │                               │  Mode Controller Node  ││
│           │   /system/mode                │                        ││
│           │◀──────────────────────────────│  NORMAL                ││
│           │                               │  DEGRADED              ││
│           │                               │  CRITICAL → SAFE STOP  ││
│           │                               └────────────────────────┘│
│           │                                                         │
│           ▼                                                         │
│  ┌──────────────────┐                                               │
│  │ nexus_reporter_  │                                               │
│  │ node             │                                               │
│  │                  │                                               │
│  │ • pass/fail eval │                                               │
│  │ • FMEA mapping   │                                               │
│  │ • report gen     │                                               │
│  └──────────────────┘                                               │
└─────────────────────────────────────────────────────────────────────┘
                                  ▲
                        micro-ROS │ UART/USB
                                  │
┌─────────────────────────────────┴───────────────────────────────────┐
│                      STM32 (micro-ROS node)                         │
│                                                                     │
│  Subscribes: /edge/sensor_input                                     │
│  Publishes:  /edge/event_classification                             │
│                                                                     │
│  ┌──────────────┐   ┌──────────────────┐   ┌──────────────────┐    │
│  │ micro-ROS    │──▶│ TFLite-Micro     │──▶│ GPIO Timing      │    │
│  │ Interface    │   │ Inference Engine │   │ Probe            │    │
│  └──────────────┘   └──────────────────┘   └──────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

### Topic Map

| Topic | Publisher | Subscribers | Content |
|---|---|---|---|
| `/sensor/stream` | `nexus_stimulus_node` | AI Event Detector | Sensor window (float array + timestamp) |
| `/ai/event_class` | AI Event Detector | `nexus_monitor_node`, Mode Controller | Classification + confidence + latency |
| `/system/mode` | Mode Controller | `nexus_monitor_node` | Current mode enum + transition timestamp |
| `/nexus/results` | `nexus_reporter_node` | — | Structured pass/fail per test case |

---

## Operational Modes

### Mode Definitions

```python
class OperationalMode(Enum):
    NORMAL   = 0    # Nominal sensor stream, full autonomous operation
    DEGRADED = 1    # Anomalous signal detected, reduced operation + alert
    CRITICAL = 2    # Critical event detected, safe stop initiated
```

### Valid Mode Transitions

```
NORMAL ──────────────────▶ DEGRADED ──────────────▶ CRITICAL
  ▲                            │                        │
  │                            │                        │
  └────────────────────────────┘                        │
           (recovery)                                   │
                                              (requires manual reset)
```

CRITICAL is a terminal state under autonomous operation. Recovery requires operator intervention. This is a system-level requirement, not an AI requirement — and NEXUS validates that the mode controller enforces it.

---

## Event Classes

The AI event detector classifies each sensor window into one of three event classes that map directly to operational modes:

| Event Class | Trigger Condition | Maps To |
|---|---|---|
| `NOMINAL` | Signal within expected distribution | `NORMAL` |
| `ANOMALY` | Signal deviation exceeding threshold | `DEGRADED` |
| `CRITICAL_EVENT` | High-confidence extreme deviation | `CRITICAL` |

The surrogate sensor stream is a windowed time-series (accelerometer or biosignal-derived) generated by `nexus_stimulus_node`. The specific signal domain is replaceable — the validation methodology is invariant to it.

---

## Validation Targets

### 1. Classification Correctness Under Nominal Conditions
Does the AI node correctly classify known-good and known-bad inputs?

- Nominal inputs → `NOMINAL` classification with confidence ≥ threshold
- Injected anomaly inputs → `ANOMALY` classification
- Injected critical inputs → `CRITICAL_EVENT` classification
- Ground truth labels carried in stimulus metadata, evaluated by monitor node

### 2. Mode Controller Response Correctness
Does the mode controller take the right action on every AI classification?

| AI Output | Expected Mode Transition | Failure Case |
|---|---|---|
| `NOMINAL` | Stay `NORMAL` or recover to `NORMAL` | Spurious mode escalation |
| `ANOMALY` | Transition to `DEGRADED` | Missed degradation, or overreaction to `CRITICAL` |
| `CRITICAL_EVENT` | Transition to `CRITICAL`, initiate safe stop | Missed critical event — highest severity failure |
| Any (post-CRITICAL) | Remain `CRITICAL` | Autonomous recovery from terminal state |

### 3. Timing Budget Compliance
Does inference complete within the control loop budget?

- End-to-end latency: `/sensor/stream` publish → `/ai/event_class` receipt
- Mode transition latency: `/ai/event_class` receipt → `/system/mode` publish
- Total pipeline latency: sensor publish → mode change
- All three measured independently; all three have defined pass/fail thresholds

### 4. Fault Injection and Graceful Degradation

| Fault | Stimulus | Expected AI Behavior | Expected Mode Behavior |
|---|---|---|---|
| Zero input | All-zero sensor window | `ANOMALY` or `CRITICAL_EVENT`, never silent `NOMINAL` | Escalate, never stay `NORMAL` |
| Clipped signal | Saturated sensor values | Elevated uncertainty, classification within contract | Escalate appropriately |
| OOD input | Out-of-distribution window | Explicit uncertainty signal, no silent confident `NOMINAL` | Conservative escalation |
| Dropped input | No `/sensor/stream` for N cycles | Stale output flagged, not republished silently | Mode controller holds last known, does not autonomously recover |
| High-freq burst | Input above rated frequency | Inference queue does not back up, no state corruption | No spurious mode transitions |

### 5. Critical Event Miss — Highest Priority Failure Mode
The most dangerous failure: AI outputs `NOMINAL` on a `CRITICAL_EVENT` input. System continues operating when it should safe-stop.

- Dedicated test suite with high repetition across input variations
- Any single miss is an unconditional test failure regardless of overall pass rate
- Maps to FM-06 (highest RPN in FMEA)

### 6. False Critical — Second Priority Failure Mode
AI outputs `CRITICAL_EVENT` on a `NOMINAL` input. System executes unnecessary safe stop.

- Unrecoverable autonomously — requires operator reset
- High operational cost in defense/autonomous context
- Maps to FM-03

### 7. Quantization Divergence (STM32 HIL)
Does the INT8 quantized model on STM32 produce the same mode decisions as the FP32 host model?

- Evaluated on the full nominal, anomaly, and critical stimulus set
- Classification disagreements tracked separately from confidence value differences
- Any NORMAL→CRITICAL or CRITICAL→NORMAL disagreement is a critical divergence

### 8. Operational Scenario Validation
End-to-end behavioral correctness across defined operational scenarios:

| Scenario | Description |
|---|---|
| `nominal_operation` | Sustained nominal inputs, system stays NORMAL |
| `gradual_degradation` | Signal quality degrades progressively, system escalates NORMAL→DEGRADED |
| `sudden_critical` | Abrupt critical event, system escalates directly NORMAL→CRITICAL |
| `recovery_sequence` | Anomaly resolves, system recovers DEGRADED→NORMAL |
| `sensor_dropout` | Input topic goes silent mid-operation, system handles stale state |
| `sustained_fault_injection` | Extended OOD input stream, no false critical events |

---

## FMEA

Full table and RPN rationale in [`docs/fmea/fmea_table.md`](docs/fmea/fmea_table.md).

| ID | Failure Mode | Autonomous Consequence | S | O | D | RPN | Test |
|---|---|---|---|---|---|---|---|
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

## Project Structure

```
nexus/
│
├── README.md
├── LICENSE                                     # Apache 2.0
├── requirements.txt                            # Python host dependencies
├── package.xml                                 # ROS2 package manifest
├── CMakeLists.txt                              # ROS2 build config
│
├── docs/
│   ├── validation_spec.md                      # Operational requirements and pass/fail thresholds
│   ├── architecture.md                         # System architecture and data flow
│   ├── autonomous_behavior.md                  # Event detection and mode switching specification
│   ├── fmea/
│   │   ├── fmea_table.md                       # Full FMEA with RPN scores and rationale
│   │   └── fmea_to_test_map.md                 # Failure mode to test case traceability
│   └── contracts/
│       ├── ai_output_contract.md               # AI node output interface contract
│       └── mode_controller_contract.md         # Mode controller input/output contract
│
├── nexus/                                      # ROS2 Python package
│   ├── __init__.py
│   │
│   ├── nodes/
│   │   ├── stimulus_node.py                    # Sensor simulator + fault injector
│   │   ├── monitor_node.py                     # Contract + timing + propagation monitor
│   │   └── reporter_node.py                    # Result aggregation and reporting
│   │
│   ├── validation/
│   │   ├── contract_validator.py               # Message schema and value range validation
│   │   ├── timing_validator.py                 # Latency measurement and budget enforcement
│   │   ├── mode_transition_validator.py        # Mode controller response correctness
│   │   ├── fault_propagation.py                # Inter-node fault propagation detection
│   │   └── divergence_analyzer.py              # INT8 vs FP32 classification comparison
│   │
│   ├── stimulus/
│   │   ├── stream_generator.py                 # Nominal sensor stream generation
│   │   ├── fault_injector.py                   # Degenerate input generation
│   │   └── scenario_player.py                  # Scenario sequence execution
│   │
│   └── reporting/
│       ├── fmea_mapper.py                      # Maps results to FMEA failure modes
│       ├── pass_fail_evaluator.py              # Threshold evaluation
│       └── report_writer.py                    # JSON and HTML report generation
│
├── system_under_test/                          # Reference implementation (replaceable)
│   ├── ai_event_detector_node.py              # AI event detector ROS2 node
│   └── mode_controller_node.py                # Mode controller ROS2 node
│
├── config/
│   ├── validation_spec.yaml                    # Pass/fail thresholds
│   ├── mode_definitions.yaml                   # Operational mode enum and transitions
│   ├── contracts/
│   │   ├── ai_output_contract.yaml             # Machine-readable AI output contract
│   │   └── mode_controller_contract.yaml       # Machine-readable mode contract
│   └── stimulus/
│       ├── nominal.yaml                        # Nominal stream profiles
│       ├── edge_cases.yaml                     # Boundary condition inputs
│       └── fault_cases.yaml                    # Fault injection scenarios
│
├── scenarios/
│   ├── nominal_operation.yaml
│   ├── gradual_degradation.yaml
│   ├── sudden_critical.yaml
│   ├── recovery_sequence.yaml
│   ├── sensor_dropout.yaml
│   └── sustained_fault_injection.yaml
│
├── launch/
│   ├── nexus_full_validation.launch.py         # Full validation suite
│   ├── nexus_timing_only.launch.py             # Timing budget only
│   ├── nexus_fault_injection.launch.py         # Fault injection suite
│   ├── nexus_hil.launch.py                     # STM32 hardware-in-the-loop
│   └── nexus_scenario.launch.py                # Single scenario execution
│
├── tests/
│   ├── conftest.py                             # Shared fixtures, ROS2 context
│   ├── test_classification_correctness.py      # Nominal classification accuracy
│   ├── test_mode_transitions.py                # Mode controller response correctness
│   ├── test_timing_budget.py                   # FM-01, FM-08: latency compliance
│   ├── test_quantization_divergence.py         # FM-02: INT8 vs FP32 equivalence
│   ├── test_false_critical.py                  # FM-03: NOMINAL → CRITICAL_EVENT
│   ├── test_contract_compliance.py             # FM-04: output contract validation
│   ├── test_fault_dropped_input.py             # FM-05: stale output on dropped input
│   ├── test_critical_event_miss.py             # FM-06: CRITICAL_EVENT → NOMINAL (highest severity)
│   ├── test_fault_ood_input.py                 # FM-07: OOD input response
│   ├── test_critical_terminal.py               # FM-09: no autonomous CRITICAL recovery
│   ├── test_fault_propagation.py               # Inter-node fault propagation
│   └── test_scenarios.py                       # End-to-end scenario validation
│
├── firmware/                                   # STM32 micro-ROS node
│   ├── Core/
│   │   ├── Src/
│   │   │   ├── main.c                          # Entry point, peripheral init
│   │   │   ├── microros_node.c                 # micro-ROS pub/sub setup
│   │   │   ├── inference_engine.c              # TFLite-Micro inference wrapper
│   │   │   └── timing_probe.c                  # GPIO toggle latency measurement
│   │   └── Inc/
│   │       ├── microros_node.h
│   │       ├── inference_engine.h
│   │       └── timing_probe.h
│   ├── Models/
│   │   ├── model_int8.tflite                   # Quantized INT8 event detector
│   │   └── model_int8.cc                       # C array for firmware embedding
│   └── Lib/
│       ├── tflite-micro/
│       └── micro_ros_stm32cubemx_utils/
│
├── results/
│   └── .gitkeep
│
└── scripts/
    ├── flash_firmware.sh
    ├── build_firmware.sh
    ├── start_microros_agent.sh
    └── run_validation.sh
```

---

## Hardware Setup

**Target:** STM32 Nucleo-F446RE or STM32F4 Discovery
**Host:** Linux with ROS2 Humble or Jazzy

| STM32 Pin | Connection | Purpose |
|---|---|---|
| USART2 TX/RX | USB-UART to host | micro-ROS agent communication |
| PA5 (GPIO OUT) | Logic analyzer (optional) | Inference start probe |
| PA6 (GPIO OUT) | Logic analyzer (optional) | Inference end probe |
| NRST | ST-Link | Flash and debug |

---

## Quickstart

### 1. Build

```bash
cd ~/ros2_ws/src && git clone https://github.com/twrappe/nexus
cd ~/ros2_ws && colcon build --packages-select nexus
source install/setup.bash
```

### 2. Run full validation (host only)

```bash
ros2 launch nexus nexus_full_validation.launch.py
```

### 3. Run with STM32 HIL

```bash
./scripts/flash_firmware.sh /dev/ttyUSB0
./scripts/start_microros_agent.sh /dev/ttyUSB0 115200
ros2 launch nexus nexus_hil.launch.py port:=/dev/ttyUSB0
```

### 4. Run a specific scenario

```bash
ros2 launch nexus nexus_scenario.launch.py \
  scenario:=scenarios/sudden_critical.yaml
```

### 5. Run pytest suite

```bash
pytest tests/ -v --html=results/reports/report.html
```

---

## Validation Specification Summary

| Parameter | Threshold |
|---|---|
| Inference latency — host (nominal) | ≤ 20ms |
| Inference latency — STM32 HIL (nominal) | ≤ 50ms |
| Inference latency — STM32 HIL (stressed) | ≤ 75ms |
| Mode transition latency (AI output → mode change) | ≤ 10ms |
| INT8 vs FP32 classification agreement | ≥ 98% |
| Critical event miss rate | 0% — any miss is unconditional failure |
| False critical rate | ≤ 1% on nominal input distribution |
| Output contract compliance | 100% |
| OOD input — uncertainty signal present | 100% |
| Autonomous CRITICAL recovery | 0 occurrences permitted |

---

## Relationship to SENTINEL and PRISM

| Pillar | Project | What It Validates |
|---|---|---|
| Pillar 1 — Input validation | [SENTINEL](https://github.com/twrappe/sentinel) | Signal preprocessing, artifact rejection, cross-modal faithfulness |
| Pillar 2 — Model validation | [SENTINEL](https://github.com/twrappe/sentinel) | ECE, hallucination rate, temporal precision, confidence calibration |
| Pillar 3 — Integration validation | [PRISM](https://github.com/twrappe/prism) | Cross-component failure correlation at scale, interface contract violations |
| Pillar 4 — System HIL validation | **NEXUS** | AI-driven mode switching correctness, ROS2 node contracts, STM32 edge HIL |

---

## License

Apache 2.0 — see [LICENSE](LICENSE)
