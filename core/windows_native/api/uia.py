"""Windows UI Automation API wrapper using uiautomation library."""
import logging
from typing import Optional, List, Callable, Any
import re

from ..models.element import UIElement, ElementRole, WindowElement
from ..models.bounds import Bounds

logger = logging.getLogger(__name__)

# Try to import uiautomation, fallback to pywinauto
try:
    import uiautomation as uia
    UIA_AVAILABLE = True
except ImportError:
    UIA_AVAILABLE = False
    logger.warning("uiautomation not available, using fallback")


class UIAWrapper:
    """Wrapper for Windows UI Automation API."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._root = None
        self._initialize()

    def _initialize(self) -> None:
        """Initialize UIA root element."""
        if UIA_AVAILABLE:
            try:
                self._root = uia.GetRootControl()
                self.logger.info("UI Automation initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize UIA: {e}")
                self._root = None

    def get_desktop(self) -> Optional[Any]:
        """Get desktop root element."""
        return self._root

    def find_window(self, title: str, partial: bool = True,
                    timeout: int = 3) -> Optional[Any]:
        """Find window by title."""
        if not UIA_AVAILABLE:
            return None
        try:
            if partial:
                # Use regex for partial match
                pattern = re.compile(re.escape(title), re.IGNORECASE)
                windows = uia.GetRootControl().GetChildren()
                for window in windows:
                    if pattern.search(window.Name):
                        return window
                return None
            else:
                return uia.WindowControl(searchDepth=1, Name=title)
        except Exception as e:
            self.logger.error(f"Failed to find window: {e}")
            return None

    def find_element(self, parent: Any, name: Optional[str] = None,
                     automation_id: Optional[str] = None,
                     class_name: Optional[str] = None,
                     control_type: Optional[str] = None,
                     partial: bool = True) -> Optional[Any]:
        """Find child element by criteria."""
        if not UIA_AVAILABLE:
            return None
        try:
            conditions = []
            if name:
                if partial:
                    # Manual traversal for partial match
                    for child in parent.GetChildren():
                        if name.lower() in child.Name.lower():
                            return child
                    return None
                else:
                    conditions.append(lambda c: c.Name == name)
            if automation_id:
                conditions.append(lambda c: c.AutomationId == automation_id)
            if class_name:
                conditions.append(lambda c: c.ClassName == class_name)
            if control_type:
                conditions.append(lambda c: c.ControlTypeName == control_type)

            # If only name with exact match, use UIA's built-in search
            if name and not partial and len(conditions) == 1:
                return parent.GetFirstChildControl(lambda c: c.Name == name)

            # General search
            for child in parent.GetChildren():
                match = True
                for condition in conditions:
                    if not condition(child):
                        match = False
                        break
                if match:
                    return child
            return None
        except Exception as e:
            self.logger.error(f"Failed to find element: {e}")
            return None

    def find_all_elements(self, parent: Any, name: Optional[str] = None,
                          control_type: Optional[str] = None) -> List[Any]:
        """Find all matching child elements."""
        if not UIA_AVAILABLE:
            return []
        try:
            results = []
            for child in parent.GetChildren():
                match = True
                if name and name.lower() not in child.Name.lower():
                    match = False
                if control_type and child.ControlTypeName != control_type:
                    match = False
                if match:
                    results.append(child)
            return results
        except Exception as e:
            self.logger.error(f"Failed to find elements: {e}")
            return []

    def get_element_bounds(self, element: Any) -> Optional[Bounds]:
        """Get element bounding rectangle."""
        if not UIA_AVAILABLE:
            return None
        try:
            rect = element.BoundingRectangle
            return Bounds(
                x=rect.left,
                y=rect.top,
                width=rect.right - rect.left,
                height=rect.bottom - rect.top
            )
        except Exception as e:
            self.logger.error(f"Failed to get bounds: {e}")
            return None

    def get_element_info(self, element: Any) -> UIElement:
        """Convert UIA element to UIElement model."""
        if not UIA_AVAILABLE:
            return UIElement()
        try:
            bounds = self.get_element_bounds(element)
            role = self._map_control_type(element.ControlTypeName)
            return UIElement(
                name=element.Name or "",
                role=role,
                automation_id=element.AutomationId or "",
                class_name=element.ClassName or "",
                bounds=bounds,
                process_id=element.ProcessId or 0,
                handle=element.NativeWindowHandle or 0,
                is_enabled=element.IsEnabled,
                is_visible=element.IsVisible,
                is_focused=element.HasKeyboardFocus,
                value=element.GetValuePattern().Value if element.GetValuePattern() else "",
                description=element.HelpText or "",
                native_element=element
            )
        except Exception as e:
            self.logger.error(f"Failed to get element info: {e}")
            return UIElement()

    def _map_control_type(self, control_type: str) -> ElementRole:
        """Map UIA control type to ElementRole."""
        mapping = {
            "ButtonControl": ElementRole.BUTTON,
            "EditControl": ElementRole.EDIT,
            "ComboBoxControl": ElementRole.COMBOBOX,
            "ListControl": ElementRole.LIST,
            "ListItemControl": ElementRole.LISTITEM,
            "MenuControl": ElementRole.MENU,
            "MenuItemControl": ElementRole.MENUITEM,
            "WindowControl": ElementRole.WINDOW,
            "PaneControl": ElementRole.PANE,
            "DocumentControl": ElementRole.DOCUMENT,
            "HyperlinkControl": ElementRole.HYPERLINK,
            "CheckBoxControl": ElementRole.CHECKBOX,
            "RadioButtonControl": ElementRole.RADIOBUTTON,
            "SliderControl": ElementRole.SLIDER,
            "TabControl": ElementRole.TAB,
            "TabItemControl": ElementRole.TABITEM,
            "ToolBarControl": ElementRole.TOOLBAR,
            "StatusBarControl": ElementRole.STATUSBAR,
            "ProgressBarControl": ElementRole.PROGRESSBAR,
            "TreeControl": ElementRole.TREE,
            "TreeItemControl": ElementRole.TREEITEM,
        }
        return mapping.get(control_type, ElementRole.UNKNOWN)

    def click_element(self, element: Any) -> bool:
        """Click on UIA element."""
        if not UIA_AVAILABLE:
            return False
        try:
            element.Click()
            return True
        except Exception as e:
            self.logger.error(f"Failed to click element: {e}")
            return False

    def type_into_element(self, element: Any, text: str) -> bool:
        """Type text into element."""
        if not UIA_AVAILABLE:
            return False
        try:
            element.SendKeys(text)
            return True
        except Exception as e:
            self.logger.error(f"Failed to type into element: {e}")
            return False

    def get_window_tree(self, window: Any) -> WindowElement:
        """Build window tree from UIA window element."""
        if not UIA_AVAILABLE:
            return WindowElement()
        try:
            window_info = self.get_element_info(window)
            window_elem = WindowElement(
                name=window_info.name,
                role=ElementRole.WINDOW,
                automation_id=window_info.automation_id,
                class_name=window_info.class_name,
                bounds=window_info.bounds,
                process_id=window_info.process_id,
                handle=window_info.handle,
                native_element=window
            )
            self._build_tree_recursive(window, window_elem)
            return window_elem
        except Exception as e:
            self.logger.error(f"Failed to build window tree: {e}")
            return WindowElement()

    def _build_tree_recursive(self, uia_element: Any, parent_elem: UIElement) -> None:
        """Recursively build element tree."""
        try:
            for child in uia_element.GetChildren():
                child_info = self.get_element_info(child)
                child_elem = UIElement(
                    name=child_info.name,
                    role=child_info.role,
                    automation_id=child_info.automation_id,
                    class_name=child_info.class_name,
                    bounds=child_info.bounds,
                    process_id=child_info.process_id,
                    handle=child_info.handle,
                    is_enabled=child_info.is_enabled,
                    is_visible=child_info.is_visible,
                    native_element=child
                )
                parent_elem.add_child(child_elem)
                self._build_tree_recursive(child, child_elem)
        except Exception as e:
            self.logger.debug(f"Tree traversal stopped: {e}")
