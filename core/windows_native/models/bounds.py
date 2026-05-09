"""UI element bounds model."""
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Bounds:
    """Represents a rectangular region on screen."""
    x: int
    y: int
    width: int
    height: int

    @property
    def left(self) -> int:
        return self.x

    @property
    def top(self) -> int:
        return self.y

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @property
    def center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)

    @property
    def area(self) -> int:
        return self.width * self.height

    def contains(self, x: int, y: int) -> bool:
        """Check if point is inside bounds."""
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def to_tuple(self) -> Tuple[int, int, int, int]:
        """Convert to (x, y, width, height) tuple."""
        return (self.x, self.y, self.width, self.height)

    @classmethod
    def from_tuple(cls, rect: Tuple[int, int, int, int]) -> "Bounds":
        """Create from (left, top, right, bottom) tuple."""
        return cls(
            x=rect[0],
            y=rect[1],
            width=rect[2] - rect[0],
            height=rect[3] - rect[1]
        )

    def __repr__(self) -> str:
        return f"Bounds(x={self.x}, y={self.y}, w={self.width}, h={self.height})"
