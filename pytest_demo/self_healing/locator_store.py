from __future__ import annotations

import json
from pathlib import Path
from typing import Any

LOCATOR_FILE = Path(__file__).resolve().parents[1] / "locators" / "locators.json"


def load_locators(file_path: Path | None = None) -> dict[str, Any]:
    path = file_path or LOCATOR_FILE
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_locators(data: dict[str, Any], file_path: Path | None = None) -> None:
    path = file_path or LOCATOR_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_locator(key: str, file_path: Path | None = None) -> dict[str, Any]:
    locators = load_locators(file_path=file_path)
    if key not in locators:
        raise KeyError(f"Locator key not found: {key}")
    return locators[key]


def update_primary_locator(
    key: str,
    new_locator: dict[str, str],
    file_path: Path | None = None,
) -> None:
    locators = load_locators(file_path=file_path)
    if key not in locators:
        raise KeyError(f"Locator key not found: {key}")
    locators[key]["primary"] = new_locator
    save_locators(locators, file_path=file_path)
