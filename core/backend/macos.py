"""macOS backend implementation using AppleScript and Quartz."""
import subprocess
import logging
from typing import Optional, List, Tuple

from .base import BaseBackend, PlatformType, WindowInfo, Point, Size

logger = logging.getLogger(__name__)


class MacOSBackend(BaseBackend):
    """macOS-specific desktop automation backend."""

    def get_platform(self) -> PlatformType:
        return PlatformType.MACOS

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
            script = 'tell application "System Events" to get {name, id} of every application process whose visible is true'
            output = subprocess.check_output(["osascript", "-e", script], text=True, timeout=5)
            # Parse output
            lines = output.strip().split(",")
            for i, line in enumerate(lines):
                name = line.strip()
                if name:
                    windows.append(WindowInfo(hwnd=i, title=name, is_visible=True))
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
            script = f'tell application "{window_info.title}" to activate'
            subprocess.run(["osascript", "-e", script], check=True, timeout=5)
            return True
        except Exception as e:
            logger.error(f"Failed to focus window: {e}")
            return False

    def open_application(self, name: str, args: Optional[List[str]] = None) -> bool:
        try:
            cmd = ["open", "-a", name] + (args or [])
            subprocess.Popen(cmd, shell=False)
            return True
        except Exception as e:
            logger.error(f"Failed to open application: {e}")
            return False

    def show_alert(self, text: str, title: str = "Alert") -> None:
        script = f'display dialog "{text}" with title "{title}" buttons {{"OK"}} default button "OK"'
        subprocess.run(["osascript", "-e", script], timeout=5)

    def show_confirm(self, text: str, title: str = "Confirm") -> bool:
        script = f'display dialog "{text}" with title "{title}" buttons {{"Cancel", "OK"}} default button "OK"'
        try:
            subprocess.run(["osascript", "-e", script], check=True, timeout=5)
            return True
        except subprocess.CalledProcessError:
            return False

    def show_prompt(self, text: str, title: str = "Input") -> str:
        script = f'display dialog "{text}" with title "{title}" default answer ""'
        try:
            output = subprocess.check_output(["osascript", "-e", script], text=True, timeout=5)
            return output.strip().split(":")[-1].strip()
        except Exception:
            return ""

    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None):
        import pyautogui
        return pyautogui.screenshot(region=region)
