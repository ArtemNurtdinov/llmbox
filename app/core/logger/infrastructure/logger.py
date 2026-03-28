import logging

from app.core.logger.domain.logger import Logger


class LoggerImpl(Logger):
    def __init__(self, tag: str):
        self._app_logger = logging.getLogger(tag)

    def log_debug(self, message: str):
        self._app_logger.debug(message)

    def log_info(self, message: str):
        self._app_logger.info(message)

    def log_error(self, message: str):
        self._app_logger.error(message)

    def log_exception(self, message: str, exception: Exception):
        self._app_logger.error(message, exception, exc_info=True)

    def create_child(self, child_tag: str) -> Logger:
        return LoggerImpl(tag=child_tag)
