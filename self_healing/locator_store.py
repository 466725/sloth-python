from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

# =========================
# Paths & Configuration
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]
LOCATORS_DIR = BASE_DIR / "locators"

SIGNINPAGE_LOCATOR_FILE = LOCATORS_DIR / "signinpage.json"
SIGNUPPAGE_LOCATOR_FILE = LOCATORS_DIR / "signuppage.json"

KEY_TO_FILE: Mapping[str, Path] = {
    "tangerine.login": SIGNINPAGE_LOCATOR_FILE,
    "tangerine.signup": SIGNUPPAGE_LOCATOR_FILE,
}


# =========================
# Internal Helpers
# =========================

def _read_json(path: Path) -> dict[str, Any]:
    """Read and parse a JSON file."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    """Write data to a JSON file with consistent formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def _existing_locator_files() -> list[Path]:
    """Return all existing default locator files."""
    return [
        path
        for path in (SIGNINPAGE_LOCATOR_FILE, SIGNUPPAGE_LOCATOR_FILE)
        if path.exists()
    ]


def _resolve_file_for_key(key: str, override: Path | None = None) -> Path:
    """
    Resolve which locator file contains a given key.
    Resolution order:
    1. Explicit file override
    2. Static key-to-file mapping
    3. Scan default locator files
    """
    if override is not None:
        return override

    if mapped_path := KEY_TO_FILE.get(key):
        return mapped_path

    for path in _existing_locator_files():
        if key in _read_json(path):
            return path

    raise KeyError(f"Locator key not found: {key}")


# =========================
# Public API
# =========================

def load_locators(file_path: Path | None = None) -> dict[str, Any]:
    """
    Load locators from a single file or merge all default locator files.
    """
    if file_path:
        return _read_json(file_path)

    merged: dict[str, Any] = {}

    for path in _existing_locator_files():
        data = _read_json(path)
        duplicates = merged.keys() & data.keys()
        if duplicates:
            keys = ", ".join(sorted(duplicates))
            raise ValueError(f"Duplicate locator key(s) found: {keys}")
        merged.update(data)

    if not merged:
        raise FileNotFoundError(f"No locator files found under {LOCATORS_DIR}")

    return merged


def save_locators(data: dict[str, Any], file_path: Path) -> None:
    """Persist locators to disk."""
    _write_json(file_path, data)


def get_locator(key: str, file_path: Path | None = None) -> dict[str, Any]:
    """Retrieve a single locator by key."""
    locators = load_locators(file_path)
    try:
        return locators[key]
    except KeyError:
        raise KeyError(f"Locator key not found: {key}") from None


def update_primary_locator(
        key: str,
        new_locator: dict[str, str],
        file_path: Path | None = None,
) -> None:
    """
    Update the 'primary' locator for a given key.
    """
    resolved_file = _resolve_file_for_key(key, file_path)
    locators = load_locators(resolved_file)

    if key not in locators:
        raise KeyError(f"Locator key not found: {key}")

    locators[key]["primary"] = new_locator
    save_locators(locators, resolved_file)
