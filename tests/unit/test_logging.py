import logging

import pytest

from app.core.logging import LOG_FORMAT, configure_logging


def test_configure_logging_sets_level_and_format() -> None:
    configure_logging("debug")

    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG
    assert root_logger.handlers[0].formatter._fmt == LOG_FORMAT


def test_configure_logging_rejects_unknown_level() -> None:
    with pytest.raises(ValueError, match="Unsupported log level"):
        configure_logging("verbose")
