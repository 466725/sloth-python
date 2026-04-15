from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from pytest_demo.ai_generation.mcp_context import BrowserSnapshot
from pytest_demo.ai_generation.prompt_builder import SYSTEM_PROMPT, build_generation_prompt


class ScriptClient(Protocol):
    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        ...


@dataclass
class CreationResult:
    output_path: Path
    code: str


class TestScriptCreator:
    def __init__(self, client: ScriptClient):
        self.client = client

    def create(
            self,
            *,
            snapshot: BrowserSnapshot,
            goal: str,
            test_name: str,
            output_path: Path,
    ) -> CreationResult:
        prompt = build_generation_prompt(snapshot=snapshot, goal=goal, test_name=test_name)
        raw_code = self.client.generate(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        code = _normalize_generated_code(raw_code, test_name=test_name, url=snapshot.url)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(code, encoding="utf-8")
        return CreationResult(output_path=output_path, code=code)


def _normalize_generated_code(raw: str, *, test_name: str, url: str) -> str:
    code = _extract_code_block(raw).strip()

    if "def " not in code:
        return _fallback_template(test_name=test_name, url=url)

    if f"def {test_name}(" not in code:
        code = re.sub(r"def\s+test_[A-Za-z0-9_]+\s*\(", f"def {test_name}(", code, count=1)

    if "import pytest" not in code and "from playwright.sync_api" not in code:
        code = "import pytest\n\n" + code

    return code.rstrip() + "\n"


def _extract_code_block(raw: str) -> str:
    match = re.search(r"```(?:python)?\n(?P<code>[\s\S]*?)```", raw)
    if match:
        return match.group("code")
    return raw


def _fallback_template(*, test_name: str, url: str) -> str:
    return (
        "from playwright.sync_api import Page\n\n\n"
        f"def {test_name}(page: Page):\n"
        f"    page.goto(\"{url}\", wait_until=\"domcontentloaded\")\n"
        "    assert page.title()\n"
    )
