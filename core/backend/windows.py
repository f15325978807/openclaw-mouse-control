"""Windows backend implementation using ctypes and win32 APIs."""
import ctypes
from ctypes import wintypes
import subprocess
import logging
from typing import Optional, List, Tuple
import time

from .base import BaseBackend, PlatformType, WindowInfo, Point, Size

logger = logging.getLogger(__name__)


class WindowsBackend(BaseBackend):
    """Windows-specific desktop automation backend."""

    def __init__(self):
        super().__init__()
        self._user32 = ctypes.windll.user32
        self._kernel32 = ctypes.windll.kernel32
        self._enum_windows_proc_type = ctypes.WINFUNCTYPE(
            wintypes.BOOL, wintypes.HWND, wintypes.LPARAM
        )

    def get_platform(self) -> PlatformType:
        return PlatformType.WINDOWS

    def get_screen_size(self) -> Size:
        width = self._user32.GetSystemMetrics(0)
        height = self._user32.GetSystemMetrics(1)
        return Size(width, height)

    def get_mouse_position(self) -> Point:
        pt = wintypes.POINT()
        self._user32.GetCursorPos(ctypes.byref(pt))
        return Point(pt.x, pt.y)

    def set_mouse_position(self, x: int, y: int, duration: float = 0.0) -> None:
        import pyautogui
        pyautogui.moveTo(x, y, duration=duration)

    def mouse_click(self, x: Optional[int] = None, y: Optional[int] = None,
                    button: str = "left", clicks: int = 1) -> None:
        import pyautogui
        if x is not None and y is not None:
            pyautogui.click(x, y, button=button, clicks=clicks)
        else:
            pyautogui.click(button=button, clicks=clicks)

    def mouse_scroll(self, clicks: int, x: Optional[int] = None,
                     y: Optional[int] = None) -> None:
        import pyautogui
        if x is not None and y is not None:
            pyautogui.scroll(clicks, x, y)
        else:
            pyautogui.scroll(clicks)

    def mouse_drag(self, x: int, y: int, duration: float = 0.5,
                   button: str = "left") -> None:
        import pyautogui
        pyautogui.dragTo(x, y, duration=duration, button=button)

    def get_visible_windows(self) -> List[WindowInfo]:
        windows = []

        def enum_callback(hwnd, _):
            if self._user32.IsWindowVisible(hwnd):
                length = self._user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    self._user32.GetWindowTextW(hwnd, buffer, length + 1)
                    title = buffer.value
                    if title.strip():
                        rect = wintypes.RECT()
                        self._user32.GetWindowRect(hwnd, ctypes.byref(rect))
                        windows.append(WindowInfo(
                            hwnd=hwnd,
                            title=title,
                            rect=(rect.left, rect.top, rect.right, rect.bottom),
                            is_visible=True
                        ))
            return True

        proc = self._enum_windows_proc_type(enum_callback)
        self._user32.EnumWindows(proc, 0)
        return windows

    def find_window(self, title: str) -> Optional[WindowInfo]:
        windows = self.get_visible_windows()
        title_lower = title.lower()
        for win in windows:
            if title_lower in win.title.lower():
                return win
        return None

    def focus_window(self, window_info: WindowInfo) -> bool:
        try:
            self._user32.SetForegroundWindow(window_info.hwnd)
            return True
        except Exception as e:
            logger.error(f"Failed to focus window: {e}")
            return False

    def open_application(self, name: str, args: Optional[List[str]] = None) -> bool:
        try:
            cmd = [name] + (args or [])
            subprocess.Popen(cmd, shell=False)
            return True
        except Exception as e:
            logger.error(f"Failed to open application: {e}")
            return False

    def show_alert(self, text: str, title: str = "Alert") -> None:
        self._user32.MessageBoxW(0, text, title, 0x00000000)

    def show_confirm(self, text: str, title: str = "Confirm") -> bool:
        result = self._user32.MessageBoxW(0, text, title, 0x00000001)
        return result == 1  # IDOK

    def show_prompt(self, text: str, title: str = "Input") -> str:
        # Windows native input dialog would require more complex implementation
        # Fallback to console input for now
        return input(f"{text}: ")

    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None):
        import pyautogui
        return pyautogui.screenshot(region=region)
