import sys

from .analysis import analyze_all
from .config import OUTPUT_DIR, REPOS_DIR, load_config
from .console_report import print_report
from .exports import generate_csv, generate_member_csv


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    config = load_config()
    results = analyze_all(config, REPOS_DIR)

    if not results:
        print("No team data found.")
        return

    generate_csv(results, OUTPUT_DIR)
    generate_member_csv(results, OUTPUT_DIR)
    print_report(results, config)