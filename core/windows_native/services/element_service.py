"""UI Element service for semantic automation."""
import logging
from typing import Optional, List, Any

from ..api.uia import UIAWrapper
from ..models.element import UIElement, ElementRole, WindowElement
from ..models.window import WindowTree

logger = logging.getLogger(__name__)


class ElementService:
    """High-level service for UI element operations."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._uia = UIAWrapper()
        self._current_window: Optional[WindowElement] = None
        self._window_tree: Optional[WindowTree] = None

    def find_window(self, title: str, partial: bool = True) -> Optional[WindowElement]:
        """Find window by title."""
        uia_window = self._uia.find_window(title, partial)
        if uia_window:
            window_elem = self._uia.get_window_tree(uia_window)
            self._current_window = window_elem
            self._window_tree = WindowTree()
            self._window_tree.build_tree(window_elem)
            return window_elem
        return None

    def find_element(self, name: Optional[str] = None,
                     role: Optional[ElementRole] = None,
                     automation_id: Optional[str] = None,
                     class_name: Optional[str] = None,
                     partial: bool = True) -> Optional[UIElement]:
        """Find element by semantic properties."""
        if not self._window_tree:
            self.logger.warning("No window tree available, call find_window first")
            return None

        # Search in window tree
        if name:
            elem = self._window_tree.find_by_name(name, partial)
            if elem:
                if role and elem.role != role:
                    pass  # Skip, will search fallback
                elif automation_id and elem.automation_id != automation_id:
                    pass
                elif class_name and elem.class_name != class_name:
                    pass
                else:
                    return elem

        # Fallback to UIA direct search
        if self._current_window and self._current_window.native_element:
            uia_elem = self._uia.find_element(
                self._current_window.native_element,
                name=name,
                automation_id=automation_id,
                class_name=class_name,
                partial=partial
            )
            if uia_elem:
                return self._uia.get_element_info(uia_elem)

        return None

    def find_all_elements(self, role: Optional[ElementRole] = None,
                          name: Optional[str] = None) -> List[UIElement]:
        """Find all matching elements."""
        if not self._window_tree:
            return []

        results = []
        if role:
            results = self._window_tree.find_by_role(role)
        if name:
            all_elems = self._window_tree.get_all_elements()
            results = [e for e in all_elems if name.lower() in e.name.lower()]

        return results

    def click_element(self, element: UIElement) -> bool:
        """Click on element."""
        if element.native_element:
            return self._uia.click_element(element.native_element)
        
        # Fallback to coordinate click
        if element.bounds:
            center = element.bounds.center
            import pyautogui
            pyautogui.click(center[0], center[1])
            return True
        return False

    def type_into_element(self, element: UIElement, text: str) -> bool:
        """Type text into element."""
        if element.native_element:
            return self._uia.type_into_element(element.native_element, text)
        
        # Fallback: click then type
        if self.click_element(element):
            import pyautogui
            pyautogui.write(text)
            return True
        return False

    def get_element_text(self, element: UIElement) -> str:
        """Get element text/value."""
        return element.value or element.name

    def is_element_enabled(self, element: UIElement) -> bool:
        """Check if element is enabled."""
        return element.is_enabled

    def is_element_visible(self, element: UIElement) -> bool:
        """Check if element is visible."""
        return element.is_visible

    def get_window_tree(self) -> Optional[WindowTree]:
        """Get current window tree."""
        return self._window_tree

    def dump_tree(self) -> str:
        """Dump current window tree."""
        if self._window_tree:
            return self._window_tree.dump_tree()
        return "No window tree available"
