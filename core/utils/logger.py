"""Logging utilities for OpenClaw Mouse Control."""
import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from ..config.settings import get_config


def setup_logging(
    level: Optional[str] = None,
    log_dir: Optional[str] = None,
    file_enabled: Optional[bool] = None
) -> logging.Logger:
    """Configure logging with file and console handlers.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_dir: Directory for log files
        file_enabled: Whether to enable file logging
        
    Returns:
        Configured root logger
    """
    config = get_config()
    
    level = level or config.logging.level
    log_dir = log_dir or config.logging.log_dir
    file_enabled = file_enabled if file_enabled is not None else config.logging.file_enabled
    
    # Create logger
    logger = logging.getLogger("openclaw_mouse")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    if file_enabled:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_path / "openclaw-mouse.log",
            maxBytes=config.logging.max_file_size,
            backupCount=config.logging.backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger
