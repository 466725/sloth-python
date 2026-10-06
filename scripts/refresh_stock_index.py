#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refresh local stock autocomplete index assets.

Default flow:
1. Generate ``apps/dsa-web/public/stocks.index.json`` from local catalog CSV files
   plus JP/KR seed rows, without fetching from an external provider.
2. Copy the generated index to ``temps/static/stocks.index.json`` to mirror the local dev build output.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
WEB_INDEX_PATH = REPO_ROOT / "apps" / "dsa-web" / "public" / "stocks.index.json"
STATIC_INDEX_PATH = REPO_ROOT / "temps" / "static" / "stocks.index.json"


def _run(command: Sequence[str]) -> None:
    print(f"[refresh_stock_index] $ {' '.join(command)}", flush=True)
    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    subprocess.run(command, cwd=REPO_ROOT, check=True, env=env)


def _sync_static_index() -> None:
    if not WEB_INDEX_PATH.is_file():
        raise FileNotFoundError(f"generated Web index not found: {WEB_INDEX_PATH}")
    STATIC_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(WEB_INDEX_PATH, STATIC_INDEX_PATH)
    print(f"[refresh_stock_index] synced {WEB_INDEX_PATH} -> {STATIC_INDEX_PATH}", flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="刷新股票自动补全索引")
    parser.add_argument(
        "--source",
        choices=("csv", "akshare"),
        default="csv",
        help="Local CSV catalog (default) or existing AkShare CSV export",
    )
    parser.add_argument("--test", action="store_true", help="Validate without writing index files")
    args = parser.parse_args(argv)

    try:
        command = [sys.executable, "scripts/generate_index_from_csv.py", "--source", args.source]
        if args.test:
            command.append("--test")
        _run(command)
        if not args.test:
            _sync_static_index()

    except subprocess.CalledProcessError as exc:
        print(
            f"[refresh_stock_index] ERROR: command failed with exit code {exc.returncode}",
            file=sys.stderr,
        )
        return exc.returncode or 1
    except (OSError, RuntimeError) as exc:
        print(f"[refresh_stock_index] ERROR: {exc}", file=sys.stderr)
        return 1

    print("[refresh_stock_index] done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
