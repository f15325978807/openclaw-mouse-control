"""Base backend interface for cross-platform desktop automation."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Tuple, Callable
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PlatformType(Enum):
    WINDOWS = "Windows"
    MACOS = "Darwin"
    LINUX = "Linux"


@dataclass
class WindowInfo:
    """Window information data class."""
    hwnd: int
    title: str
    class_name: Optional[str] = None
    rect: Optional[Tuple[int, int, int, int]] = None
    is_visible: bool = True


@dataclass
class Point:
    """2D point data class."""
    x: int
    y: int


@dataclass
class Size:
    """Screen size data class."""
    width: int
    height: int


class BaseBackend(ABC):
    """Abstract base class for platform-specific backends."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._hwnd_cache: dict = {}
        self._window_list_cache: Optional[List[WindowInfo]] = None
        self._cache_ttl = 1.0  # seconds
        self._last_cache_time = 0.0

    @abstractmethod
    def get_platform(self) -> PlatformType:
        """Return the current platform type."""
        pass

    @abstractmethod
    def get_screen_size(self) -> Size:
        """Get the primary screen size."""
        pass

    @abstractmethod
    def get_mouse_position(self) -> Point:
        """Get current mouse cursor position."""
        pass

    @abstractmethod
    def set_mouse_position(self, x: int, y: int, duration: float = 0.0) -> None:
        """Move mouse to specified coordinates."""
        pass

    @abstractmethod
    def mouse_click(self, x: Optional[int] = None, y: Optional[int] = None,
                    button: str = "left", clicks: int = 1) -> None:
        """Perform mouse click."""
        pass

    @abstractmethod
    def mouse_scroll(self, clicks: int, x: Optional[int] = None,
                     y: Optional[int] = None) -> None:
        """Scroll mouse wheel."""
        pass

    @abstractmethod
    def mouse_drag(self, x: int, y: int, duration: float = 0.5,
                   button: str = "left") -> None:
        """Drag mouse to coordinates."""
        pass

    @abstractmethod
    def get_visible_windows(self) -> List[WindowInfo]:
        """Get list of visible windows."""
        pass

    @abstractmethod
    def find_window(self, title: str) -> Optional[WindowInfo]:
        """Find window by title (partial match)."""
        pass

    @abstractmethod
    def focus_window(self, window_info: WindowInfo) -> bool:
        """Bring window to foreground."""
        pass

    @abstractmethod
    def open_application(self, name: str, args: Optional[List[str]] = None) -> bool:
        """Launch an application."""
        pass

    @abstractmethod
    def show_alert(self, text: str, title: str = "Alert") -> None:
        """Show alert dialog."""
        pass

    @abstractmethod
    def show_confirm(self, text: str, title: str = "Confirm") -> bool:
        """Show confirmation dialog. Returns True if OK clicked."""
        pass

    @abstractmethod
    def show_prompt(self, text: str, title: str = "Input") -> str:
        """Show input prompt dialog."""
        pass

    @abstractmethod
    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> "Image.Image":
        """Capture screenshot."""
        pass

    def invalidate_cache(self) -> None:
        """Clear internal caches."""
        self._hwnd_cache.clear()
        self._window_list_cache = None
        self.logger.debug("Cache invalidated")
