# Forkathon Repository Analyzer

This tool scans every repository configured in `config.json` for the hackathon
time window and prints a complete comparison directly in the console. It does
not require an image template or generate a progress image.

The console report includes:

- Overall totals for commits, additions, deletions, net lines, files, and authors
- A ranked team comparison
- Repository URL, first and last commit, and active development span
- Contributor-level commits, line changes, file touches, and contribution share

It also writes two optional CSV exports to `output/`:

- `team_statistics.csv`
- `member_statistics.csv`

## Run

Install the dependencies, then run:

```text
python analyzer.py
```

The analyzer updates or clones the repositories listed in `config.json`, scans
their Git history, prints the report, and refreshes the CSV exports.

## Configuration

Edit `config.json` to change the hackathon name, start/end timestamps, or the
repositories that should be scanned. Repository directories are stored under
`repos/`.
