"""Contract tests for tool-dom-extract mount() registration."""

from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from amplifier_module_tool_dom_extract import mount


async def test_mount_registers_tool():
    """mount() must register the tool under the 'tools' mount point and return metadata."""
    coordinator = MagicMock()
    coordinator.mount = AsyncMock()

    result = await mount(coordinator)

    coordinator.mount.assert_called_once()
    call_args = coordinator.mount.call_args
    assert call_args[0][0] == "tools"
    assert result is not None
    assert result["name"] == "tool-dom-extract"
    assert "dom_extract" in result["provides"]


async def test_tool_has_required_properties():
    """The mounted tool instance must expose the Tool protocol correctly."""
    coordinator = MagicMock()
    coordinator.mount = AsyncMock()

    await mount(coordinator)

    tool = coordinator.mount.call_args[0][1]
    assert tool.name == "dom_extract"
    assert isinstance(tool.description, str)
    assert tool.description
    assert isinstance(tool.input_schema, dict)
    assert tool.input_schema["required"] == ["url"]
    assert callable(tool.execute)
