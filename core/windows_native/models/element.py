"""UI Element models for Windows Native Automation."""
from dataclasses import dataclass, field
from typing import Optional, List, Any, Callable
from enum import Enum
import logging

from .bounds import Bounds

logger = logging.getLogger(__name__)


class ElementRole(Enum):
    """UI Automation control roles."""
    BUTTON = "Button"
    EDIT = "Edit"
    COMBOBOX = "ComboBox"
    LIST = "List"
    LISTITEM = "ListItem"
    MENU = "Menu"
    MENUITEM = "MenuItem"
    WINDOW = "Window"
    PANE = "Pane"
    DOCUMENT = "Document"
    HYPERLINK = "Hyperlink"
    CHECKBOX = "CheckBox"
    RADIOBUTTON = "RadioButton"
    SLIDER = "Slider"
    TAB = "Tab"
    TABITEM = "TabItem"
    TOOLBAR = "ToolBar"
    STATUSBAR = "StatusBar"
    PROGRESSBAR = "ProgressBar"
    TREE = "Tree"
    TREEITEM = "TreeItem"
    UNKNOWN = "Unknown"


@dataclass
class UIElement:
    """Base UI element model."""
    name: str = ""
    role: ElementRole = ElementRole.UNKNOWN
    automation_id: str = ""
    class_name: str = ""
    bounds: Optional[Bounds] = None
    process_id: int = 0
    handle: int = 0
    is_enabled: bool = True
    is_visible: bool = True
    is_focused: bool = False
    value: str = ""
    description: str = ""
    help_text: str = ""
    accelerator: str = ""
    access_key: str = ""
    native_element: Any = None
    _parent: Optional["UIElement"] = field(default=None, repr=False)
    _children: List["UIElement"] = field(default_factory=list, repr=False)

    @property
    def parent(self) -> Optional["UIElement"]:
        return self._parent

    @property
    def children(self) -> List["UIElement"]:
        return self._children

    @property
    def center(self) -> Optional[tuple]:
        """Get center point of element."""
        if self.bounds:
            return self.bounds.center
        return None

    def add_child(self, child: "UIElement") -> None:
        """Add child element."""
        child._parent = self
        self._children.append(child)

    def find_child(self, name: Optional[str] = None,
                   role: Optional[ElementRole] = None,
                   automation_id: Optional[str] = None,
                   class_name: Optional[str] = None) -> Optional["UIElement"]:
        """Find first matching child element."""
        for child in self._children:
            if name and name.lower() not in child.name.lower():
                continue
            if role and child.role != role:
                continue
            if automation_id and child.automation_id != automation_id:
                continue
            if class_name and child.class_name != class_name:
                continue
            return child
        return None

    def find_all_children(self, name: Optional[str] = None,
                          role: Optional[ElementRole] = None,
                          automation_id: Optional[str] = None,
                          class_name: Optional[str] = None) -> List["UIElement"]:
        """Find all matching child elements."""
        results = []
        for child in self._children:
            if name and name.lower() not in child.name.lower():
                continue
            if role and child.role != role:
                continue
            if automation_id and child.automation_id != automation_id:
                continue
            if class_name and child.class_name != class_name:
                continue
            results.append(child)
        return results

    def get_path(self) -> str:
        """Get element path from root."""
        path = []
        current = self
        while current:
            path.append(f"{current.role.value}({current.name})")
            current = current.parent
        return " -> ".join(reversed(path))

    def __repr__(self) -> str:
        return f"UIElement(name='{self.name}', role={self.role.value}, bounds={self.bounds})"


@dataclass
class ButtonElement(UIElement):
    """Button element."""
    is_default: bool = False
    is_cancel: bool = False

    def __post_init__(self):
        self.role = ElementRole.BUTTON


@dataclass
class InputElement(UIElement):
    """Input/Edit element."""
    is_read_only: bool = False
    is_password: bool = False
    max_length: int = 0
    placeholder: str = ""

    def __post_init__(self):
        self.role = ElementRole.EDIT


@dataclass
class MenuElement(UIElement):
    """Menu element."""
    items: List[UIElement] = field(default_factory=list)

    def __post_init__(self):
        self.role = ElementRole.MENU


@dataclass
class WindowElement(UIElement):
    """Window element."""
    is_maximized: bool = False
    is_minimized: bool = False
    is_active: bool = False
    title_bar: Optional[UIElement] = None
    menu_bar: Optional[UIElement] = None
    status_bar: Optional[UIElement] = None

    def __post_init__(self):
        self.role = ElementRole.WINDOW
