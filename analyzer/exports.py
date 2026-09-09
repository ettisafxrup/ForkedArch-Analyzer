import csv


TEAM_FIELDS = [
    "team", "repository", "commits", "lines_added", "lines_deleted",
    "net_lines", "files_changed", "contributors", "first_commit",
    "last_commit", "duration_hours"
]

MEMBER_FIELDS = [
    "team", "member", "commits", "lines_added", "lines_deleted",
    "files_changed", "contribution_percentage"
]


def generate_csv(results, output_dir):
    file = output_dir / "team_statistics.csv"
    with file.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=TEAM_FIELDS)
        writer.writeheader()
        writer.writerows({field: team[field] for field in TEAM_FIELDS} for team in results)
    print(f"[CSV] {file}")


def generate_member_csv(results, output_dir):
    file = output_dir / "member_statistics.csv"
    with file.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=MEMBER_FIELDS)
        writer.writeheader()
        for team in results:
            for member, data in team["authors"].items():
                writer.writerow({
                    "team": team["team"],
                    "member": member,
                    "commits": data["commits"],
                    "lines_added": data["added"],
                    "lines_deleted": data["deleted"],
                    "files_changed": data["files"],
                    "contribution_percentage": data["percentage"]
                })
    print(f"[CSV] {file}")