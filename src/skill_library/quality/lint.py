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

    def lint_atomic(self, skill_path: str | Path) -> LintResult:
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
            frontmatter.get("description", "")
        )
        errors.extend(desc_errors)
        warnings.extend(desc_warnings)

        # Rule 4: body 长度
        body_warnings = check_body_length(body)
        warnings.extend(body_warnings)

        # Rule 5: 文件引用有效性
        ref_errors = check_references(skill_path, body)
        errors.extend(ref_errors)

        # Rule 6: allowed-tools
        at_errors = check_allowed_tools(frontmatter.get("allowed-tools"))
        errors.extend(at_errors)

        # Rule 7: metadata
        meta_warnings = check_metadata(frontmatter.get("metadata"))
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

    def lint_workflow(self, skill_path: str | Path, skills_root: str | Path | None = None) -> LintResult:
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
        desc_errors, desc_warnings = check_description(frontmatter.get("description", ""))
        errors.extend(desc_errors)
        warnings.extend(desc_warnings)
        warnings.extend(check_body_length(body))
        errors.extend(check_references(skill_path, body))
        errors.extend(check_allowed_tools(frontmatter.get("allowed-tools")))
        warnings.extend(check_metadata(frontmatter.get("metadata")))
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
        """解析 YAML frontmatter 和 body"""
        if not content.startswith("---"):
            return {}, content

        try:
            end = content.index("---", 3)
            yaml_content = content[3:end].strip()
            body = content[end + 3:].strip()

            # 简单解析 YAML（不依赖 pyyaml）
            frontmatter = self._simple_yaml_parse(yaml_content)
            return frontmatter, body
        except (ValueError, IndexError):
            return {}, content

    def _simple_yaml_parse(self, yaml_content: str) -> dict:
        """简单的 YAML 解析（仅支持基本键值对 + > 多行）"""
        result = {}
        fold_key = None  # 当前折叠块的 key
        fold_lines = []  # 折叠块的行
        fold_strip = False  # >- strip trailing newline

        for raw_line in yaml_content.split("\n"):
            stripped = raw_line.strip()
            if fold_key:
                # 折叠模式：缩进行属于值，非缩进行结束折叠
                if raw_line and not raw_line[0].isspace() and not raw_line.startswith("---"):
                    # 折叠结束，写入结果
                    text = " ".join(fold_lines).strip()
                    if fold_strip:
                        text = text.rstrip("\n")
                    result[fold_key] = text
                    fold_key = None
                    fold_lines = []
                    # 本行作为新键处理（fall through）
                else:
                    if stripped and not stripped.startswith("#"):
                        fold_lines.append(stripped)
                    continue

            if not stripped or stripped.startswith("#"):
                continue
            if ":" in stripped:
                key, _, value = stripped.partition(":")
                key = key.strip()
                value = value.strip()
                # 处理 > 和 >- 多行值（进入折叠模式）
                if value in (">", ">-"):
                    fold_key = key
                    fold_strip = value == ">-"
                    fold_lines = []
                    continue
                # 处理列表
                if value.startswith("[") and value.endswith("]"):
                    items = value[1:-1].split(",")
                    result[key] = [item.strip().strip("'\"") for item in items if item.strip()]
                # 处理布尔值
                elif value.lower() in ("true", "false"):
                    result[key] = value.lower() == "true"
                # 处理数字
                elif value.isdigit():
                    result[key] = int(value)
                # 处理字符串
                else:
                    result[key] = value.strip("'\"")
        # 文件结束，刷新折叠块
        if fold_key and fold_lines:
            text = " ".join(fold_lines).strip()
            if fold_strip:
                text = text.rstrip("\n")
            result[fold_key] = text
        return result
