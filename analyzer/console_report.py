from datetime import datetime, timezone


RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
DIM = "\033[2m"


def _supports_color():
    try:
        return __import__("sys").stdout.isatty()
    except AttributeError:
        return False


def _style(text, color=""):
    if not _supports_color() or not color:
        return str(text)
    return f"{color}{text}{RESET}"


def _number(value):
    return f"{value:,}"


def _duration(hours):
    if not hours:
        return "-"
    days, remaining = divmod(hours, 24)
    if days:
        return f"{days:.0f}d {remaining:.1f}h"
    return f"{hours:.1f}h"


def _timestamp(value):
    if not value:
        return "-"
    return datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M")


def _table(headers, rows, alignments=None):
    if not rows:
        return "(none)"

    alignments = alignments or ["left"] * len(headers)
    values = [[str(value) for value in row] for row in rows]
    widths = [len(str(header)) for header in headers]
    for row in values:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def format_row(row):
        cells = []
        for index, value in enumerate(row):
            if alignments[index] == "right":
                cells.append(value.rjust(widths[index]))
            else:
                cells.append(value.ljust(widths[index]))
        return " | ".join(cells)

    separator = "-+-".join("-" * width for width in widths)
    return "\n".join([format_row(headers), separator] + [format_row(row) for row in values])


def print_report(results, config):
    name = config["hackathon"]["name"]
    start = config["hackathon"]["start"]
    end = config["hackathon"]["end"]
    total_commits = sum(team["commits"] for team in results)
    total_added = sum(team["lines_added"] for team in results)
    total_deleted = sum(team["lines_deleted"] for team in results)
    total_files = sum(team["files_changed"] for team in results)
    total_contributors = sum(team["contributors"] for team in results)

    print()
    print(_style("=" * 100, CYAN))
    print(_style(name, BOLD + CYAN))
    print(_style("Repository comparison report", BOLD))
    print(_style("=" * 100, CYAN))
    print(f"Window: {start} -> {end}")
    print(f"Scanned repositories: {len(results)}")
    print()

    print(_style("OVERALL TOTALS", BOLD + GREEN))
    print(_table(
        ["Commits", "Lines added", "Lines deleted", "Net lines", "Files changed", "Contributors"],
        [[
            _number(total_commits), _number(total_added), _number(total_deleted),
            _number(total_added - total_deleted), _number(total_files), _number(total_contributors)
        ]],
        ["right"] * 6,
    ))
    print()

    comparison_rows = []
    for rank, team in enumerate(results, 1):
        comparison_rows.append([
            rank,
            team["team"],
            _number(team["commits"]),
            f"+{_number(team['lines_added'])}",
            f"-{_number(team['lines_deleted'])}",
            _number(team["net_lines"]),
            _number(team["files_changed"]),
            team["contributors"],
            _duration(team["duration_hours"]),
        ])

    print(_style("TEAM COMPARISON (ranked by net lines, commits, files)", BOLD + GREEN))
    print(_table(
        ["#", "Team", "Commits", "Added", "Deleted", "Net", "Files", "People", "Active span"],
        comparison_rows,
        ["right", "left", "right", "right", "right", "right", "right", "right", "right"],
    ))
    print()

    print(_style("TEAM DETAILS", BOLD + GREEN))
    for rank, team in enumerate(results, 1):
        print()
        print(_style(f"{rank:>2}. {team['team']}", BOLD + YELLOW))
        print(f"Repository: {team['repository']}")
        print(
            f"Commits: {_number(team['commits'])} | "
            f"Code: +{_number(team['lines_added'])} / -{_number(team['lines_deleted'])} "
            f"(net {_number(team['net_lines'])}) | "
            f"Files: {_number(team['files_changed'])} | "
            f"Contributors: {team['contributors']}"
        )
        print(
            f"First commit: {_timestamp(team['first_commit'])} | "
            f"Last commit: {_timestamp(team['last_commit'])} | "
            f"Active span: {_duration(team['duration_hours'])}"
        )

        member_rows = []
        authors = sorted(
            team["authors"].items(),
            key=lambda item: (-item[1]["added"], -item[1]["commits"], item[0].casefold()),
        )
        for member, data in authors:
            member_rows.append([
                member,
                data["commits"],
                _number(data["added"]),
                _number(data["deleted"]),
                data["files"],
                f"{data['percentage']:.2f}%",
            ])
        print(_table(
            ["Contributor", "Commits", "Added", "Deleted", "File touches", "Share"],
            member_rows,
            ["left", "right", "right", "right", "right", "right"],
        ))

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print()
    print(_style("=" * 100, CYAN))
    print(_style(f"Report generated: {generated_at}", DIM))