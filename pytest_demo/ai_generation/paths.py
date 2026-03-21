from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_output_path(output_path: str | Path) -> Path:
    path = Path(output_path)
    if path.is_absolute():
        return path
    return (project_root() / path).resolve()
