from __future__ import annotations

from pathlib import Path

from ai_gen.mcp_context import BrowserSnapshot

PROMPTS_DIR = Path(__file__).with_name("prompts")


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8").strip()


SYSTEM_PROMPT = _load_prompt("system.md")


def build_generation_prompt(snapshot: BrowserSnapshot, goal: str, test_name: str) -> str:
    template = _load_prompt("generation.md")
    values = {
        "goal": goal,
        "test_name": test_name,
        "url": snapshot.url,
        "title": snapshot.title,
        "element_tree": snapshot.element_tree[:2000],
    }
    for name, value in values.items():
        template = template.replace(f"{{{name}}}", value)
    return template
