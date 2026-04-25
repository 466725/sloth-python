from typing import Any, Dict


class MCPPlaywrightHelper:
    """
    Small utility class to demonstrate how Playwright tests
    can call MCP tools for AI-assisted UI testing.

    Example Usage in a Playwright Test
    @pytest.mark.asyncio
    async def test_login_flow(page, mcp_client):
        helper = MCPPlaywrightHelper(mcp_client)

        await page.goto("https://example.com")

        # Ask MCP to suggest a locator
        login_button_locator = await helper.suggest_locator(
            page,
            description="the login button"
        )

        await page.click(login_button_locator)

        # Ask MCP to analyze the page after login
        analysis = await helper.analyze_page(page)
        print("AI Page Analysis:", analysis)
    """

    def __init__(self, mcp_client):
        """
        mcp_client: an initialized MCP client instance
        """
        self.mcp = mcp_client

    async def analyze_page(self, page) -> Dict[str, Any]:
        """
        Sends the current DOM snapshot to an MCP tool for analysis.
        Useful for:
        - AI locator suggestions
        - Accessibility hints
        - Page structure understanding
        """
        dom = await page.content()

        result = await self.mcp.call_tool(
            tool="analyze_dom",
            arguments={"html": dom}
        )
        return result

    async def suggest_locator(self, page, description: str) -> str:
        """
        Ask MCP to generate a Playwright locator based on a natural-language description.
        Example: "the login button", "the search input", etc.
        """
        dom = await page.content()

        result = await self.mcp.call_tool(
            tool="suggest_locator",
            arguments={
                "html": dom,
                "description": description
            }
        )

        return result.get("locator", "")

    async def validate_event(self, event_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Example of using MCP to validate analytics or UI events.
        """
        result = await self.mcp.call_tool(
            tool="validate_event",
            arguments={"event": event_payload}
        )
        return result
