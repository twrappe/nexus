# AI Event Detector Output Contract

Formal contract for the `/ai/event_class` topic.
Source of truth: `config/contracts/event_class_output.yaml`.

## Topic

`/ai/event_class`

## Publisher

`ai_event_detector_node`

## Subscribers

`nexus_monitor_node`, `mode_controller_node`

## Fields

<!-- TODO: expand from config/contracts/event_class_output.yaml -->

| Field | Type | Valid Values | Notes |
| --- | --- | --- | --- |
| `event_class` | int | 0 (NOMINAL), 1 (ANOMALY), 2 (CRITICAL_EVENT) | Maps via `mode_definitions.yaml` |
| `confidence` | float | [0.0, 1.0] | FM-04: outside range is a contract violation |
| `timestamp` | builtin_interfaces/Time | any | Used for latency measurement (FM-01) |

## Violation Conditions (FM-04)

- `confidence` < 0.0 or > 1.0
- `event_class` not in {0, 1, 2}
- Missing required fields

Contract compliance must be 100%.
