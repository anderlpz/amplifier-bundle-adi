"""Verify pyproject.toml scaffolding for tool-dom-extract parses and is well-formed."""

import tomllib
from pathlib import Path

PYPROJECT_PATH = Path(__file__).parent.parent / "pyproject.toml"


def test_pyproject_parses():
    """pyproject.toml must be valid TOML."""
    with open(PYPROJECT_PATH, "rb") as f:
        data = tomllib.load(f)
    assert data["project"]["name"] == "amplifier-module-tool-dom-extract"


def test_pyproject_declares_no_amplifier_core_dependency():
    """amplifier-core is a peer dependency and must NOT be declared."""
    with open(PYPROJECT_PATH, "rb") as f:
        data = tomllib.load(f)
    assert data["project"]["dependencies"] == []


def test_pyproject_entry_point_targets_mount():
    """Entry point must wire tool-dom-extract to the mount() function."""
    with open(PYPROJECT_PATH, "rb") as f:
        data = tomllib.load(f)
    entry_points = data["project"]["entry-points"]["amplifier.modules"]
    assert entry_points["tool-dom-extract"] == "amplifier_module_tool_dom_extract:mount"
