"""E13-S2: Skill 膨胀检测"""

from pathlib import Path
from ..models import LintWarning


MAX_BODY_LINES = 500
MAX_BODY_WORDS = 5000
MAX_REFERENCE_FILES = 10


def check_bloat(skill_path: Path) -> list[LintWarning]:
    """检测 skill 是否违反最佳实践限制。"""
    warnings = []

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return warnings

    body = _extract_body(skill_md)
    lines = body.split("\n")
    words = body.split()

    if len(lines) > MAX_BODY_LINES:
        warnings.append(LintWarning(
            rule="bloat-lines",
            message=f"Body 共 {len(lines)} 行，超过 {MAX_BODY_LINES} 行限制",
        ))

    if len(words) > MAX_BODY_WORDS:
        warnings.append(LintWarning(
            rule="bloat-words",
            message=f"Body 共 {len(words)} 词，超过 {MAX_BODY_WORDS} 词限制",
        ))

    # 检查 reference 文件数
    ref_dir = skill_path / "references"
    if ref_dir.exists():
        ref_files = [f for f in ref_dir.iterdir() if f.is_file()]
        if len(ref_files) > MAX_REFERENCE_FILES:
            warnings.append(LintWarning(
                rule="bloat-references",
                message=f"references/ 共 {len(ref_files)} 个文件，超过 {MAX_REFERENCE_FILES} 限制",
            ))

    return warnings


def _extract_body(skill_md: Path) -> str:
    """从 SKILL.md 提取 body（去掉 frontmatter）。"""
    content = skill_md.read_text(encoding="utf-8")
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].strip()
    return content.strip()
