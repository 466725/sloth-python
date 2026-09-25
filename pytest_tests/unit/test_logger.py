import logging
from pathlib import Path

import pytest

from config.config import LoggerSettings
from utils.observability.logger import configure_logging, get_logger


@pytest.mark.unit
def test_get_logger_uses_requested_name():
    assert get_logger("example.component").name == "example.component"


@pytest.mark.unit
def test_configure_logging_uses_logger_settings(tmp_path):
    log_file = tmp_path / "application.log"
    logger_settings = LoggerSettings(
        level="DEBUG",
        log_file=str(log_file),
        log_format="%(levelname)s %(message)s",
    )

    root_logger = configure_logging(logger_settings=logger_settings)

    assert root_logger.level == logging.DEBUG
    assert any(
        isinstance(handler, logging.FileHandler)
        and handler.baseFilename == str(log_file)
        for handler in root_logger.handlers
    )

    for handler in root_logger.handlers:
        handler.close()
        root_logger.removeHandler(handler)


@pytest.mark.unit
def test_logger_writes_message_to_temps_log_file():
    log_file = Path("temps/logs/test_logger.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    message = "logger integration test message"
    root_logger = logging.getLogger()
    previous_level = root_logger.level
    logger_settings = LoggerSettings(
        level="INFO",
        log_file=str(log_file),
        log_format="%(levelname)s %(name)s: %(message)s",
    )

    configure_logging(logger_settings=logger_settings)
    get_logger("logger-test").info(message)

    for handler in root_logger.handlers:
        handler.flush()

    try:
        assert log_file.exists()
        assert message in log_file.read_text(encoding="utf-8")
    finally:
        for handler in list(root_logger.handlers):
            if isinstance(handler, logging.FileHandler) and Path(handler.baseFilename) == log_file.resolve():
                handler.close()
                root_logger.removeHandler(handler)
        root_logger.setLevel(previous_level)