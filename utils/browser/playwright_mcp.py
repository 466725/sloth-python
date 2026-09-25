"""Helpers for calling MCP tools from Playwright tests."""

from collections.abc import Awaitable
from typing import Any, Protocol


class PlaywrightPage(Protocol):
    def content(self) -> Awaitable[str]:
        """Return the current page HTML."""


class MCPClient(Protocol):
    def call_tool(self, *, tool: str, arguments: dict[str, Any]) -> Awaitable[dict[str, Any]]:
        """Call an MCP tool with JSON-compatible arguments."""


class MCPPlaywrightHelper:
    """Call MCP analysis tools using a Playwright page snapshot."""

    def __init__(self, mcp_client: MCPClient):
        self.mcp = mcp_client

    async def get_page_html(self, page: PlaywrightPage) -> str:
        """Read the current HTML from a Playwright-compatible page."""

        return await page.content()

    async def call_tool(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call an MCP tool through the configured client."""

        return await self.mcp.call_tool(tool=tool, arguments=arguments)

    async def analyze_page(self, page: PlaywrightPage) -> dict[str, Any]:
        """Analyze the current page HTML through the MCP server."""

        return await self.call_tool(
            "analyze_dom", {"html": await self.get_page_html(page)}
        )

    async def suggest_locator(self, page: PlaywrightPage, description: str) -> str:
        """Return an MCP-suggested locator for a page element description."""

        if not description.strip():
            raise ValueError("description must not be empty")

        result = await self.call_tool(
            "suggest_locator",
            {"html": await self.get_page_html(page), "description": description},
        )
        return result.get("locator", "")

    async def validate_event(self, event_payload: dict[str, Any]) -> dict[str, Any]:
        """Validate an analytics event payload through the MCP server."""

        return await self.call_tool("validate_event", {"event": event_payload})

    async def _get_dom(self, page: PlaywrightPage) -> str:
        """Backward-compatible alias for :meth:`get_page_html`."""

        return await self.get_page_html(page)

    async def _call_mcp_tool(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Backward-compatible alias for :meth:`call_tool`."""

        return await self.call_tool(tool, arguments)
