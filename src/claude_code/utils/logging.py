"""
Logging utilities
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    rich_console: Optional[Console] = None,
) -> logging.Logger:
    """Setup logging with Rich handler"""

    # Create logger
    logger = logging.getLogger("claude_code")
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Rich console handler
    console = rich_console or Console()
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )
    rich_handler.setLevel(logging.INFO)
    logger.addHandler(rich_handler)

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get logger instance"""
    if name:
        return logging.getLogger(f"claude_code.{name}")
    return logging.getLogger("claude_code")


class LoggerMixin:
    """Mixin to add logging to classes"""

    @property
    def logger(self) -> logging.Logger:
        if not hasattr(self, "_logger"):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger
