"""Contract tests for tool-impeccable's mount() registration."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from amplifier_module_tool_impeccable import mount


@pytest.mark.asyncio
async def test_mount_registers_tool():
    coordinator = MagicMock()
    coordinator.mount = AsyncMock()

    result = await mount(coordinator)

    coordinator.mount.assert_called_once()
    assert coordinator.mount.call_args[0][0] == "tools"
    assert result is not None
    assert result["name"] == "tool-impeccable"
    assert "impeccable_detect" in result["provides"]


@pytest.mark.asyncio
async def test_tool_has_required_properties():
    coordinator = MagicMock()
    coordinator.mount = AsyncMock()

    await mount(coordinator)

    tool = coordinator.mount.call_args[0][1]
    assert isinstance(tool.name, str)
    assert tool.name == "impeccable_detect"
    assert isinstance(tool.description, str)
    assert tool.description != ""
    assert isinstance(tool.input_schema, dict)
    assert tool.input_schema["required"] == ["url"]
    assert callable(tool.execute)
