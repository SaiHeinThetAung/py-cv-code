from paddleocr import PaddleOCR
from .config import CONFIG

class OCR:
    def __init__(self):
        self.ocr = PaddleOCR(
            use_angle_cls=CONFIG["ocr"]["use_angle_cls"],
            lang=CONFIG["ocr"]["lang"],
            use_gpu=CONFIG["ocr"]["use_gpu"],
            cpu_math_library_num_threads=CONFIG["ocr"]["cpu_math_library_num_threads"],
            show_log=False
        )

    def __call__(self, img):
        result = self.ocr.ocr(img, cls=True)
        return result[0] if result else []