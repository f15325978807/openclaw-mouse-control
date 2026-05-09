"""Input service for mouse and keyboard actions."""
import logging
from typing import Optional, Tuple

from ..models.element import UIElement
from ..models.bounds import Bounds

logger = logging.getLogger(__name__)


class InputService:
    """Service for simulating user input."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> None:
        """Click at coordinates."""
        import pyautogui
        pyautogui.click(x, y, button=button, clicks=clicks)

    def click_element(self, element: UIElement, button: str = "left") -> bool:
        """Click on element center."""
        if element.bounds:
            center = element.bounds.center
            self.click(center[0], center[1], button)
            return True
        return False

    def move_to(self, x: int, y: int, duration: float = 0.2) -> None:
        """Move mouse to coordinates."""
        import pyautogui
        pyautogui.moveTo(x, y, duration=duration)

    def move_to_element(self, element: UIElement, duration: float = 0.2) -> bool:
        """Move mouse to element center."""
        if element.bounds:
            center = element.bounds.center
            self.move_to(center[0], center[1], duration)
            return True
        return False

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int,
             duration: float = 0.5, button: str = "left") -> None:
        """Drag from start to end."""
        import pyautogui
        pyautogui.moveTo(start_x, start_y)
        pyautogui.dragTo(end_x, end_y, duration=duration, button=button)

    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """Scroll mouse wheel."""
        import pyautogui
        if x is not None and y is not None:
            pyautogui.scroll(clicks, x, y)
        else:
            pyautogui.scroll(clicks)

    def type_text(self, text: str, interval: float = 0.01) -> None:
        """Type text."""
        import pyautogui
        pyautogui.write(text, interval=interval)

    def press_key(self, key: str, presses: int = 1, interval: float = 0.1) -> None:
        """Press key."""
        import pyautogui
        pyautogui.press(key, presses=presses, interval=interval)

    def hotkey(self, *keys: str) -> None:
        """Press key combination."""
        import pyautogui
        pyautogui.hotkey(*keys)

    def get_position(self) -> Tuple[int, int]:
        """Get current mouse position."""
        import pyautogui
        return pyautogui.position()
