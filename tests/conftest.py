"""NEXUS pytest configuration and shared fixtures."""
import pytest


@pytest.fixture
def config_dir(tmp_path):
    """Return path to the project config directory."""
    import pathlib
    return pathlib.Path(__file__).parent.parent / "config"
