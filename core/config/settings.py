"""Configuration management for OpenClaw Mouse Control."""
import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class MouseConfig:
    """Mouse behavior configuration."""
    default_duration: float = 0.2
    default_drag_duration: float = 0.5
    failsafe_enabled: bool = True
    pause: float = 0.1


@dataclass
class SecurityConfig:
    """Security settings."""
    whitelist_enabled: bool = False
    whitelist_apps: List[str] = field(default_factory=list)
    confirm_destructive: bool = True
    max_retries: int = 3
    subprocess_timeout: int = 10


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    file_enabled: bool = True
    log_dir: str = "logs"
    max_file_size: int = 10_485_760  # 10MB
    backup_count: int = 5


@dataclass
class VisionConfig:
    """Vision/OCR configuration."""
    ocr_enabled: bool = False
    ocr_backend: str = "paddleocr"  # paddleocr, tesseract, easyocr
    confidence_threshold: float = 0.8
    screenshot_format: str = "png"


@dataclass
class Config:
    """Main configuration container."""
    mouse: MouseConfig = field(default_factory=MouseConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    vision: VisionConfig = field(default_factory=VisionConfig)


class ConfigManager:
    """Manages loading and saving configuration."""

    DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "mouse-config.yaml"

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = Config()
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                self._apply_config(data)
                logger.info(f"Configuration loaded from {self.config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
                self._save_config()
        else:
            self._save_config()
            logger.info("Default configuration created")

    def _apply_config(self, data: dict) -> None:
        """Apply loaded configuration data."""
        if "mouse" in data:
            self.config.mouse = MouseConfig(**data["mouse"])
        if "security" in data:
            self.config.security = SecurityConfig(**data["security"])
        if "logging" in data:
            self.config.logging = LoggingConfig(**data["logging"])
        if "vision" in data:
            self.config.vision = VisionConfig(**data["vision"])

    def _save_config(self) -> None:
        """Save current configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(self._to_dict(), f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def _to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "mouse": self.config.mouse.__dict__,
            "security": self.config.security.__dict__,
            "logging": self.config.logging.__dict__,
            "vision": self.config.vision.__dict__,
        }

    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()

    def save(self) -> None:
        """Explicitly save configuration."""
        self._save_config()


# Global config instance
_config_manager: Optional[ConfigManager] = None


def get_config() -> Config:
    """Get global configuration instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.config


def init_config(config_path: Optional[Path] = None) -> ConfigManager:
    """Initialize configuration with optional custom path."""
    global _config_manager
    _config_manager = ConfigManager(config_path)
    return _config_manager
