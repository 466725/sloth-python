from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from utils.ai_gen.ai_client import OpenAIChatScriptClient, OpenAIClientConfig
from utils.ai_gen.generator import TestScriptCreator, ScriptClient
from utils.ai_gen.mcp_context import ContextCollector
from utils.ai_gen.paths import resolve_path
from utils.config.config import settings

POPULAR_PLAYWRIGHT_CLI = """Popular Playwright CLI commands:
  python -m playwright install
  python -m playwright install --with-deps
  python -m playwright codegen https://example.com
  python -m playwright open https://example.com
  python -m playwright screenshot https://example.com page.png
  python -m playwright pdf https://example.com page.pdf
  python -m playwright show-trace trace.zip
"""


def _parser() -> argparse.ArgumentParser:
    ai_config: Any = settings.ai_generation
    parser = argparse.ArgumentParser(
        description="Generate pytest + Playwright UI tests from live page context.",
        epilog=POPULAR_PLAYWRIGHT_CLI,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Target page URL.")
    parser.add_argument(
        "--goal",
        required=True,
        help="Natural-language test goal for the ai generator.")
    parser.add_argument(
        "--test-name",
        default="test_generated_ui_flow",
        help="Generated pytest function name.",
    )
    parser.add_argument(
        "--output",
        default=str(Path(ai_config.output_dir) / "test_generated_ui_flow.py"),
        help="Output file path for generated test script.",
    )
    parser.add_argument(
        "--model",
        default=ai_config.model,
        help="LLM model name (e.g., gpt-4.1).",
    )
    parser.add_argument(
        "--base-url",
        default=ai_config.base_url,
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
    base_url = args.base_url
    
    # Skip invalid-looking OpenAI keys (e.g., OpenRouter sk-or-v1 keys rejected by OpenAI)
    # and fall back to ANSPIRE_API_KEYS if available
    ai_config: Any = settings.ai_generation
    model = args.model
    anspire_keys_str = os.getenv("ANSPIRE_API_KEYS", "")
    anspire_keys = [k.strip() for k in anspire_keys_str.split(",") if k.strip()]
    
    if not api_key or api_key.startswith("sk-or-v1"):
        if anspire_keys:
            api_key = anspire_keys[0]
            # Always use Anspire gateway when using Anspire key, regardless of default base_url
            base_url = "https://open-gateway.anspire.cn/v6"
            # Use Anspire-supported model by default; gpt-4.1 is not available on Anspire
            if model == ai_config.model:
                model = "Doubao-Seed-2.0-lite"
        elif not api_key:
            parser.error(
                "OPENAI_API_KEY or ANSPIRE_API_KEYS is required for ai generation."
            )

    from playwright.sync_api import sync_playwright
    collector = ContextCollector(max_dom_chars=ai_config.max_dom_chars)

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
            model=model,
            base_url=(base_url or None),
        )
    )
    creator = TestScriptCreator(client)

    output_path = resolve_path(args.output)
    result = creator.create(
        snapshot=snapshot,
        goal=args.goal,
        test_name=args.test_name,
        output_path=output_path,
    )

    print(f"Generated test script: {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
