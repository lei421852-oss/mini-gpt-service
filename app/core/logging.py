import logging

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def configure_logging(log_level: str) -> None:
    normalized_level = log_level.upper()
    if normalized_level not in LOG_LEVELS:
        raise ValueError(f"Unsupported log level: {log_level!r}")

    logging.basicConfig(
        level=LOG_LEVELS[normalized_level],
        format=LOG_FORMAT,
        force=True,
    )
