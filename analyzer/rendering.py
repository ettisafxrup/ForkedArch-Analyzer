from pathlib import Path
import shutil
import subprocess
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont


def load_font(size):
    candidates = [
        "C:/Windows/Fonts/Arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]

    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    fc_match = shutil.which("fc-match")
    if fc_match:
        result = subprocess.run(
            [fc_match, "-f", "%{file}", "sans-serif"],
            capture_output=True,
            text=True,
            check=False
        )
        matched_font = Path(result.stdout.strip())
        if matched_font.exists():
            return ImageFont.truetype(matched_font, size)

    return ImageFont.load_default()


def centered_text(draw, text, center_x, y, font, fill=(235, 235, 235)):
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    draw.text((center_x - width / 2, y), text, font=font, fill=fill)


def generate_image(results, template_file, output_dir, hackathon_start):
    print("[IMAGE] Rendering template...")
    image = Image.open(template_file).convert("RGBA")
    draw = ImageDraw.Draw(image)
    scale_x = image.width / 1664
    scale_y = image.height / 936
    team_font = load_font(round(22 * scale_y))
    number_font = load_font(round(27 * scale_y))
    elapsed_font = load_font(round(22 * scale_y))

    team_column = round(315 * scale_x)
    columns = [
        round(value * scale_x)
        for value in [580, 780, 980, 1150, 1370, 1550]
    ]
    row_count = min(len(results), 10)
    row_positions = [
        round(y * scale_y)
        for y in (
            377 + index * (846 - 377) / max(row_count - 1, 1)
            for index in range(row_count)
        )
    ]

    for index, team in enumerate(results[:row_count]):
        y = row_positions[index]
        centered_text(draw, team["team"], team_column, y, team_font)
        values = [
            str(team["commits"]),
            f"{team['lines_added']:,}",
            f"{team['lines_deleted']:,}",
            f"{team['net_lines']:,}",
            str(team["files_changed"]),
            str(team["contributors"])
        ]
        for center_x, value in zip(columns, values):
            centered_text(draw, value, center_x, y, number_font)

    
    start = datetime.fromisoformat(hackathon_start)
    now = datetime.now(start.tzinfo)
    elapsed_hours = max(0, int((now - start).total_seconds() // 3600))
    
    centered_text(
        draw,
        f"{elapsed_hours} hours.",
        round(255 * scale_x),
        round(175 * scale_y),
        elapsed_font,
    )

    output = output_dir / "forkathon_progress.png"
    image.save(output, quality=95)
    print(f"[IMAGE] {output}")