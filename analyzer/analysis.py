from datetime import datetime

from .repositories import get_code_statistics, get_commits, prepare_repository


def analyze_team(team, repos_dir, start, end):
    repo = prepare_repository(team, repos_dir)
    commits = get_commits(repo, start, end)
    statistics = get_code_statistics(repo, start, end)

    dates = []
    for commit in commits:
        try:
            dates.append(datetime.fromisoformat(commit["date"].replace(" ", "T")))
        except ValueError:
            continue

    first_commit = min(dates) if dates else None
    last_commit = max(dates) if dates else None
    duration_hours = 0

    if first_commit and last_commit:
        duration_hours = round((last_commit - first_commit).total_seconds() / 3600, 2)

    authors = statistics["authors"]
    total_added = statistics["added"]
    for author, data in authors.items():
        data["percentage"] = round(data["added"] / total_added * 100, 2) if total_added > 0 else 0

    return {
        "team": team.get("name", team["name"]),
        "repository": team["repository"],
        "commits": len(commits),
        "lines_added": statistics["added"],
        "lines_deleted": statistics["deleted"],
        "net_lines": statistics["net"],
        "files_changed": statistics["files"],
        "contributors": len(authors) - 1, # Exclude ettisafxrup
        "first_commit": first_commit.isoformat() if first_commit else "",
        "last_commit": last_commit.isoformat() if last_commit else "",
        "duration_hours": duration_hours,
        "authors": authors
    }


def analyze_all(config, repos_dir):
    results = []
    start = config["hackathon"]["start"]
    end = config["hackathon"]["end"]

    print()
    print("=" * 70)
    print("FORKATHON 2026 CODE ANALYZER")
    print("=" * 70)

    for team in config["teams"]:
        try:
            result = analyze_team(team, repos_dir, start, end)
            results.append(result)
            print(
                f"[OK] {team['name']} | {result['commits']} commits | "
                f"+{result['lines_added']} / -{result['lines_deleted']}"
            )
        except Exception as error:
            print(f"[FAILED] {team['name']}: {error}")

    return sorted(
        results,
        key=lambda result: (
            -result["lines_added"],
            -result["commits"],
            result["team"].casefold()
        ),
    )