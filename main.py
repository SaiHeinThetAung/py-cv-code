from pathlib import Path
from src.preprocessor import prepare_image
from src.ocr_engine import OCR
from src.postprocessor import extract_best_name
from src.utils import save_annotated, log

def extract_ship_name(image_path: str | Path):
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(path)

    log.info(f"Processing {path.name}")

    img = prepare_image(str(path))
    ocr_result = OCR()(img)

    name, conf = extract_best_name(ocr_result)

    out_dir = Path("output/results")
    out_dir.mkdir(exist_ok=True, parents=True)
    vis_path = out_dir / f"{path.stem}_result.jpg"
    save_annotated(img, ocr_result, vis_path)

    return {
        "file": path.name,
        "name": name,
        "confidence": conf,
        "visualization": str(vis_path)
    }