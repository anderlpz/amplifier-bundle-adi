"""Amplifier tool module: structured DOM Intelligence Package extraction from a live page."""

import asyncio
import json
import logging
from typing import Any

from amplifier_core import ToolResult

logger = logging.getLogger(__name__)

VIEWPORTS = {
    "mobile": {"width": 375, "height": 812},
    "tablet": {"width": 768, "height": 1024},
    "desktop": {"width": 1440, "height": 900},
}

DEFAULT_VIEWPORT = VIEWPORTS["desktop"]

DEFAULT_SELECTORS = ["h1", "h2", "h3", "header", "nav", "main", "footer", "button", "a"]

_EXTRACT_JS = """
(() => {{
  const selectors = {selectors};
  const styleProps = [
    "color",
    "background-color",
    "font-family",
    "font-size",
    "font-weight",
    "line-height",
    "display",
    "margin",
    "padding",
    "gap",
  ];

  const computed_styles = {{}};
  const layout_geometry = {{}};

  selectors.forEach((selector) => {{
    const elements = Array.from(document.querySelectorAll(selector));
    computed_styles[selector] = elements.map((el) => {{
      const style = window.getComputedStyle(el);
      const styles = {{}};
      styleProps.forEach((prop) => {{
        styles[prop] = style.getPropertyValue(prop);
      }});
      return styles;
    }});

    layout_geometry[selector] = elements.map((el) => {{
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      return {{
        x: rect.x,
        y: rect.y,
        width: rect.width,
        height: rect.height,
        overflow:
          el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight,
        zIndex: style.getPropertyValue("z-index"),
      }};
    }});
  }});

  const headings = Array.from(
    document.querySelectorAll("h1, h2, h3, h4, h5, h6")
  ).map((el) => ({{
    level: el.tagName.toLowerCase(),
    text: (el.textContent || "").slice(0, 80),
  }}));

  const semantic_elements = [
    "header",
    "nav",
    "main",
    "aside",
    "footer",
    "section",
    "article",
  ].filter((tag) => document.querySelector(tag) !== null);

  const dom_structure = {{
    headings,
    semantic_elements,
  }};

  return JSON.stringify({{
    computed_styles,
    dom_structure,
    layout_geometry,
  }});
}})();
"""


class DomExtractTool:
    """Navigates to a live page and extracts a structured DOM Intelligence Package."""

    @property
    def name(self) -> str:
        return "dom_extract"

    @property
    def description(self) -> str:
        return (
            "Navigates to a live page and extracts a structured DOM Intelligence "
            "Package: accessibility tree, computed styles, DOM structure, and "
            "layout geometry."
        )

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL of the live page to extract the DOM Intelligence Package from.",
                },
                "viewport": {
                    "type": "object",
                    "description": "Viewport dimensions to use when extracting the page.",
                    "properties": {
                        "width": {"type": "integer"},
                        "height": {"type": "integer"},
                    },
                },
                "selectors": {
                    "type": "array",
                    "description": "CSS selectors to extract computed styles and layout geometry for.",
                    "items": {"type": "string"},
                },
            },
            "required": ["url"],
        }

    async def execute(self, input_data: dict) -> ToolResult:
        url = input_data["url"]
        viewport = input_data.get("viewport") or DEFAULT_VIEWPORT
        selectors = input_data.get("selectors") or DEFAULT_SELECTORS

        try:
            package = await self._extract(url, viewport, selectors)
        except FileNotFoundError:
            return ToolResult(
                success=False,
                output="agent-browser CLI not found. Ensure it is on PATH.",
            )
        except RuntimeError as exc:
            return ToolResult(
                success=False,
                output=f"DOM extraction failed: {exc}",
            )

        return ToolResult(success=True, output=package)

    async def _extract(self, url: str, viewport: dict, selectors: list) -> dict:
        await self._browser("open", url)
        await self._browser("viewport", str(viewport["width"]), str(viewport["height"]))

        a11y_raw = await self._browser("snapshot", "--json")

        js = _EXTRACT_JS.format(selectors=json.dumps(selectors))
        data_raw = await self._browser("eval", js)

        accessibility_tree = json.loads(a11y_raw) if a11y_raw.strip() else {}
        data = json.loads(data_raw)

        return {
            "url": url,
            "viewport": viewport,
            "accessibility_tree": accessibility_tree,
            "computed_styles": data["computed_styles"],
            "dom_structure": data["dom_structure"],
            "layout_geometry": data["layout_geometry"],
        }

    async def _browser(self, *args: str) -> str:
        process = await asyncio.create_subprocess_exec(
            "agent-browser",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(
                stderr.decode().strip() or f"exit code {process.returncode}"
            )

        return stdout.decode()


async def mount(coordinator, config: dict[str, Any] | None = None):
    """Mount the DOM extraction tool.

    Args:
        coordinator: The module coordinator
        config: Optional configuration (unused)

    Returns:
        Module metadata dict describing this module and what it provides.
    """
    tool = DomExtractTool()
    await coordinator.mount("tools", tool, name=tool.name)
    logger.info("Mounted DomExtractTool")
    return {
        "name": "tool-dom-extract",
        "version": "0.1.0",
        "provides": ["dom_extract"],
    }
