from .analysis import analyze_all
from .config import OUTPUT_DIR, REPOS_DIR, TEMPLATE_FILE, load_config
from .exports import generate_csv, generate_member_csv
from .rendering import generate_image


def main():
    config = load_config()
    results = analyze_all(config, REPOS_DIR)

    if not results:
        print("No team data found.")
        return

    generate_csv(results, OUTPUT_DIR)
    generate_member_csv(results, OUTPUT_DIR)
    generate_image(results, TEMPLATE_FILE, OUTPUT_DIR, config["hackathon"]["start"])

    print()
    print("=" * 70)
    print("FORKATHON ANALYSIS COMPLETE")
    print("=" * 70)