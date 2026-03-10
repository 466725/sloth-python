from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").strip().lower(), (b or "").strip().lower()).ratio()


def _tag_score(tag: Any, expected: dict[str, Any]) -> float:
    text = tag.get_text(strip=True)
    attrs = tag.attrs or {}

    text_score = similarity(text, str(expected.get("text", "")))
    id_score = similarity(str(attrs.get("id", "")), str(expected.get("id", "")))
    class_score = similarity(" ".join(attrs.get("class", [])), str(expected.get("class", "")))
    name_score = similarity(str(attrs.get("name", "")), str(expected.get("name", "")))
    aria_score = similarity(str(attrs.get("aria-label", "")), str(expected.get("aria_label", "")))
    tag_score = 1.0 if expected.get("tag") and tag.name == expected.get("tag") else 0.0

    return (
        text_score * 0.35
        + id_score * 0.25
        + class_score * 0.15
        + name_score * 0.10
        + aria_score * 0.10
        + tag_score * 0.05
    )


def _xpath_from_tag(tag: Any) -> str:
    path_parts: list[str] = []
    current: Any = tag
    while current is not None and current.name != "[document]":
        siblings = (
            [sib for sib in current.parent.find_all(current.name, recursive=False)]
            if current.parent
            else []
        )
        if len(siblings) > 1:
            index = siblings.index(current) + 1
            path_parts.append(f"{current.name}[{index}]")
        else:
            path_parts.append(current.name)
        current = (
            current.parent
            if current.parent is not None and getattr(current.parent, "name", None)
            else None
        )
    return "/" + "/".join(reversed(path_parts))


def suggest_locator_from_candidate(candidate: Any) -> dict[str, str]:
    attrs = candidate.attrs or {}

    if attrs.get("id"):
        return {"by": "id", "value": str(attrs["id"])}
    if attrs.get("data-testid"):
        return {"by": "css", "value": f"[data-testid='{attrs['data-testid']}']"}
    if attrs.get("name"):
        return {"by": "css", "value": f"[name='{attrs['name']}']"}
    if attrs.get("class"):
        first_class = attrs["class"][0]
        return {"by": "css", "value": f"{candidate.name}.{first_class}"}

    return {"by": "xpath", "value": _xpath_from_tag(candidate)}


def find_similar_element(page_source: str, expected: dict[str, Any]) -> tuple[Any | None, float]:
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return None, 0.0

    soup = BeautifulSoup(page_source, "lxml")
    candidates = soup.find_all(True)

    best: Any | None = None
    best_score = 0.0

    for candidate in candidates:
        score = _tag_score(candidate, expected)
        if score > best_score:
            best = candidate
            best_score = score

    return best, best_score
