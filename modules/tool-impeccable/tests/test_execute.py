"""Tests locking ImpeccableTool.execute() CLEAN/FINDINGS/error branches.

These tests stub the subprocess boundary (_run_detect) so they never invoke
the real `impeccable` CLI.
"""

from unittest.mock import AsyncMock

import pytest

from amplifier_module_tool_impeccable import ImpeccableTool


@pytest.mark.asyncio
async def test_execute_clean_when_no_findings():
    tool = ImpeccableTool()
    tool._run_detect = AsyncMock(return_value=[])

    result = await tool.execute({"url": "http://localhost:5173"})

    assert result.success is True
    assert isinstance(result.output, dict)
    assert result.output["status"] == "CLEAN"
    assert result.output["findings"] == []


@pytest.mark.asyncio
async def test_execute_findings_when_slop_detected():
    finding = {
        "antipattern": "overused-font",
        "name": "Overused font",
        "severity": "warning",
        "file": "http://localhost:5173",
        "line": 0,
        "snippet": "Primary font: inter",
    }
    tool = ImpeccableTool()
    tool._run_detect = AsyncMock(return_value=[finding])

    result = await tool.execute({"url": "http://localhost:5173"})

    assert result.success is True
    assert isinstance(result.output, dict)
    assert result.output["status"] == "FINDINGS"
    assert result.output["findings"] == [finding]


@pytest.mark.asyncio
async def test_execute_reports_missing_cli():
    tool = ImpeccableTool()
    tool._run_detect = AsyncMock(side_effect=FileNotFoundError())

    result = await tool.execute({"url": "http://localhost:5173"})

    assert result.success is False
    assert isinstance(result.output, str)
    assert "not found" in result.output.lower()


@pytest.mark.asyncio
async def test_execute_reports_cli_error():
    tool = ImpeccableTool()
    tool._run_detect = AsyncMock(side_effect=RuntimeError("boom"))

    result = await tool.execute({"url": "http://localhost:5173"})

    assert result.success is False
    assert isinstance(result.output, str)
    assert "boom" in result.output
