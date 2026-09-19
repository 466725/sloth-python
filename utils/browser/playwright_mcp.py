"""Helpers for calling MCP tools from Playwright tests."""

from typing import Any


class MCPPlaywrightHelper:
    """Call MCP analysis tools using a Playwright page snapshot."""

    def __init__(self, mcp_client):
        self.mcp = mcp_client

    async def _get_dom(self, page) -> str:
        return await page.content()

    async def _call_mcp_tool(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        return await self.mcp.call_tool(tool=tool, arguments=arguments)

    async def analyze_page(self, page) -> dict[str, Any]:
        dom = await self._get_dom(page)
        return await self._call_mcp_tool("analyze_dom", {"html": dom})

    async def suggest_locator(self, page, description: str) -> str:
        dom = await self._get_dom(page)
        result = await self._call_mcp_tool(
            "suggest_locator", {"html": dom, "description": description}
        )
        return result.get("locator", "")

    async def validate_event(self, event_payload: dict[str, Any]) -> dict[str, Any]:
        return await self._call_mcp_tool("validate_event", {"event": event_payload})
