"""UI Element cache with TTL support."""
import logging
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass

from ..models.element import UIElement, WindowElement

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Cache entry with timestamp."""
    data: Any
    timestamp: float
    ttl: float

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        return time.time() - self.timestamp > self.ttl


class UICache:
    """Cache for UI elements with TTL."""

    def __init__(self, default_ttl: float = 5.0):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._elements: Dict[str, CacheEntry] = {}
        self._windows: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl

    def get_element(self, key: str) -> Optional[UIElement]:
        """Get cached element."""
        entry = self._elements.get(key)
        if entry and not entry.is_expired():
            return entry.data
        if entry:
            del self._elements[key]
        return None

    def set_element(self, key: str, element: UIElement, ttl: Optional[float] = None) -> None:
        """Cache element."""
        self._elements[key] = CacheEntry(
            data=element,
            timestamp=time.time(),
            ttl=ttl or self._default_ttl
        )

    def get_window(self, title: str) -> Optional[WindowElement]:
        """Get cached window."""
        entry = self._windows.get(title)
        if entry and not entry.is_expired():
            return entry.data
        if entry:
            del self._windows[title]
        return None

    def set_window(self, title: str, window: WindowElement, ttl: Optional[float] = None) -> None:
        """Cache window."""
        self._windows[title] = CacheEntry(
            data=window,
            timestamp=time.time(),
            ttl=ttl or self._default_ttl
        )

    def invalidate_element(self, key: str) -> None:
        """Remove element from cache."""
        if key in self._elements:
            del self._elements[key]

    def invalidate_window(self, title: str) -> None:
        """Remove window from cache."""
        if title in self._windows:
            del self._windows[title]

    def invalidate_all(self) -> None:
        """Clear all caches."""
        self._elements.clear()
        self._windows.clear()
        self.logger.debug("Cache invalidated")

    def cleanup_expired(self) -> int:
        """Remove expired entries. Returns count removed."""
        removed = 0
        expired_keys = [k for k, v in self._elements.items() if v.is_expired()]
        for key in expired_keys:
            del self._elements[key]
            removed += 1

        expired_windows = [k for k, v in self._windows.items() if v.is_expired()]
        for key in expired_windows:
            del self._windows[key]
            removed += 1

        return removed
