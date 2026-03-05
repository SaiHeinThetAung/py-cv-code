import cv2
import numpy as np
from .config import CONFIG

def prepare_image(path: str) -> np.ndarray:
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(path)

    # resize keeping aspect ratio
    h, w = img.shape[:2]
    if max(h, w) > CONFIG["preprocess"]["max_size"]:
        s = CONFIG["preprocess"]["max_size"] / max(h, w)
        img = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)

    if CONFIG["preprocess"].get("clahe", False):
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.8, tileGridSize=(8,8))
        l = clahe.apply(l)
        img = cv2.cvtColor(cv2.merge((l,a,b)), cv2.COLOR_LAB2BGR)

    if CONFIG["preprocess"].get("sharpen", False):
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        img = cv2.filter2D(img, -1, kernel)

    return img