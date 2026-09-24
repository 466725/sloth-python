"""CSV reading helpers used by test data and examples."""

from __future__ import annotations

import csv
from collections.abc import Iterator
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def resolve_path(file_path: str | Path) -> Path:
    """Resolve relative data paths from the repository root."""
    path = Path(file_path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def read_csv(file_path: str | Path) -> Iterator[dict[str, str]]:
    """Yield CSV rows as dictionaries."""
    with resolve_path(file_path).open("r", encoding="utf-8", newline="") as file:
        yield from csv.DictReader(file)


def read_csv_to_list(
    file_path: str | Path, *, convert_to_int: bool = True
) -> list[list[int]] | list[list[str]]:
    """Read a headered CSV into rows, optionally converting values to integers."""
    with resolve_path(file_path).open("r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        rows = [row for row in reader if row]

    if not convert_to_int:
        return rows

    try:
        return [list(map(int, row)) for row in rows]
    except ValueError as error:
        raise ValueError(
            "Found non-integer cell while convert_to_int=True. "
            "Use convert_to_int=False for mixed CSV content."
        ) from error
