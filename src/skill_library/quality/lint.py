"""质量检测引擎"""

from pathlib import Path

from .models import LintError, LintWarning, LintResult
from .rules.name_format import check_name_format
from .rules.description import check_description
from .rules.body_length import check_body_length
from .rules.references import check_references
from .rules.allowed_tools import check_allowed_tools
from .rules.metadata import check_metadata
from .rules.workflow_refs import check_workflow_refs
from .rules.workflow_steps import check_steps_complete
from .rules.workflow_gates import check_gate_markers
from .rules.workflow_deps import check_step_deps
from .rules.bloat import check_bloat


class QualityEngine:
    """质量检测引擎，执行原子 skill 7 项 lint 规则"""

    def lint_atomic(self, skill_path: str | Path, profile: str = "skill-library") -> LintResult:
        """原子 skill 7 项检测"""
        skill_path = Path(skill_path)
        errors: list[LintError] = []
        warnings: list[LintWarning] = []

        # 读取 SKILL.md
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            return LintResult(
                passed=False,
                errors=[LintError(rule="file", message=f"SKILL.md 不存在: {skill_md}")],
                score=0,
            )

        content = skill_md.read_text(encoding="utf-8")
        frontmatter, body = self._parse_frontmatter(content)

        # Rule 1: name 格式
        name_errors = check_name_format(
            frontmatter.get("name", ""),
            skill_path.name,
        )
        errors.extend(name_errors)

        # Rule 2+3: description
        desc_errors, desc_warnings = check_description(
            frontmatter.get("description", ""),
            frontmatter=frontmatter,
            profile=profile,
        )
        errors.extend(desc_errors)
        warnings.extend(desc_warnings)

        # Rule 4: body 长度
        body_warnings = check_body_length(body)
        warnings.extend(body_warnings)

        # Rule 5: 文件引用有效性
        ref_errors = check_references(skill_path, body)
        errors.extend(ref_errors)

        # Rule 6: allowed-tools（仅 skill-library profile 检查）
        if profile == "skill-library":
            at_errors = check_allowed_tools(frontmatter.get("allowed-tools"))
            errors.extend(at_errors)

        # Rule 7: metadata
        meta_warnings = check_metadata(frontmatter.get("metadata"), profile=profile)
        warnings.extend(meta_warnings)

        # E13-S2: 膨胀检测
        warnings.extend(check_bloat(skill_path))

        # 计算分数
        score = max(0, 100 - len(errors) * 10 - len(warnings) * 2)
        passed = len(errors) == 0

        return LintResult(
            passed=passed,
            errors=errors,
            warnings=warnings,
            score=score,
        )

    def lint_workflow(self, skill_path: str | Path, skills_root: str | Path | None = None, profile: str = "skill-library") -> LintResult:
        """工作流 skill 检测（7 项基础 + 4 项工作流）"""
        skill_path = Path(skill_path)
        errors: list[LintError] = []
        warnings: list[LintWarning] = []

        # 读取 SKILL.md
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            return LintResult(
                passed=False,
                errors=[LintError(rule="file", message=f"SKILL.md 不存在: {skill_md}")],
                score=0,
            )

        content = skill_md.read_text(encoding="utf-8")
        frontmatter, body = self._parse_frontmatter(content)

        # 基础 7 项规则
        errors.extend(check_name_format(frontmatter.get("name", ""), skill_path.name))
        desc_errors, desc_warnings = check_description(
            frontmatter.get("description", ""),
            frontmatter=frontmatter,
            profile=profile,
        )
        errors.extend(desc_errors)
        warnings.extend(desc_warnings)
        warnings.extend(check_body_length(body))
        errors.extend(check_references(skill_path, body))
        if profile == "skill-library":
            errors.extend(check_allowed_tools(frontmatter.get("allowed-tools")))
        warnings.extend(check_metadata(frontmatter.get("metadata"), profile=profile))
        warnings.extend(check_bloat(skill_path))

        # 工作流 4 项规则
        metadata = frontmatter.get("metadata", {})
        design_pattern = metadata.get("design-pattern", "") if isinstance(metadata, dict) else ""

        errors.extend(check_workflow_refs(skill_path, body, skills_root and Path(skills_root)))
        errors.extend(check_steps_complete(body))
        warnings.extend(check_gate_markers(body, design_pattern))
        errors.extend(check_step_deps(body))

        # 计算分数
        score = max(0, 100 - len(errors) * 10 - len(warnings) * 2)
        passed = len(errors) == 0

        return LintResult(
            passed=passed,
            errors=errors,
            warnings=warnings,
            score=score,
        )

    def _parse_frontmatter(self, content: str) -> tuple[dict, str]:
        """解析 YAML frontmatter 和 body。复用 registry.parser 的 yaml.safe_load 实现。"""
        from ..registry.parser import _split_frontmatter
        return _split_frontmatter(content)


def main():
    """CLI 入口：python -m skill_library.quality.lint <path>...

    对给定路径执行 lint 检测。支持：
    - 单个 skill 路径
    - 包含 skill 的根目录（自动扫描）
    """
    import sys
    from ..registry.scanner import scan_skills

    engine = QualityEngine()
    all_passed = True

    if len(sys.argv) < 2:
        print("Usage: python -m skill_library.quality.lint <path> [...]")
        print("  <path>  skill 目录路径或包含 skill 的根目录")
        sys.exit(1)

    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"路径不存在: {path}")
            all_passed = False
            continue

        if path.is_dir() and (path / "SKILL.md").is_file():
            skills = [path]
        elif path.is_dir():
            skills = scan_skills(path)
        else:
            print(f"无效路径: {path}")
            all_passed = False
            continue

        if not skills:
            print(f"未找到 skill: {path}")
            all_passed = False
            continue

        for skill_path in skills:
            result = engine.lint_atomic(skill_path)
            status = "PASS" if result.passed else "FAIL"
            print(f"[{status}] {skill_path.name}: score={result.score}")
            for e in result.errors:
                print(f"  ERROR: [{e.rule}] {e.message}")
            for w in result.warnings:
                print(f"  WARN:  [{w.rule}] {w.message}")
            if not result.passed:
                all_passed = False

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
