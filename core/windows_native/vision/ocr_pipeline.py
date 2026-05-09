"""OCR pipeline for text recognition."""
import logging
from typing import Optional, List, Tuple
from dataclasses import dataclass

from ..models.bounds import Bounds

logger = logging.getLogger(__name__)

# Try to import OCR backends
try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
except ImportError:
    PADDLE_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


@dataclass
class OCRResult:
    """OCR recognition result."""
    text: str
    confidence: float
    bounds: Bounds


class OCRPipeline:
    """OCR pipeline with multiple backends."""

    def __init__(self, backend: str = "paddleocr"):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._backend = backend
        self._paddle_ocr: Optional[PaddleOCR] = None
        self._initialize()

    def _initialize(self) -> None:
        """Initialize OCR backend."""
        if self._backend == "paddleocr" and PADDLE_AVAILABLE:
            try:
                self._paddle_ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang='en',
                    show_log=False
                )
                self.logger.info("PaddleOCR initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize PaddleOCR: {e}")
                self._backend = "tesseract"

        if self._backend == "tesseract" and TESSERACT_AVAILABLE:
            self.logger.info("Tesseract OCR initialized")

    def recognize(self, image) -> List[OCRResult]:
        """Recognize text in image.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            List of OCR results
        """
        if self._backend == "paddleocr" and self._paddle_ocr:
            return self._recognize_paddle(image)
        elif self._backend == "tesseract" and TESSERACT_AVAILABLE:
            return self._recognize_tesseract(image)
        else:
            self.logger.warning("No OCR backend available")
            return []

    def _recognize_paddle(self, image) -> List[OCRResult]:
        """Recognize using PaddleOCR."""
        import numpy as np
        results = []
        try:
            # Convert PIL to numpy if needed
            if hasattr(image, 'convert'):
                image = np.array(image)

            result = self._paddle_ocr.ocr(image, cls=True)
            if result and result[0]:
                for line in result[0]:
                    if line:
                        bbox, (text, confidence) = line
                        x_coords = [p[0] for p in bbox]
                        y_coords = [p[1] for p in bbox]
                        bounds = Bounds(
                            x=int(min(x_coords)),
                            y=int(min(y_coords)),
                            width=int(max(x_coords) - min(x_coords)),
                            height=int(max(y_coords) - min(y_coords))
                        )
                        results.append(OCRResult(
                            text=text,
                            confidence=confidence,
                            bounds=bounds
                        ))
        except Exception as e:
            self.logger.error(f"PaddleOCR failed: {e}")
        return results

    def _recognize_tesseract(self, image) -> List[OCRResult]:
        """Recognize using Tesseract."""
        results = []
        try:
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                text = data['text'][i].strip()
                if text:
                    conf = int(data['conf'][i])
                    if conf > 0:
                        bounds = Bounds(
                            x=data['left'][i],
                            y=data['top'][i],
                            width=data['width'][i],
                            height=data['height'][i]
                        )
                        results.append(OCRResult(
                            text=text,
                            confidence=conf / 100.0,
                            bounds=bounds
                        ))
        except Exception as e:
            self.logger.error(f"Tesseract failed: {e}")
        return results

    def find_text(self, image, target_text: str) -> Optional[OCRResult]:
        """Find specific text in image."""
        results = self.recognize(image)
        target_lower = target_text.lower()
        for result in results:
            if target_lower in result.text.lower():
                return result
        return None
