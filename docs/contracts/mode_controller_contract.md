# Mode Controller Output Contract

Formal contract for the `/system/mode` topic.
Source of truth: `config/contracts/system_mode_output.yaml`.

## Topic

`/system/mode`

## Publisher

`mode_controller_node`

## Subscribers

`nexus_monitor_node`

## Fields

<!-- TODO: expand from config/contracts/system_mode_output.yaml -->

| Field | Type | Valid Values | Notes |
| --- | --- | --- | --- |
| `mode` | int | 0 (NORMAL), 1 (DEGRADED), 2 (CRITICAL) | Maps via `mode_definitions.yaml` |
| `transition_timestamp` | builtin_interfaces/Time | any | Used for mode transition latency (FM-01) |

## State Machine Constraints

Valid transitions:

```
NORMAL → DEGRADED → CRITICAL
  ↑           │
  └───────────┘  (recovery)
```

- CRITICAL is terminal under autonomous operation (FM-09)
- No transition from CRITICAL without operator reset

## Violation Conditions

- `mode` not in {0, 1, 2}
- Autonomous transition out of CRITICAL (FM-09, unconditional failure)
- Transition that violates the allowed state machine graph
