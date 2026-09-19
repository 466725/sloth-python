"""Shared logging configuration and logger creation helpers."""

from __future__ import annotations

import logging
import os
from pathlib import Path

DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DEFAULT_LOG_LEVEL = "INFO"


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name or __name__)


def configure_logging(
    level: str | int | None = None,
    log_file: str | os.PathLike[str] | None = None,
) -> logging.Logger:
    root_logger = logging.getLogger()
    root_logger.setLevel(_resolve_level(level))

    if not root_logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
        root_logger.addHandler(stream_handler)

    configured_file = log_file or os.getenv("LOG_FILE")
    if configured_file and not _has_file_handler(root_logger, configured_file):
        file_path = Path(configured_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
        root_logger.addHandler(file_handler)

    return root_logger


def _resolve_level(level: str | int | None) -> int:
    value = level if level is not None else os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)
    if isinstance(value, int):
        return value
    resolved = logging.getLevelNamesMapping().get(value.upper())
    if resolved is None:
        raise ValueError(f"Unknown logging level: {value}")
    return resolved


def _has_file_handler(logger: logging.Logger, log_file: str | os.PathLike[str]) -> bool:
    target = Path(log_file).resolve()
    return any(
        isinstance(handler, logging.FileHandler)
        and Path(handler.baseFilename).resolve() == target
        for handler in logger.handlers
    )
