"""Screenshot service using high-performance backends."""
import logging
from typing import Optional, Tuple, List

from ..api.dxgi import DXGIScreenshot

logger = logging.getLogger(__name__)


class ScreenshotService:
    """Service for capturing screenshots."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._dxgi = DXGIScreenshot()

    def capture(self, region: Optional[Tuple[int, int, int, int]] = None,
                monitor: int = 0) -> "Image.Image":
        """Capture screenshot."""
        return self._dxgi.capture(region, monitor)

    def capture_all_monitors(self) -> List["Image.Image"]:
        """Capture all monitors."""
        return self._dxgi.capture_all_monitors()

    def capture_window(self, window) -> Optional["Image.Image"]:
        """Capture specific window."""
        if window and window.bounds:
            return self.capture(window.bounds.to_tuple())
        return None

    def get_monitor_info(self) -> list:
        """Get monitor information."""
        return self._dxgi.get_monitor_info()

    def close(self) -> None:
        """Release resources."""
        self._dxgi.close()
