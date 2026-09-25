"""Shared logging configuration and logger creation helpers."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from config.config import LoggerSettings, settings


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name or __name__)


def configure_logging(
    level: str | int | None = None,
    log_file: str | os.PathLike[str] | None = None,
    *,
    logger_settings: LoggerSettings | None = None,
) -> logging.Logger:
    """Configure the root logger from shared settings and return it."""

    config = logger_settings or settings.logger
    root_logger = logging.getLogger()
    root_logger.setLevel(_resolve_level(level if level is not None else config.level))

    if not root_logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(config.log_format))
        root_logger.addHandler(stream_handler)

    configured_file = log_file if log_file is not None else config.log_file
    if configured_file and not _has_file_handler(root_logger, configured_file):
        file_path = Path(configured_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(config.log_format))
        root_logger.addHandler(file_handler)

    return root_logger


def _resolve_level(value: str | int) -> int:
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
