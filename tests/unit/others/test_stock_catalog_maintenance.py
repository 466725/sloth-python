"""Regression tests for provider-independent autocomplete catalog maintenance."""

import json
import sys
from unittest.mock import patch

from scripts import generate_index_from_csv as generator
from scripts import refresh_stock_index as refresh


def configure_catalog(monkeypatch, tmp_path):
    catalog_dir = tmp_path / "catalog"
    catalog_dir.mkdir()
    index_path = tmp_path / "stocks.index.json"
    index_path.write_text('[["existing"]]', encoding="utf-8")
    monkeypatch.setattr(generator, "CATALOG_DIR", catalog_dir)
    monkeypatch.setattr(generator, "WEB_INDEX_PATH", index_path)
    monkeypatch.setattr(generator, "require_pypinyin", lambda: True)
    monkeypatch.setattr(sys, "argv", ["generate_index_from_csv.py"])
    return catalog_dir, index_path


def write_catalog(catalog_dir, us_name="Apple Inc."):
    (catalog_dir / "stock_list_a.csv").write_text(
        "ts_code,name\n600519.SH,Example A\n", encoding="utf-8"
    )
    (catalog_dir / "stock_list_hk.csv").write_text(
        "ts_code,name\n00700.HK,Example HK\n", encoding="utf-8"
    )
    (catalog_dir / "stock_list_us.csv").write_text(
        f"ts_code,enname\nAAPL,{us_name}\n", encoding="utf-8"
    )


def test_missing_catalog_does_not_overwrite_bundled_index(monkeypatch, tmp_path):
    _, index_path = configure_catalog(monkeypatch, tmp_path)

    assert generator.main() == 1
    assert index_path.read_text(encoding="utf-8") == '[["existing"]]'


def test_incomplete_market_data_does_not_overwrite_index(monkeypatch, tmp_path):
    catalog_dir, index_path = configure_catalog(monkeypatch, tmp_path)
    write_catalog(catalog_dir, us_name="DUMMY")

    assert generator.main() == 1
    assert index_path.read_text(encoding="utf-8") == '[["existing"]]'


def test_local_catalog_rebuild_preserves_all_markets(monkeypatch, tmp_path):
    catalog_dir, index_path = configure_catalog(monkeypatch, tmp_path)
    write_catalog(catalog_dir)

    assert generator.main() == 0
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert len(index) == 3
    assert {row[0] for row in index} == {"600519.SH", "00700.HK", "AAPL"}


def test_refresh_validation_does_not_write_static_assets():
    with patch.object(refresh, "_run") as run, patch.object(refresh, "_sync_static_index") as sync:
        assert refresh.main(["--test"]) == 0

    run.assert_called_once_with(
        [sys.executable, "scripts/generate_index_from_csv.py", "--source", "csv", "--test"]
    )
    sync.assert_not_called()


def test_refresh_generator_failure_does_not_sync_assets():
    with (
        patch.object(
            refresh, "_run", side_effect=refresh.subprocess.CalledProcessError(1, "generator")
        ),
        patch.object(refresh, "_sync_static_index") as sync,
    ):
        assert refresh.main([]) == 1

    sync.assert_not_called()
