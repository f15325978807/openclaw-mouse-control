"""Window model for Windows Native Automation."""
from dataclasses import dataclass, field
from typing import Optional, List, Callable
import logging

from .element import WindowElement, UIElement, ElementRole
from .bounds import Bounds

logger = logging.getLogger(__name__)


@dataclass
class WindowTree:
    """Represents the window hierarchy tree."""
    root: Optional[WindowElement] = None
    _flat_cache: List[UIElement] = field(default_factory=list, repr=False)

    def build_tree(self, root_element: WindowElement) -> None:
        """Build tree from root element."""
        self.root = root_element
        self._rebuild_flat_cache()

    def _rebuild_flat_cache(self) -> None:
        """Rebuild flat element cache for fast lookup."""
        self._flat_cache = []
        if self.root:
            self._traverse(self.root)

    def _traverse(self, element: UIElement) -> None:
        """Traverse tree and add to flat cache."""
        self._flat_cache.append(element)
        for child in element.children:
            self._traverse(child)

    def find_by_name(self, name: str, partial: bool = True) -> Optional[UIElement]:
        """Find element by name."""
        name_lower = name.lower()
        for elem in self._flat_cache:
            if partial:
                if name_lower in elem.name.lower():
                    return elem
            else:
                if elem.name.lower() == name_lower:
                    return elem
        return None

    def find_by_role(self, role: ElementRole) -> List[UIElement]:
        """Find elements by role."""
        return [e for e in self._flat_cache if e.role == role]

    def find_by_automation_id(self, automation_id: str) -> Optional[UIElement]:
        """Find element by automation ID."""
        for elem in self._flat_cache:
            if elem.automation_id == automation_id:
                return elem
        return None

    def find_by_class_name(self, class_name: str) -> List[UIElement]:
        """Find elements by class name."""
        return [e for e in self._flat_cache if e.class_name == class_name]

    def find_by_bounds(self, x: int, y: int) -> Optional[UIElement]:
        """Find element containing point."""
        for elem in self._flat_cache:
            if elem.bounds and elem.bounds.contains(x, y):
                return elem
        return None

    def dump_tree(self, indent: int = 0) -> str:
        """Dump tree as formatted string."""
        if not self.root:
            return "Empty tree"
        return self._dump_element(self.root, indent)

    def _dump_element(self, element: UIElement, indent: int) -> str:
        """Dump single element and children."""
        prefix = "  " * indent
        result = f"{prefix}{element.role.value}({element.name}) [{element.bounds}]\n"
        for child in element.children:
            result += self._dump_element(child, indent + 1)
        return result

    def get_all_elements(self) -> List[UIElement]:
        """Get all elements in tree."""
        return self._flat_cache.copy()
