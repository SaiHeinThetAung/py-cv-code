# run.py   (hardcoded default + still supports --folder)

import argparse
from pathlib import Path
from main import extract_ship_name

DEFAULT_IMAGE = "data/shipname11.jpg"          # ← change here when needed

def main():
    parser = argparse.ArgumentParser(description="Ship Hull Name Extractor")
    parser.add_argument(
        "--folder",
        action="store_true",
        help="Process all images in data/test_images/"
    )
    args = parser.parse_args()

    if args.folder:
        folder = Path("data/test_images")
        if not folder.exists():
            print("Folder not found:", folder)
            return
        images = [p for p in folder.iterdir() if p.suffix.lower() in {'.jpg','.jpeg','.png'}]
        if not images:
            print("No images in folder")
            return
        for p in images:
            try:
                r = extract_ship_name(p)
                print(f"{p.name:30} → {r['name'] or '—':<20} ({r['confidence']:.3f})")
            except Exception as e:
                print(f"{p.name:30} → ERROR {e}")
    else:
        # default hardcoded mode when no arguments
        print(f"Using default image: {DEFAULT_IMAGE}")
        try:
            r = extract_ship_name(DEFAULT_IMAGE)
            print(f"  → {r['name'] or 'NOT FOUND':<20}  conf = {r['confidence']:.3f}")
            print(f"  Annotated → {r['visualization']}")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()