"""目录扫描器：识别标准 skill 目录结构"""

from pathlib import Path

# 跳过的目录名
SKIP_DIRS = {"__pycache__", ".git", ".hg", ".svn", "node_modules", ".tox", ".eggs", ".mypy_cache", ".pytest_cache", ".ruff_cache"}


def scan_skills(root_dir: str | Path) -> list[Path]:
    """扫描目录，返回包含 SKILL.md 的子目录列表。

    只扫描一层（不递归），跳过隐藏目录和特殊目录。
    """
    root = Path(root_dir)
    if not root.is_dir():
        return []

    results: list[Path] = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        # 跳过隐藏目录
        if entry.name.startswith("."):
            continue
        # 跳过特殊目录
        if entry.name in SKIP_DIRS:
            continue
        # 检查是否包含 SKILL.md
        if (entry / "SKILL.md").is_file():
            results.append(entry)

    return results
