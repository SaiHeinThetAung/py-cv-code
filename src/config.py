from pathlib import Path
import yaml

with open(Path(__file__).parent.parent / "config.yaml") as f:
    CONFIG = yaml.safe_load(f)