from __future__ import annotations

import json
from textwrap import dedent

from pytest_demo.ai_generation.mcp_context import BrowserSnapshot

SYSTEM_PROMPT = (
    "You are a senior QA automation engineer. Generate robust Python pytest + Playwright tests only. "
    "CRITICAL: Always use the pytest-playwright 'page' fixture pattern (def test_name(page: Page):). "
    "Never use manual browser lifecycle (sync_playwright, launch, close). "
    "Use resilient selectors, keep assertions meaningful, and return code only."
)


def build_generation_prompt(snapshot: BrowserSnapshot, goal: str, test_name: str) -> str:
    # Optimize context to reduce token count - only send essential info
    context = {
        "url": snapshot.url,
        "title": snapshot.title,
        "element_tree": snapshot.element_tree[:3000],  # Trim to first 3000 chars
        # Don't include full DOM, network events, or mcp_payload to reduce tokens
    }

    return dedent(
        f"""
        Goal:
        {goal}

        Create a runnable test function named `{test_name}` using pytest and Playwright sync API.
        Requirements:
        - Include imports required by the generated test.
        - Navigate to `{snapshot.url}`.
        - Verify the page with at least one meaningful assertion.
        - Prefer locator strategies (id, data-testid, text) that are likely stable.
        - Do not include explanations, markdown, or prose. Return code only.

        Page context:
        Title: {snapshot.title}
        URL: {snapshot.url}
        
        Element tree (truncated):
        {snapshot.element_tree[:2000]}
        """
    ).strip()

