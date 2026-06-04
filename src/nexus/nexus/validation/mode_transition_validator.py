"""Mode state machine correctness validator — FM-06, FM-09.

Validates that mode transitions satisfy the allowed transition graph and
that CRITICAL is treated as a terminal state.
Step 5 of build order.
"""
# TODO: implement


def validate_transition(from_mode, to_mode, ai_output) -> bool:
    """Return True if the mode transition is valid for the given AI output."""
    raise NotImplementedError
