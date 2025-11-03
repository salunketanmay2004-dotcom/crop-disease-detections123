"""Logger configuration module for the crop detection application."""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Set up and configure a logger instance.

    Args:
        name: Name of the logger, typically __name__ of the module.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - '
        '%(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / "crop_detection.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_level = os.getenv("LOG_LEVEL", "INFO").upper()
    console_handler.setLevel(getattr(logging, console_level, logging.INFO))
    console_handler.setFormatter(simple_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

