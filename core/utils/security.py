"""Security utilities for OpenClaw Mouse Control."""
import logging
import pyautogui
from typing import List, Optional
from ..config.settings import get_config

logger = logging.getLogger(__name__)


class SecurityManager:
    """Manages security settings and validations."""

    def __init__(self):
        self.config = get_config()
        self._setup_failsafe()

    def _setup_failsafe(self) -> None:
        """Configure PyAutoGUI failsafe."""
        pyautogui.FAILSAFE = self.config.mouse.failsafe_enabled
        if self.config.mouse.pause > 0:
            pyautogui.PAUSE = self.config.mouse.pause
        logger.info(f"Failsafe enabled: {pyautogui.FAILSAFE}")

    def is_app_whitelisted(self, app_name: str) -> bool:
        """Check if application is in whitelist."""
        if not self.config.security.whitelist_enabled:
            return True
        whitelist = [w.lower() for w in self.config.security.whitelist_apps]
        return app_name.lower() in whitelist

    def validate_coordinates(self, x: int, y: int) -> bool:
        """Validate coordinates are within screen bounds."""
        import pyautogui
        width, height = pyautogui.size()
        return 0 <= x < width and 0 <= y < height

    def sanitize_command(self, command: str) -> str:
        """Sanitize command string to prevent injection."""
        # Remove dangerous characters
        dangerous = [";", "&", "|", "`", "$", "(", ")", "{", "}", ">", "<"]
        sanitized = command
        for char in dangerous:
            sanitized = sanitized.replace(char, "")
        return sanitized.strip()

    def should_confirm_destructive(self) -> bool:
        """Check if destructive operations require confirmation."""
        return self.config.security.confirm_destructive

    def get_subprocess_timeout(self) -> int:
        """Get configured subprocess timeout."""
        return self.config.security.subprocess_timeout

    def get_max_retries(self) -> int:
        """Get configured max retry attempts."""
        return self.config.security.max_retries
