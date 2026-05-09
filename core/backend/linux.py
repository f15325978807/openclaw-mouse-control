"""Linux backend implementation using X11 and wmctrl."""
import subprocess
import logging
import os
from typing import Optional, List, Tuple

from .base import BaseBackend, PlatformType, WindowInfo, Point, Size

logger = logging.getLogger(__name__)


class LinuxBackend(BaseBackend):
    """Linux-specific desktop automation backend."""

    def __init__(self):
        super().__init__()
        self._display = os.environ.get("DISPLAY", ":0")
        self._is_wayland = self._check_wayland()

    def _check_wayland(self) -> bool:
        """Check if running on Wayland."""
        wayland_display = os.environ.get("WAYLAND_DISPLAY")
        xdg_session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
        return wayland_display is not None or xdg_session_type == "wayland"

    def get_platform(self) -> PlatformType:
        return PlatformType.LINUX

    def get_screen_size(self) -> Size:
        import pyautogui
        width, height = pyautogui.size()
        return Size(width, height)

    def get_mouse_position(self) -> Point:
        import pyautogui
        x, y = pyautogui.position()
        return Point(x, y)

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
        try:
            output = subprocess.check_output(["wmctrl", "-l"], text=True, timeout=5)
            for line in output.strip().split("\n"):
                parts = line.split(None, 3)
                if len(parts) >= 4:
                    hwnd = int(parts[0], 16)
                    title = parts[3]
                    if title.strip():
                        windows.append(WindowInfo(hwnd=hwnd, title=title, is_visible=True))
        except Exception as e:
            logger.error(f"Failed to get windows: {e}")
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
            subprocess.run(["wmctrl", "-i", "-a", hex(window_info.hwnd)], check=True, timeout=5)
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
        subprocess.run(["zenity", "--info", "--title", title, "--text", text], timeout=5)

    def show_confirm(self, text: str, title: str = "Confirm") -> bool:
        try:
            subprocess.run(["zenity", "--question", "--title", title, "--text", text], check=True, timeout=5)
            return True
        except subprocess.CalledProcessError:
            return False

    def show_prompt(self, text: str, title: str = "Input") -> str:
        try:
            result = subprocess.check_output(["zenity", "--entry", "--title", title, "--text", text], text=True, timeout=5)
            return result.strip()
        except Exception:
            return ""

    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None):
        import pyautogui
        return pyautogui.screenshot(region=region)
