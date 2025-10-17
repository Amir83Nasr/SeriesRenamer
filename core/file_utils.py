import re
from pathlib import Path


def parse_season_episode(filename: str):
    """شماره فصل و قسمت را از روی اسم فایل تشخیص می‌دهد."""
    patterns = [
        r"[sS](\d{1,2})[eE](\d{1,2})",  # S01E02
        r"(\d{1,2})[xX](\d{1,2})",  # 1x02
        r"Season[ _-]?(\d{1,2}).*Episode[ _-]?(\d{1,2})",  # Season 2 Episode 4
        r"Fasl[ _-]?(\d{1,2}).*Ghesmat[ _-]?(\d{1,2})",  # فارسی
        r"[eE][pP]?[ _-]?(\d{1,3})",  # فقط Episode بدون فصل: E02 یا Ep02
    ]
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) == 2:
                season, episode = groups
                return int(season), int(episode)
            elif len(groups) == 1:
                episode = groups[0]
                return 1, int(episode)
    return None, None


def find_season_folders(root: Path):
    """اگر پوشه‌ی فصل وجود نداشت، فولدر اصلی برگردانده می‌شود."""
    root = Path(root)
    season_dirs = sorted(
        [
            d
            for d in root.iterdir()
            if d.is_dir() and re.search(r"season", d.name, re.IGNORECASE)
        ]
    )
    return season_dirs if season_dirs else [root]


def prepare_rename_map_for_season(
    season_path: Path,
    series_name: str,
    season_num: int,
    allowed_exts,
    include_season: bool = True,
):
    """
    ساخت نقشه تغییر نام فایل‌ها.
    include_season = False یعنی فقط شماره قسمت در نام جدید بیاد (مثلاً 'E02')
    """
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
            s_num, e_num = parse_season_episode(f.name)

            # اگر فایل خودش شماره‌ای نداره
            e_num = e_num or idx
            s_num = s_num or season_num

            if include_season:
                new_name = f"{series_name} S{s_num:02d} E{e_num:02d}{ext}"
            else:
                new_name = f"{series_name} E{e_num:02d}{ext}"

            new_path = season_path / new_name
            pairs.append((f, new_path))
            preview_lines.append((season_path.name, f.name, new_name, ext))
    return pairs, preview_lines
