"""
Logging utilities for pyDQA4ProcessMining.

Provides a Logger class that writes to both console and a rotating log file.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import logging
from logging.handlers import RotatingFileHandler
from pydqa4pm.utils import constants as C


class Logger:
    """
    A logging utility that outputs to both console and a rotating log file.
    
    Attributes:
        logger_name: Name identifier for the logger instance.
    
    Example:
        >>> log = Logger("my_module")
        >>> log.info("Processing started")
        >>> log.error("An error occurred")
    """
    
    def __init__(self, logger_name: str):
        """
        Initialize the logger with console and file handlers.
        
        Args:
            logger_name: Identifier for this logger instance.
        """
        self._logger = logging.getLogger(logger_name)
        
        # Avoid adding handlers multiple times
        if not self._logger.handlers:
            log_handler = RotatingFileHandler(
                C.TRACE_FILENAME,
                mode="a",
                maxBytes=100000,
                backupCount=1,
                encoding=C.ENCODING
            )
            log_handler.setFormatter(logging.Formatter(C.TRACE_FORMAT))
            self._logger.setLevel(C.TRACE_LEVEL)
            self._logger.addHandler(log_handler)

    def _display(self, message: str) -> None:
        """Print message to console."""
        print(message)
    
    def _build_message(self, messages: tuple) -> str:
        """Concatenate multiple message parts into a single string."""
        return "".join(str(msg) for msg in messages)
    
    def info(self, *message) -> None:
        """Log an info-level message."""
        final_message = self._build_message(message)
        self._display(f"Info> {final_message}")
        self._logger.info(final_message)

    def error(self, *message) -> None:
        """Log an error-level message."""
        final_message = self._build_message(message)
        self._display(f"Error> {final_message}")
        self._logger.error(final_message)

    def debug(self, *message) -> None:
        """Log a debug-level message."""
        final_message = self._build_message(message)
        self._display(f"Debug> {final_message}")
        self._logger.debug(final_message)

    def warning(self, *message) -> None:
        """Log a warning-level message."""
        final_message = self._build_message(message)
        self._display(f"Warning> {final_message}")
        self._logger.warning(final_message)


# Alias for backward compatibility
log = Logger

