"""Tests for DomExtractTool.execute() with the _extract I/O boundary stubbed out.

These tests never launch a real browser: the _extract() method (which owns all
subprocess/agent-browser I/O) is replaced with an AsyncMock so execute() logic
can be verified in isolation.
"""

from unittest.mock import AsyncMock

from amplifier_module_tool_dom_extract import DEFAULT_SELECTORS
from amplifier_module_tool_dom_extract import DEFAULT_VIEWPORT
from amplifier_module_tool_dom_extract import DomExtractTool


def _fake_package(url: str, viewport: dict) -> dict:
    """Build a fake DOM Intelligence Package as _extract would return."""
    return {
        "url": url,
        "viewport": viewport,
        "accessibility_tree": {"role": "WebArea", "children": []},
        "computed_styles": {
            "h1": {"font-family": "Georgia", "color": "rgb(17, 17, 17)"}
        },
        "dom_structure": {
            "headings": [{"level": 1, "text": "Welcome"}],
            "semantic_elements": ["header", "main", "footer"],
        },
        "layout_geometry": {
            "h1": {
                "x": 0,
                "y": 0,
                "width": 320,
                "height": 40,
                "overflow": False,
                "zIndex": "auto",
            }
        },
    }


async def test_execute_returns_full_package():
    """execute() returns success with the full DOM Intelligence Package on success."""
    tool = DomExtractTool()
    tool._extract = AsyncMock(side_effect=lambda url, vp, sel: _fake_package(url, vp))

    result = await tool.execute({"url": "https://example.com"})

    assert result.success is True
    out = result.output
    assert {
        "accessibility_tree",
        "computed_styles",
        "dom_structure",
        "layout_geometry",
    } <= set(out.keys())
    assert out["dom_structure"]["headings"][0]["level"] == 1


async def test_execute_defaults_viewport_and_selectors():
    """execute() passes DEFAULT_VIEWPORT and DEFAULT_SELECTORS when not provided."""
    tool = DomExtractTool()
    tool._extract = AsyncMock(side_effect=lambda url, vp, sel: _fake_package(url, vp))

    await tool.execute({"url": "https://example.com"})

    call = tool._extract.call_args
    assert call[0][1] == DEFAULT_VIEWPORT
    assert call[0][2] == DEFAULT_SELECTORS


async def test_execute_passes_custom_viewport_and_selectors():
    """execute() forwards caller-provided viewport and selectors unchanged."""
    tool = DomExtractTool()
    tool._extract = AsyncMock(side_effect=lambda url, vp, sel: _fake_package(url, vp))
    vp = {"width": 375, "height": 812}

    await tool.execute(
        {"url": "https://example.com", "viewport": vp, "selectors": [".hero"]}
    )

    call = tool._extract.call_args
    assert call[0][1] == vp
    assert call[0][2] == [".hero"]


async def test_execute_reports_missing_browser_cli():
    """execute() reports a clear failure when the agent-browser CLI is not found."""
    tool = DomExtractTool()
    tool._extract = AsyncMock(side_effect=FileNotFoundError())

    result = await tool.execute({"url": "https://example.com"})

    assert result.success is False
    assert "not found" in result.output.lower()


async def test_execute_reports_extraction_error():
    """execute() reports a clear failure with the underlying error message on extraction failure."""
    tool = DomExtractTool()
    tool._extract = AsyncMock(side_effect=RuntimeError("nav timeout"))

    result = await tool.execute({"url": "https://example.com"})

    assert result.success is False
    assert "nav timeout" in result.output
