import re
from pathlib import Path


def parse_season_episode(filename: str):
    """شماره فصل و قسمت را از روی اسم فایل تشخیص می‌دهد."""
    patterns = [
        r"[sS](\d{1,2})[eE](\d{1,2})",  # S01E02
        r"(\d{1,2})[xX](\d{1,2})",  # 1x02
        r"Season[ _-]?(\d{1,2}).*Episode[ _-]?(\d{1,2})",  # Season 2 Episode 4
        r"Fasl[ _-]?(\d{1,2}).*Ghesmat[ _-]?(\d{1,2})",  # فارسی: Fasl 2 Ghesmat 4
    ]
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            season, episode = match.groups()
            return int(season), int(episode)
    return None, None


def find_season_folders(root: Path):
    """
    جستجوی فولدرهای فصل. اگر پیدا نشد،
    فقط پوشه‌ی اصلی برگردانده می‌شود.
    """
    root = Path(root)
    season_dirs = sorted(
        [
            d
            for d in root.iterdir()
            if d.is_dir() and re.search(r"season", d.name, re.IGNORECASE)
        ]
    )

    # اگر هیچ پوشه‌ی فصل وجود نداشت، کل فولدر اصلی را برگردان
    if not season_dirs:
        return [root]

    return season_dirs


def prepare_rename_map_for_season(
    season_path: Path, series_name: str, season_num: int, allowed_exts
):
    """لیستی از نام‌های جدید برای فایل‌ها در یک فصل تولید می‌کند."""
    all_files = [
        f
        for f in season_path.iterdir()
        if f.is_file() and f.suffix.lower() in allowed_exts
    ]
    grouped = {}
    for f in all_files:
        grouped.setdefault(f.suffix.lower(), []).append(f)

    pairs, preview_lines = [], []
    for ext in sorted(grouped.keys()):
        files = sorted(grouped[ext], key=lambda x: x.name.lower())
        for idx, f in enumerate(files, start=1):
            new_name = f"{series_name} S{season_num:02d} E{idx:02d}{ext}"
            new_path = season_path / new_name
            pairs.append((f, new_path))
            preview_lines.append((season_path.name, f.name, new_name, ext))
    return pairs, preview_lines
