"""Amplifier tool module wrapping the impeccable design-slop detector CLI."""

import asyncio
import json
import logging
from typing import Any

from amplifier_core import ToolResult

logger = logging.getLogger(__name__)


class ImpeccableTool:
    """Wraps the `impeccable detect` CLI, returning CLEAN or structured findings."""

    @property
    def name(self) -> str:
        return "impeccable_detect"

    @property
    def description(self) -> str:
        return (
            "Runs the impeccable design-slop detector against a URL or file and "
            "returns a deterministic verdict: CLEAN if no findings are reported, "
            "or FINDINGS with the structured list of issues detected."
        )

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL or file path to run the impeccable detector against.",
                },
            },
            "required": ["url"],
        }

    async def execute(self, input_data: dict) -> ToolResult:
        target = input_data["url"]

        try:
            findings = await self._run_detect(target)
        except FileNotFoundError:
            return ToolResult(
                success=False,
                output=(
                    "impeccable CLI not found. Install it globally with: "
                    "npm install -g impeccable"
                ),
            )
        except RuntimeError as exc:
            return ToolResult(
                success=False,
                output=f"impeccable detect failed: {exc}",
            )

        status = "CLEAN" if not findings else "FINDINGS"
        return ToolResult(success=True, output={"status": status, "findings": findings})

    async def _run_detect(self, target: str) -> list:
        # Invoke the globally-installed `impeccable` binary directly (installed via
        # `npm install -g impeccable`). This matches the orchestrator preflight
        # (`which impeccable`) and the README install instruction. Do NOT use
        # `npx impeccable` — npx would resolve a different/absent package and
        # diverge from the preflight check.
        process = await asyncio.create_subprocess_exec(
            "impeccable",
            "detect",
            "--json",
            target,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        raw = stdout.decode().strip()

        if raw.startswith("["):
            return json.loads(raw)

        raise RuntimeError(
            stderr.decode().strip() or raw or f"exit code {process.returncode}"
        )


async def mount(coordinator, config: dict[str, Any] | None = None):
    """Mount the impeccable design-slop detector tool.

    Args:
        coordinator: The module coordinator
        config: Optional configuration (unused)

    Returns:
        Module metadata dict describing this module and what it provides.
    """
    tool = ImpeccableTool()
    await coordinator.mount("tools", tool, name=tool.name)
    logger.info("Mounted ImpeccableTool")
    return {
        "name": "tool-impeccable",
        "version": "0.1.0",
        "provides": ["impeccable_detect"],
    }
