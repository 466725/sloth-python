from __future__ import annotations

import json
from pathlib import Path
from typing import Any

LOCATORS_DIR = Path(__file__).resolve().parents[1] / "locators"
SIGNINPAGE_LOCATOR_FILE = LOCATORS_DIR / "signinpage.json"
SIGNUPPAGE_LOCATOR_FILE = LOCATORS_DIR / "signuppage.json"

KEY_TO_FILE: dict[str, Path] = {
    "tangerine.login": SIGNINPAGE_LOCATOR_FILE,
    "tangerine.signup": SIGNUPPAGE_LOCATOR_FILE,
}


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _default_locator_files() -> list[Path]:
    files = [SIGNINPAGE_LOCATOR_FILE, SIGNUPPAGE_LOCATOR_FILE]
    return [path for path in files if path.exists()]


def _resolve_file_for_key(key: str, file_path: Path | None = None) -> Path:
    if file_path is not None:
        return file_path

    mapped_file = KEY_TO_FILE.get(key)
    if mapped_file is not None:
        return mapped_file

    for path in _default_locator_files():
        if key in _read_json(path):
            return path

    raise KeyError(f"Locator key not found: {key}")


def load_locators(file_path: Path | None = None) -> dict[str, Any]:
    if file_path is not None:
        return _read_json(file_path)

    merged: dict[str, Any] = {}
    for path in _default_locator_files():
        data = _read_json(path)
        overlap = set(merged).intersection(data)
        if overlap:
            overlap_list = ", ".join(sorted(overlap))
            raise ValueError(f"Duplicate locator key(s) found across split files: {overlap_list}")
        merged.update(data)

    if merged:
        return merged

    raise FileNotFoundError(
        f"No locator files found under {LOCATORS_DIR}. "
    )


def save_locators(data: dict[str, Any], file_path: Path | None = None) -> None:
    path = file_path
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
    resolved_file = _resolve_file_for_key(key, file_path=file_path)
    locators = load_locators(file_path=resolved_file)
    if key not in locators:
        raise KeyError(f"Locator key not found: {key}")
    locators[key]["primary"] = new_locator
    save_locators(locators, file_path=resolved_file)
