"""Win32 API wrapper for low-level Windows operations."""
import logging
import ctypes
from ctypes import wintypes
from typing import Optional, Tuple, List

logger = logging.getLogger(__name__)


class Win32API:
    """Wrapper for common Win32 API functions."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._user32 = ctypes.windll.user32
        self._kernel32 = ctypes.windll.kernel32

    def get_foreground_window(self) -> int:
        """Get handle of foreground window."""
        return self._user32.GetForegroundWindow()

    def get_window_text(self, hwnd: int) -> str:
        """Get window title."""
        length = self._user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buffer = ctypes.create_unicode_buffer(length + 1)
            self._user32.GetWindowTextW(hwnd, buffer, length + 1)
            return buffer.value
        return ""

    def get_window_rect(self, hwnd: int) -> Optional[Tuple[int, int, int, int]]:
        """Get window rectangle."""
        rect = wintypes.RECT()
        if self._user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return (rect.left, rect.top, rect.right, rect.bottom)
        return None

    def set_foreground_window(self, hwnd: int) -> bool:
        """Bring window to foreground."""
        return bool(self._user32.SetForegroundWindow(hwnd))

    def is_window_visible(self, hwnd: int) -> bool:
        """Check if window is visible."""
        return bool(self._user32.IsWindowVisible(hwnd))

    def get_cursor_pos(self) -> Tuple[int, int]:
        """Get current cursor position."""
        pt = wintypes.POINT()
        self._user32.GetCursorPos(ctypes.byref(pt))
        return (pt.x, pt.y)

    def set_cursor_pos(self, x: int, y: int) -> bool:
        """Set cursor position."""
        return bool(self._user32.SetCursorPos(x, y))

    def screen_to_client(self, hwnd: int, x: int, y: int) -> Tuple[int, int]:
        """Convert screen coordinates to client coordinates."""
        pt = wintypes.POINT(x, y)
        self._user32.ScreenToClient(hwnd, ctypes.byref(pt))
        return (pt.x, pt.y)

    def client_to_screen(self, hwnd: int, x: int, y: int) -> Tuple[int, int]:
        """Convert client coordinates to screen coordinates."""
        pt = wintypes.POINT(x, y)
        self._user32.ClientToScreen(hwnd, ctypes.byref(pt))
        return (pt.x, pt.y)

    def post_message(self, hwnd: int, msg: int, wparam: int = 0, lparam: int = 0) -> bool:
        """Post message to window."""
        return bool(self._user32.PostMessageW(hwnd, msg, wparam, lparam))

    def send_message(self, hwnd: int, msg: int, wparam: int = 0, lparam: int = 0) -> int:
        """Send message to window."""
        return self._user32.SendMessageW(hwnd, msg, wparam, lparam)

    def get_async_key_state(self, key_code: int) -> bool:
        """Check if key is currently pressed."""
        return bool(self._user32.GetAsyncKeyState(key_code) & 0x8000)
