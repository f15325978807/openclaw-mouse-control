"""Window management service."""
import logging
from typing import Optional, List

from ..api.uia import UIAWrapper
from ..models.element import WindowElement

logger = logging.getLogger(__name__)


class WindowService:
    """Service for window operations."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._uia = UIAWrapper()

    def find_window(self, title: str, partial: bool = True) -> Optional[WindowElement]:
        """Find window by title."""
        uia_window = self._uia.find_window(title, partial)
        if uia_window:
            return self._uia.get_window_tree(uia_window)
        return None

    def get_all_windows(self) -> List[WindowElement]:
        """Get all visible windows."""
        windows = []
        try:
            desktop = self._uia.get_desktop()
            if desktop:
                for child in desktop.GetChildren():
                    try:
                        window = self._uia.get_window_tree(child)
                        if window and window.name:
                            windows.append(window)
                    except Exception:
                        pass
        except Exception as e:
            self.logger.error(f"Failed to get windows: {e}")
        return windows

    def focus_window(self, window: WindowElement) -> bool:
        """Focus window."""
        if window.native_element:
            try:
                window.native_element.SetFocus()
                return True
            except Exception as e:
                self.logger.error(f"Failed to focus window: {e}")
        return False

    def maximize_window(self, window: WindowElement) -> bool:
        """Maximize window."""
        if window.native_element:
            try:
                window.native_element.Maximize()
                return True
            except Exception as e:
                self.logger.error(f"Failed to maximize window: {e}")
        return False

    def minimize_window(self, window: WindowElement) -> bool:
        """Minimize window."""
        if window.native_element:
            try:
                window.native_element.Minimize()
                return True
            except Exception as e:
                self.logger.error(f"Failed to minimize window: {e}")
        return False

    def close_window(self, window: WindowElement) -> bool:
        """Close window."""
        if window.native_element:
            try:
                window.native_element.Close()
                return True
            except Exception as e:
                self.logger.error(f"Failed to close window: {e}")
        return False
