"""Validate the regular-file collaboration instruction contract."""

import pytest

from scripts import check_ai_assets


def test_claude_entry_accepts_instructions_without_agents_file(monkeypatch, tmp_path):
    claude = tmp_path / "CLAUDE.md"
    claude.write_text(
        "# Repository instructions\n\n## Rules\nKeep changes focused.\n", encoding="utf-8"
    )
    monkeypatch.setattr(check_ai_assets, "CLAUDE", claude)
    monkeypatch.setattr(check_ai_assets, "ROOT", tmp_path)

    check_ai_assets.ensure_claude_entry()
    assert not (tmp_path / "AGENTS.md").exists()


@pytest.mark.parametrize("content", ["", "AGENTS.md", "# Repository instructions\n"])
def test_claude_entry_rejects_empty_or_pointer_content(monkeypatch, tmp_path, content):
    claude = tmp_path / "CLAUDE.md"
    claude.write_text(content, encoding="utf-8")
    monkeypatch.setattr(check_ai_assets, "CLAUDE", claude)
    monkeypatch.setattr(check_ai_assets, "ROOT", tmp_path)

    with pytest.raises(SystemExit) as error:
        check_ai_assets.ensure_claude_entry()
    assert error.value.code == 1


def test_claude_entry_rejects_missing_file(monkeypatch, tmp_path):
    monkeypatch.setattr(check_ai_assets, "CLAUDE", tmp_path / "CLAUDE.md")
    monkeypatch.setattr(check_ai_assets, "ROOT", tmp_path)

    with pytest.raises(SystemExit) as error:
        check_ai_assets.ensure_claude_entry()
    assert error.value.code == 1


def test_claude_entry_rejects_directory(monkeypatch, tmp_path):
    claude = tmp_path / "CLAUDE.md"
    claude.mkdir()
    monkeypatch.setattr(check_ai_assets, "CLAUDE", claude)
    monkeypatch.setattr(check_ai_assets, "ROOT", tmp_path)

    with pytest.raises(SystemExit) as error:
        check_ai_assets.ensure_claude_entry()
    assert error.value.code == 1
