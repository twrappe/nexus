from enum import IntEnum


class EventClass(IntEnum):
    """
    AI Event Detector output classifications.
    Published on /ai/event_class.
    """
    NOMINAL = 0
    ANOMALY = 1
    CRITICAL_EVENT = 2


class OperationalMode(IntEnum):
    """
    System operational mode set by the mode controller.
    Published on /system/mode.

    CRITICAL is a terminal state under autonomous operation.
    Any autonomous transition out of CRITICAL is a validation failure (FM-09).
    """
    NORMAL = 0
    DEGRADED = 1
    CRITICAL = 2


EVENT_CLASS_TO_MODE = {
    EventClass.NOMINAL: OperationalMode.NORMAL,
    EventClass.ANOMALY: OperationalMode.DEGRADED,
    EventClass.CRITICAL_EVENT: OperationalMode.CRITICAL,
}
