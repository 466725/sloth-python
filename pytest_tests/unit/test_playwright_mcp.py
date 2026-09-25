import asyncio

import pytest

from utils.browser.playwright_mcp import MCPPlaywrightHelper


class FakePage:
    def __init__(self, html="<button>Save</button>"):
        self.html = html
        self.content_calls = 0

    async def content(self):
        self.content_calls += 1
        return self.html


class FakeMCPClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    async def call_tool(self, *, tool, arguments):
        self.calls.append((tool, arguments))
        return self.responses.get(tool, {})


@pytest.mark.unit
def test_analyze_page_sends_page_html_to_mcp():
    client = FakeMCPClient({"analyze_dom": {"summary": "button found"}})
    page = FakePage()
    helper = MCPPlaywrightHelper(client)

    result = asyncio.run(helper.analyze_page(page))

    assert result == {"summary": "button found"}
    assert client.calls == [("analyze_dom", {"html": "<button>Save</button>"})]
    assert page.content_calls == 1


@pytest.mark.unit
def test_suggest_locator_returns_locator_from_mcp_response():
    client = FakeMCPClient({"suggest_locator": {"locator": "button:text('Save')"}})
    helper = MCPPlaywrightHelper(client)

    result = asyncio.run(helper.suggest_locator(FakePage(), "Save button"))

    assert result == "button:text('Save')"


@pytest.mark.unit
def test_suggest_locator_returns_empty_string_when_mcp_has_no_locator():
    helper = MCPPlaywrightHelper(FakeMCPClient({"suggest_locator": {}}))

    result = asyncio.run(helper.suggest_locator(FakePage(), "Save button"))

    assert result == ""


@pytest.mark.unit
def test_validate_event_passes_payload_to_mcp():
    client = FakeMCPClient({"validate_event": {"valid": True}})
    helper = MCPPlaywrightHelper(client)
    payload = {"name": "signup", "value": 1}

    result = asyncio.run(helper.validate_event(payload))

    assert result == {"valid": True}
    assert client.calls == [("validate_event", {"event": payload})]


@pytest.mark.unit
def test_suggest_locator_rejects_empty_description():
    helper = MCPPlaywrightHelper(FakeMCPClient({}))

    with pytest.raises(ValueError, match="description must not be empty"):
        asyncio.run(helper.suggest_locator(FakePage(), "  "))


@pytest.mark.unit
def test_legacy_private_helpers_still_delegate_to_public_methods():
    client = FakeMCPClient({"analyze_dom": {"ok": True}})
    helper = MCPPlaywrightHelper(client)

    result = asyncio.run(helper._call_mcp_tool("analyze_dom", {"html": "<p />"}))

    assert result == {"ok": True}