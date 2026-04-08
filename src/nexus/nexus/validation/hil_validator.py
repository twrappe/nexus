import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8

from nexus.nodes.common.mode import EventClass, OperationalMode, EVENT_CLASS_TO_MODE


class HILValidatorNode(Node):
    """
    Subscribes to /ai/event_class and /system/mode and validates:
      - output contract compliance (FM-01, FM-05)
      - mode transition latency <= 10ms (FM-04)
      - correct event class -> mode propagation (FM-06)
      - no autonomous recovery from CRITICAL (FM-09)
    """

    def __init__(self):
        super().__init__('hil_validator')

        self._last_event_class: EventClass | None = None
        self._last_event_ts: float | None = None
        self._last_mode: OperationalMode | None = None
        self._in_critical: bool = False

        self.create_subscription(
            Int8,
            '/ai/event_class',
            self._on_event_class,
            10,
        )
        self.create_subscription(
            Int8,
            '/system/mode',
            self._on_mode,
            10,
        )

        self.get_logger().info('HIL validator node started')

    # ------------------------------------------------------------------
    # Subscribers
    # ------------------------------------------------------------------

    def _on_event_class(self, msg: Int8) -> None:
        try:
            event = EventClass(msg.data)
        except ValueError:
            self._fail_contract(f'Unknown EventClass value: {msg.data}')
            return

        self._last_event_class = event
        self._last_event_ts = time.monotonic()
        self._check_contract(event)

    def _on_mode(self, msg: Int8) -> None:
        try:
            mode = OperationalMode(msg.data)
        except ValueError:
            self._fail_contract(f'Unknown OperationalMode value: {msg.data}')
            return

        arrival_ts = time.monotonic()
        self._check_fm09(mode)
        self._check_propagation(mode)
        self._check_timing(mode, arrival_ts)
        self._last_mode = mode

    # ------------------------------------------------------------------
    # Validation stubs — one per concern
    # ------------------------------------------------------------------

    def _check_contract(self, event: EventClass) -> None:
        """
        FM-01 / FM-05: AI output must be a valid EventClass value.
        Called on every /ai/event_class message.
        TODO: extend to validate confidence bounds and message structure.
        """
        pass

    def _check_propagation(self, mode: OperationalMode) -> None:
        """
        FM-06 (S=10): CRITICAL_EVENT must produce CRITICAL — any miss is
        an unconditional test failure.
        Also catches incorrect mappings for ANOMALY -> DEGRADED.
        TODO: record result to reporter.
        """
        if self._last_event_class is None:
            return

        expected = EVENT_CLASS_TO_MODE[self._last_event_class]
        if self._last_event_class == EventClass.CRITICAL_EVENT and mode != OperationalMode.CRITICAL:
            self._fail_unconditional(
                f'FM-06: CRITICAL_EVENT input produced {mode.name} — '
                f'expected {OperationalMode.CRITICAL.name}'
            )
        elif mode != expected:
            self._fail(
                f'Propagation mismatch: {self._last_event_class.name} -> '
                f'{mode.name}, expected {expected.name}'
            )

    def _check_timing(self, mode: OperationalMode, arrival_ts: float) -> None:
        """
        FM-04: Mode transition must occur within 10ms of event class publish.
        TODO: record latency samples to reporter.
        """
        if self._last_event_ts is None:
            return

        latency_ms = (arrival_ts - self._last_event_ts) * 1000.0
        if latency_ms > 10.0:
            self._fail(
                f'Timing violation: mode transition latency {latency_ms:.2f}ms '
                f'exceeds 10ms threshold'
            )

    def _check_fm09(self, mode: OperationalMode) -> None:
        """
        FM-09: Autonomous recovery from CRITICAL is an unconditional failure.
        CRITICAL is a terminal state — operator reset required.
        TODO: distinguish autonomous recovery from operator reset signal.
        """
        if self._in_critical and mode != OperationalMode.CRITICAL:
            self._fail_unconditional(
                f'FM-09: Autonomous recovery from CRITICAL to {mode.name}'
            )
        if mode == OperationalMode.CRITICAL:
            self._in_critical = True

    # ------------------------------------------------------------------
    # Reporting helpers
    # ------------------------------------------------------------------

    def _fail(self, reason: str) -> None:
        # TODO: publish failure to /nexus/results via reporter node
        self.get_logger().error(f'VALIDATION FAILURE: {reason}')

    def _fail_unconditional(self, reason: str) -> None:
        # TODO: publish unconditional failure to /nexus/results and halt scenario
        self.get_logger().fatal(f'UNCONDITIONAL FAILURE: {reason}')

    def _fail_contract(self, reason: str) -> None:
        # TODO: publish contract violation to /nexus/results
        self.get_logger().error(f'CONTRACT VIOLATION: {reason}')


def main(args=None):
    rclpy.init(args=args)
    node = HILValidatorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
