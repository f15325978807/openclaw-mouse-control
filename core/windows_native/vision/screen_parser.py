"""Screen parser combining UIA and OCR for UI understanding."""
import logging
from typing import Optional, List

from ..services.screenshot_service import ScreenshotService
from ..services.element_service import ElementService
from .ocr_pipeline import OCRPipeline
from ..models.element import UIElement, ElementRole
from ..models.bounds import Bounds

logger = logging.getLogger(__name__)


class ScreenParser:
    """Parses screen content using UIA + OCR hybrid approach."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._screenshot = ScreenshotService()
        self._element_service = ElementService()
        self._ocr = OCRPipeline()

    def parse_screen(self, window_title: Optional[str] = None) -> List[UIElement]:
        """Parse current screen and return all interactive elements.
        
        Args:
            window_title: Optional window to focus first
            
        Returns:
            List of UI elements found
        """
        elements = []

        # Try UIA first
        if window_title:
            window = self._element_service.find_window(window_title)
            if window:
                tree = self._element_service.get_window_tree()
                if tree:
                    elements = tree.get_all_elements()

        # If UIA fails or few elements found, use OCR fallback
        if len(elements) < 3:
            self.logger.info("UIA found few elements, using OCR fallback")
            ocr_elements = self._parse_with_ocr()
            elements = self._merge_elements(elements, ocr_elements)

        return elements

    def _parse_with_ocr(self) -> List[UIElement]:
        """Parse screen using OCR."""
        elements = []
        try:
            screenshot = self._screenshot.capture()
            ocr_results = self._ocr.recognize(screenshot)

            for result in ocr_results:
                element = UIElement(
                    name=result.text,
                    role=ElementRole.UNKNOWN,
                    bounds=result.bounds,
                    is_visible=True,
                    is_enabled=True
                )
                elements.append(element)
        except Exception as e:
            self.logger.error(f"OCR parsing failed: {e}")
        return elements

    def _merge_elements(self, uia_elements: List[UIElement],
                        ocr_elements: List[UIElement]) -> List[UIElement]:
        """Merge UIA and OCR results, removing duplicates."""
        merged = uia_elements.copy()
        uia_bounds = [e.bounds for e in uia_elements if e.bounds]

        for ocr_elem in ocr_elements:
            if not ocr_elem.bounds:
                continue

            # Check if OCR element overlaps with existing UIA element
            overlaps = False
            for bounds in uia_bounds:
                if self._bounds_overlap(ocr_elem.bounds, bounds):
                    overlaps = True
                    break

            if not overlaps:
                merged.append(ocr_elem)

        return merged

    def _bounds_overlap(self, a: Bounds, b: Bounds, threshold: float = 0.5) -> bool:
        """Check if two bounds overlap significantly."""
        # Calculate intersection
        left = max(a.left, b.left)
        top = max(a.top, b.top)
        right = min(a.right, b.right)
        bottom = min(a.bottom, b.bottom)

        if right < left or bottom < top:
            return False

        intersection = (right - left) * (bottom - top)
        min_area = min(a.area, b.area)

        return intersection / min_area > threshold

    def find_text_on_screen(self, text: str) -> Optional[UIElement]:
        """Find text on screen using OCR."""
        try:
            screenshot = self._screenshot.capture()
            result = self._ocr.find_text(screenshot, text)
            if result:
                return UIElement(
                    name=result.text,
                    role=ElementRole.UNKNOWN,
                    bounds=result.bounds,
                    is_visible=True
                )
        except Exception as e:
            self.logger.error(f"Text search failed: {e}")
        return None
