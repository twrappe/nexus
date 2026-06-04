# System Architecture

NEXUS validation framework architecture.

See README.md for the full ASCII architecture diagram and topic map.

<!-- TODO: expand with component interaction diagrams, sequence diagrams, and
     per-component interface tables. -->

## Components

| Component | File | Role |
| --- | --- | --- |
| `nexus_stimulus_node` | `nodes/stimulus_node.py` | Publishes synthetic sensor windows |
| `nexus_monitor_node` | `nodes/monitor_node.py` | Orchestrates validator chain |
| `nexus_reporter_node` | `nodes/reporter_node.py` | Aggregates results, generates reports |
| `ai_event_detector_node` | `system_under_test/ai_event_detector_node.py` | System under test |
| `mode_controller_node` | `system_under_test/mode_controller_node.py` | System under test |
| STM32 micro-ROS node | `firmware/` | Edge system under test (HIL) |

## Topic Map

| Topic | Publisher | Subscribers |
| --- | --- | --- |
| `/sensor/stream` | `nexus_stimulus_node` | `ai_event_detector_node` |
| `/ai/event_class` | `ai_event_detector_node` | `nexus_monitor_node`, `mode_controller_node` |
| `/system/mode` | `mode_controller_node` | `nexus_monitor_node` |
| `/nexus/results` | `nexus_reporter_node` | — |
