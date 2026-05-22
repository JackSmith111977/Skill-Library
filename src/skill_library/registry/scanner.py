"""目录扫描器：识别标准 skill 目录结构"""

from pathlib import Path

# 跳过的目录名
SKIP_DIRS = {"__pycache__", ".git", ".hg", ".svn", "node_modules", ".tox", ".eggs", ".mypy_cache", ".pytest_cache", ".ruff_cache"}


def scan_skills(root_dir: str | Path) -> list[Path]:
    """扫描目录，返回包含 SKILL.md 的子目录列表。

    支持两层结构：
    - skills/<skill>/（原子 skill 直接放根目录）
    - skills/<pack>/<skill>/（skill 按包分组）
    跳过隐藏目录和特殊目录。
    """
    root = Path(root_dir)
    if not root.is_dir():
        return []

    def _is_valid_skill_dir(d: Path) -> bool:
        return (
            d.is_dir()
            and not d.name.startswith(".")
            and d.name not in SKIP_DIRS
            and (d / "SKILL.md").is_file()
        )

    results: list[Path] = []

    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name in SKIP_DIRS:
            continue

        if (entry / "SKILL.md").is_file():
            # Level 1: skills/<skill>/
            results.append(entry)
        else:
            # Level 2: skills/<pack>/<skill>/
            for sub in sorted(entry.iterdir()):
                if _is_valid_skill_dir(sub):
                    results.append(sub)

    return results
