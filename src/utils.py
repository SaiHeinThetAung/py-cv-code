import cv2
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)7s | %(message)s")
log = logging.getLogger("hull-ocr")

def save_annotated(img, result, path: Path):
    vis = img.copy()
    for line in result:
        box = line[0]
        txt, score = line[1]

        pts = np.array(box, np.int32).reshape((-1, 1, 2))
        cv2.polylines(vis, [pts], True, (0, 220, 0), 2)

        x = int(box[0][0])
        y = int(box[0][1])
        cv2.putText(vis, f"{txt} {score:.2f}", (x, y-12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imwrite(str(path), vis)
    log.info(f"Saved: {path}")