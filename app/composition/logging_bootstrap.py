import logging
from logging.handlers import TimedRotatingFileHandler

from core.config import LoggingConfig


def setup_logging(config: LoggingConfig) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(config.level)
    root_logger.handlers.clear()

    file_handler = TimedRotatingFileHandler(
        filename=config.file,
        when="H",
        interval=8,
        backupCount=2,
        utc=False,
        encoding="utf-8",
    )
    file_handler.setLevel(config.level)
    file_formatter = logging.Formatter(config.format)
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.level)
    console_formatter = logging.Formatter(config.format)
    console_handler.setFormatter(console_formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

