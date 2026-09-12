import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config.json"
REPOS_DIR = PROJECT_ROOT / "repos"
OUTPUT_DIR = PROJECT_ROOT / "output"

REPOS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)