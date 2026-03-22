from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from pytest_demo.ai_generation.ai_client import OpenAIChatScriptClient, OpenAIClientConfig
from pytest_demo.ai_generation.generator import PlaywrightTestScriptGenerator, ScriptClient
from pytest_demo.ai_generation.mcp_context import PlaywrightMCPContextCollector
from pytest_demo.ai_generation.paths import resolve_output_path
from utils.config import settings


def _parser() -> argparse.ArgumentParser:
    ai_cfg: Any = settings.ai_generation
    parser = argparse.ArgumentParser(description="Generate pytest + Playwright UI tests from live page context.")
    parser.add_argument(
        "--url",
        required=True,
        help="Target page URL.")
    parser.add_argument(
        "--goal",
        required=True,
        help="Natural-language test goal for the AI generator.")
    parser.add_argument(
        "--test-name",
        default="test_generated_ui_flow",
        help="Generated pytest function name.",
    )
    parser.add_argument(
        "--output",
        default=str(Path(ai_cfg.output_dir) / "test_generated_ui_flow.py"),
        help="Output file path for generated test script.",
    )
    parser.add_argument(
        "--model",
        default=ai_cfg.model,
        help="LLM model name (e.g., gpt-4.1).",
    )
    parser.add_argument(
        "--base-url",
        default=ai_cfg.base_url,
        help="OpenAI-compatible base URL.",
    )
    parser.add_argument(
        "--headless",
        choices=["true", "false"],
        default="true" if settings.playwright.headless else "false",
        help="Run Playwright headless or headed while collecting context.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        parser.error("OPENAI_API_KEY is required for AI generation.")

    from playwright.sync_api import sync_playwright

    ai_cfg: Any = settings.ai_generation
    collector = PlaywrightMCPContextCollector(max_dom_chars=ai_cfg.max_dom_chars)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=args.headless == "true")
        context = browser.new_context(locale=settings.ui.locale)
        page = context.new_page()

        collector.attach_network_listeners(page)
        page.goto(args.url, wait_until="domcontentloaded")
        snapshot = collector.collect(page)

        context.close()
        browser.close()

    client: ScriptClient = OpenAIChatScriptClient(
        OpenAIClientConfig(
            api_key=api_key,
            model=args.model,
            base_url=(args.base_url or None),
        )
    )
    generator = PlaywrightTestScriptGenerator(client)

    output_path = resolve_output_path(args.output)
    result = generator.generate(
        snapshot=snapshot,
        goal=args.goal,
        test_name=args.test_name,
        output_path=output_path,
    )

    print(f"Generated test script: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

