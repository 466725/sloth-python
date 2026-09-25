"""Shared logging configuration and logger creation helpers."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path

from config.config import LoggerSettings, settings

WEEKDAY_NAMES = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


class SizeLimitedFileHandler(logging.FileHandler):
    """Append to a file and truncate it when the configured size is reached."""

    def __init__(self, filename: str | os.PathLike[str], max_bytes: int, **kwargs: object):
        self.max_bytes = max_bytes
        super().__init__(filename, **kwargs)

    def emit(self, record: logging.LogRecord) -> None:
        if self.max_bytes > 0:
            self.flush()
            message_size = len(
                f"{self.format(record)}{self.terminator}".encode(
                    self.encoding or "utf-8", errors="replace"
                )
            )
            current_size = Path(self.baseFilename).stat().st_size
            if current_size + message_size > self.max_bytes:
                self._truncate()
        super().emit(record)

    def _truncate(self) -> None:
        self.flush()
        if self.stream is not None:
            self.stream.close()
        self.stream = open(
            self.baseFilename,
            mode="w",
            encoding=self.encoding,
            errors=self.errors,
        )


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
    file_path = (
        Path(configured_file)
        if configured_file
        else Path(config.log_directory) / f"{_current_weekday()}.log"
    )
    if not _has_file_handler(root_logger, file_path):
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = SizeLimitedFileHandler(
            file_path,
            max_bytes=config.max_bytes,
            encoding="utf-8",
        )
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


def _current_weekday() -> str:
    return WEEKDAY_NAMES[datetime.now().weekday()]
