"""
Domain enumerations for NEXUS.

Single source of truth for event classes and operational modes.
All integer values are loaded from config/mode_definitions.yaml at import time —
nothing is hardcoded here.
"""

from __future__ import annotations

from enum import IntEnum
from pathlib import Path
from typing import Dict, FrozenSet

import yaml


# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------

def _find_config() -> Path:
    """Walk up from this file until config/mode_definitions.yaml is found."""
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "config" / "mode_definitions.yaml"
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "config/mode_definitions.yaml not found in any parent directory of "
        f"{__file__!r}. Ensure the workspace root contains the config/ directory."
    )


def _load() -> dict:
    with _find_config().open() as fh:
        return yaml.safe_load(fh)


_cfg: dict = _load()
