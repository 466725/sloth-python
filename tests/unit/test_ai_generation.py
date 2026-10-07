import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from utils.ai_gen import cli, paths
from utils.ai_gen.mcp_context import BrowserSnapshot

PROJECT_ROOT = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("module", ["ai_gen.cli", "utils.ai_gen.cli"])
def test_cli_module_help(module):
    result = subprocess.run(
        [sys.executable, "-m", module, "--help"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "--output" in result.stdout


def test_relative_output_is_resolved_from_repository_root(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    output = Path("temps/ai/generated_playwright/test_google_search_for_amazon.py")

    assert paths.project_root() == PROJECT_ROOT
    assert paths.resolve_path(output) == PROJECT_ROOT / output


def test_absolute_output_is_preserved(tmp_path):
    output = tmp_path / "test_generated.py"

    assert paths.resolve_path(output) == output


def test_cli_writes_requested_output(monkeypatch, tmp_path, capsys):
    import playwright.sync_api

    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    monkeypatch.setattr(paths, "project_root", lambda: tmp_path)
    working_dir = tmp_path / "working"
    working_dir.mkdir()
    monkeypatch.chdir(working_dir)

    runner = MagicMock()
    monkeypatch.setattr(playwright.sync_api, "sync_playwright", runner)
    browser = runner.return_value.__enter__.return_value.chromium.launch.return_value
    context = browser.new_context.return_value
    page = context.new_page.return_value
    snapshot = BrowserSnapshot(
        url="https://www.google.com",
        title="Google",
        dom="<textarea name='q'></textarea>",
        element_tree="<textarea name='q'></textarea>",
        screenshot_base64="",
        network_events=[],
    )
    collector = MagicMock()
    collector.collect.return_value = snapshot
    monkeypatch.setattr(cli, "ContextCollector", lambda **kwargs: collector)
    code = (
        "from playwright.sync_api import Page\n\n"
        "def test_google_search_for_amazon(page: Page):\n"
        "    page.goto('https://www.google.com')\n"
        "    page.locator('[name=q]').fill('Amazon')\n"
        "    page.locator('[name=q]').press('Enter')\n"
    )
    client = MagicMock()
    client.generate.return_value = f"```python\n{code}```"
    monkeypatch.setattr(cli, "OpenAIChatScriptClient", lambda config: client)
    output = Path("temps/ai/generated_playwright/test_google_search_for_amazon.py")
    goal = 'Verify Google search by searching for "Amazon" and pressing Enter'

    assert (
        cli.main(
            [
                "--url",
                snapshot.url,
                "--goal",
                goal,
                "--test-name",
                "test_google_search_for_amazon",
                "--output",
                str(output),
                "--headless",
                "true",
            ]
        )
        == 0
    )

    destination = tmp_path / output
    assert destination.read_text(encoding="utf-8") == code
    assert not (working_dir / output).exists()
    assert not (tmp_path / "utils" / output).exists()
    assert str(destination) in capsys.readouterr().out
    page.goto.assert_called_once_with(snapshot.url, wait_until="domcontentloaded")
    assert goal in client.generate.call_args.kwargs["user_prompt"]
    context.close.assert_called_once()
    browser.close.assert_called_once()


def test_missing_api_key_fails_before_browser_launch(monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(SystemExit) as exc:
        cli.main(["--url", "https://www.google.com", "--goal", "Search for Amazon"])

    assert exc.value.code == 2
    assert "OPENAI_API_KEY is required" in capsys.readouterr().err
