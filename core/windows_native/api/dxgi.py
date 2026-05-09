"""High-performance screenshot using DXGI Desktop Duplication."""
import logging
from typing import Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)

# DXGI is Windows-only and requires complex COM setup
# This is a simplified version using MSS as primary backend

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False
    logger.warning("mss not available, using Pillow fallback")


class DXGIScreenshot:
    """High-performance screenshot capture."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._mss = None
        self._initialize()

    def _initialize(self) -> None:
        """Initialize screenshot backend."""
        if MSS_AVAILABLE:
            try:
                self._mss = mss.mss()
                self.logger.info("MSS screenshot initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize MSS: {e}")
                self._mss = None

    def capture(self, region: Optional[Tuple[int, int, int, int]] = None,
                monitor: int = 0) -> "Image.Image":
        """Capture screenshot.
        
        Args:
            region: (x, y, width, height) or None for full screen
            monitor: Monitor index (0 = primary)
            
        Returns:
            PIL Image
        """
        if self._mss:
            return self._capture_mss(region, monitor)
        else:
            return self._capture_fallback(region)

    def _capture_mss(self, region: Optional[Tuple[int, int, int, int]],
                     monitor: int) -> "Image.Image":
        """Capture using MSS."""
        from PIL import Image
        try:
            if region:
                monitor_dict = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2],
                    "height": region[3]
                }
            else:
                # Use specified monitor
                monitors = self._mss.monitors
                if monitor < len(monitors):
                    monitor_dict = monitors[monitor]
                else:
                    monitor_dict = monitors[1] if len(monitors) > 1 else monitors[0]

            screenshot = self._mss.grab(monitor_dict)
            return Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        except Exception as e:
            self.logger.error(f"MSS capture failed: {e}")
            return self._capture_fallback(region)

    def _capture_fallback(self, region: Optional[Tuple[int, int, int, int]]) -> "Image.Image":
        """Fallback using Pillow."""
        from PIL import ImageGrab
        if region:
            return ImageGrab.grab(bbox=region)
        else:
            return ImageGrab.grab()

    def capture_all_monitors(self) -> list:
        """Capture all monitors."""
        if not self._mss:
            return [self._capture_fallback(None)]
        
        images = []
        for i, monitor in enumerate(self._mss.monitors[1:], 1):
            try:
                screenshot = self._mss.grab(monitor)
                from PIL import Image
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                images.append(img)
            except Exception as e:
                self.logger.error(f"Failed to capture monitor {i}: {e}")
        return images

    def get_monitor_info(self) -> list:
        """Get information about all monitors."""
        if not self._mss:
            return []
        return self._mss.monitors[1:]  # Skip "All in one" monitor

    def close(self) -> None:
        """Release resources."""
        if self._mss:
            self._mss.close()
            self._mss = None
