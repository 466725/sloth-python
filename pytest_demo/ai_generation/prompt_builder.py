from __future__ import annotations

import json
from textwrap import dedent

from pytest_demo.ai_generation.mcp_context import BrowserSnapshot

SYSTEM_PROMPT = (
    "You are a senior QA automation engineer. Generate robust Python pytest + Playwright tests only. "
    "Use resilient selectors, keep assertions meaningful, and return code only."
)


def build_generation_prompt(snapshot: BrowserSnapshot, goal: str, test_name: str) -> str:
    context = {
        "url": snapshot.url,
        "title": snapshot.title,
        "dom": snapshot.dom,
        "element_tree": snapshot.element_tree,
        "network_events": snapshot.network_events,
        "mcp_payload": snapshot.to_mcp_payload(),
    }

    return dedent(
        f"""
        Goal:
        {goal}

        Create a runnable test function named `{test_name}` using pytest and Playwright sync API.
        Requirements:
        - Include imports required by the generated test.
        - Navigate to `{snapshot.url}`.
        - Verify the page with at least one assertion.
        - Prefer locator strategies that are likely stable.
        - Do not include explanations, markdown, or prose.

        Browser context (JSON):
        {json.dumps(context, ensure_ascii=True)}
        """
    ).strip()

