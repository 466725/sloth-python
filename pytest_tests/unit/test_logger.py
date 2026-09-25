import logging

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