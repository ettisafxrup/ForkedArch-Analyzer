import subprocess
from collections import defaultdict


def run(command, cwd=None):
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print(f"[ERROR] {command}")
        print(result.stderr)
        return ""

    return result.stdout.strip()


def prepare_repository(team, repos_dir):
    repo_name = team["name"].replace(" ", "_")
    repo_path = repos_dir / repo_name
    url = team["repository"]

    if repo_path.exists():
        print(f"[UPDATE] {team['name']}")
        run("git fetch --all --prune", cwd=repo_path)
    else:
        print(f"[CLONE] {team['name']}")
        run(f'git clone "{url}" "{repo_path}"')

    return repo_path


def get_commits(repo, start, end):
    command = (
        f'git log --all --since="{start}" --until="{end}" '
        f'--pretty=format:"%H|%an|%ae|%ad|%s" --date=iso'
    )
    output = run(command, cwd=repo)
    commits = []

    for line in output.splitlines():
        parts = line.split("|", 4)
        if len(parts) != 5:
            continue

        sha, author, email, date, message = parts
        commits.append({
            "sha": sha,
            "author": author,
            "email": email,
            "date": date,
            "message": message
        })

    return commits


def get_code_statistics(repo, start, end):
    command = (
        f'git log --all --since="{start}" --until="{end}" --numstat '
        f'--pretty=format:"COMMIT|%H|%an|%ae"'
    )
    output = run(command, cwd=repo)
    additions = 0
    deletions = 0
    files = set()
    authors = defaultdict(lambda: {
        "commits": 0,
        "added": 0,
        "deleted": 0,
        "files": 0
    })
    current_author = None

    for line in output.splitlines():
        if line.startswith("COMMIT|"):
            parts = line.split("|")
            if len(parts) >= 4:
                current_author = parts[2]
                authors[current_author]["commits"] += 1
            continue

        parts = line.split("\t")
        if len(parts) != 3:
            continue

        added, deleted, filename = parts
        if added == "-" or deleted == "-":
            continue

        try:
            added = int(added)
            deleted = int(deleted)
        except ValueError:
            continue

        additions += added
        deletions += deleted
        files.add(filename)

        if current_author:
            authors[current_author]["added"] += added
            authors[current_author]["deleted"] += deleted
            authors[current_author]["files"] += 1

    return {
        "added": additions,
        "deleted": deletions,
        "net": additions - deletions,
        "files": len(files),
        "authors": dict(authors)
    }