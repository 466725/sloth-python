from typing import Any, Dict, Optional


class MCPPlaywrightHelper:
    """
    Utility class enabling Playwright tests to call MCP tools
    for AI-assisted UI testing (locator generation, DOM analysis,
    analytics validation, etc.).
    """

    def __init__(self, mcp_client):
        """
        mcp_client: an initialized MCP client instance.
        """
        self.mcp = mcp_client

    async def _get_dom(self, page) -> str:
        """
        Internal helper to fetch the current DOM snapshot.
        """
        return await page.content()

    async def _call_mcp_tool(self, tool: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal helper to call an MCP tool with consistent structure.
        """
        return await self.mcp.call_tool(tool=tool, arguments=arguments)

    async def analyze_page(self, page) -> Dict[str, Any]:
        """
        Sends the current DOM snapshot to an MCP tool for analysis.
        Useful for:
        - AI locator suggestions
        - Accessibility hints
        - Page structure understanding
        """
        dom = await self._get_dom(page)
        return await self._call_mcp_tool(
            tool="analyze_dom",
            arguments={"html": dom}
        )

    async def suggest_locator(self, page, description: str) -> str:
        """
        Ask MCP to generate a Playwright locator based on a natural-language description.
        Example: "the login button", "the search input", etc.
        """
        dom = await self._get_dom(page)
        result = await self._call_mcp_tool(
            tool="suggest_locator",
            arguments={"html": dom, "description": description}
        )
        return result.get("locator", "")

    async def validate_event(self, event_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate analytics or UI events using MCP.
        """
        return await self._call_mcp_tool(
            tool="validate_event",
            arguments={"event": event_payload}
        )
