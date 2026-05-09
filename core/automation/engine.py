"""Automation engine that orchestrates desktop actions."""
import platform
import logging
from typing import Optional, Type

from ..backend.base import BaseBackend
from ..backend.windows import WindowsBackend
from ..backend.macos import MacOSBackend
from ..backend.linux import LinuxBackend
from ..config.settings import get_config
from ..utils.logger import setup_logging
from ..utils.security import SecurityManager

logger = logging.getLogger(__name__)


class AutomationEngine:
    """Main automation engine with cross-platform backend support."""

    _instance: Optional["AutomationEngine"] = None
    _backend: Optional[BaseBackend] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.config = get_config()
        self.security = SecurityManager()
        self._backend = self._create_backend()
        logger.info(f"AutomationEngine initialized with {self._backend.get_platform().value} backend")

    def _create_backend(self) -> BaseBackend:
        """Create platform-specific backend."""
        system = platform.system()
        if system == "Windows":
            return WindowsBackend()
        elif system == "Darwin":
            return MacOSBackend()
        elif system == "Linux":
            return LinuxBackend()
        else:
            raise RuntimeError(f"Unsupported platform: {system}")

    @property
    def backend(self) -> BaseBackend:
        """Get current backend instance."""
        if self._backend is None:
            self._backend = self._create_backend()
        return self._backend

    def reinitialize(self) -> None:
        """Reinitialize the engine (e.g., after config changes)."""
        self._backend = self._create_backend()
        logger.info("AutomationEngine reinitialized")


# Global engine instance
def get_engine() -> AutomationEngine:
    """Get global automation engine instance."""
    return AutomationEngine()
