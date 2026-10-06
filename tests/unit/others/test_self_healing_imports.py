"""Shared self-healing imports and repository-relative paths."""

import subprocess
import sys
from pathlib import Path

import pytest

from utils.self_healing import click, find_element, self_healing
from utils.self_healing.locator_store import get_locator


def test_public_helpers_export_existing_implementations():
    assert click is self_healing.click
    assert find_element is self_healing.find_element


@pytest.mark.parametrize("key", ["tangerine.login", "tangerine.signup"])
def test_shared_locator_files_resolve_from_unrelated_directory(tmp_path, monkeypatch, key):
    monkeypatch.chdir(tmp_path)
    locator = get_locator(key)
    assert locator["primary"]["by"]
    assert locator["primary"]["value"]


def test_robot_library_imports_without_repository_on_python_path(tmp_path):
    root = Path(__file__).resolve().parents[3]
    library = root / "tests" / "robot_tests" / "ui_suites" / "playwright_keywords.py"
    code = """
import runpy
import sys
library = runpy.run_path(sys.argv[1])
assert library["PROJECT_ROOT"] == __import__("pathlib").Path(sys.argv[2])
assert callable(library["open_browser_session"])
assert callable(library["close_browser_session"])
assert callable(library["click"])
"""
    result = subprocess.run(
        [sys.executable, "-I", "-c", code, str(library), str(root)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
