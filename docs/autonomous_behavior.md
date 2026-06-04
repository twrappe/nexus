# Autonomous Behavior Under Validation

Description of the AI-driven mode switching behavior that NEXUS validates.

<!-- TODO: expand with signal domain detail, class boundary definitions,
     and link to stimulus profile configs once Step 4 is complete. -->

## The Behavior

An AI event detector node monitors a continuous sensor stream and classifies
the current operational state:

```
NOMINAL → NORMAL mode
ANOMALY → DEGRADED mode
CRITICAL_EVENT → CRITICAL mode (terminal)
```

The AI node is not advisory — its output changes what the system does.

## Event Classes

| Event Class | int | Trigger Condition | Mode |
| --- | --- | --- | --- |
| `NOMINAL` | 0 | Signal within expected distribution | `NORMAL` (0) |
| `ANOMALY` | 1 | Signal deviation exceeding threshold | `DEGRADED` (1) |
| `CRITICAL_EVENT` | 2 | High-confidence extreme deviation | `CRITICAL` (2) |

See `config/mode_definitions.yaml` for authoritative integer values.

## Failure Asymmetry

Missing a `CRITICAL_EVENT` (FM-06, S=10) is worse than a false critical
(FM-03, S=8). Validation priority reflects this asymmetry.
