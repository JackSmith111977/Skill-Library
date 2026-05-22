"""L2 指令加载器"""

from pathlib import Path

from ..registry.parser import _split_frontmatter


def load_body(skill_path: str | Path) -> str:
    """加载 SKILL.md 的 body（不含 frontmatter）"""
    skill_md = Path(skill_path) / "SKILL.md"
    if not skill_md.is_file():
        return ""

    content = skill_md.read_text(encoding="utf-8")
    _, body = _split_frontmatter(content)
    return body.strip()
