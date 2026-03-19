import csv
from collections.abc import Iterator
from pathlib import Path

# Resolve project-relative paths reliably (no matter the current working directory)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def resolve_path(file_path: str | Path) -> Path:
    """
    Convert a possibly-relative path to an absolute path.
    Relative paths are treated as relative to the project root.
    """
    p = Path(file_path)
    return p if p.is_absolute() else (PROJECT_ROOT / p)


def read_csv(file_path: str | Path) -> Iterator[dict[str, str]]:
    path = resolve_path(file_path)
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        yield from reader


def read_csv_to_list(
    file_path: str | Path, *, convert_to_int: bool = True
) -> list[list[int]] | list[list[str]]:
    path = resolve_path(file_path)
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        # skips header row
        next(reader)
        rows = [row for row in reader if row]  # skips empty rows (optional but handy)
        if not convert_to_int:
            return rows

        try:
            return [list(map(int, row)) for row in rows]
        except ValueError as error:
            raise ValueError(
                "Found non-integer cell while convert_to_int=True. "
                "Use convert_to_int=False for mixed CSV content."
            ) from error


if __name__ == "__main__":
    # Demo usage (only runs when executing this file directly)
    csv_path = "pytest_demo/theatre-data.csv"
    print(read_csv_to_list(csv_path, convert_to_int=False)[1:3])
    for row in read_csv(csv_path):
        print(row)
