"""模板引擎：创建标准 skill 模板并填充参数"""

import re
from pathlib import Path
from typing import Any

from ..state.enums import DesignPattern, SkillType


# 原子 skill 模板
ATOMIC_TEMPLATE = """---
name: {{name}}
description: This skill should be used when user asks to "{{description}}".
version: {{version}}
allowed-tools: []
metadata:
  skill-type: atomic
  design-pattern: tool-wrapper
  category: technical
---

# {{name}}

{{body}}
"""

# Pipeline 工作流模板
PIPELINE_TEMPLATE = """---
name: {{name}}
description: This workflow should be used when user asks to "{{description}}".
version: {{version}}
allowed-tools: [Read]
metadata:
  skill-type: workflow
  design-pattern: pipeline
  category: technical
---

# {{name}}

## Pipeline 步骤

Step 1: {{step1}}

Step 2: {{step2}}
"""

# Inversion 工作流模板
INVERSION_TEMPLATE = """---
name: {{name}}
description: This workflow should be used when user asks to "{{description}}".
version: {{version}}
allowed-tools: [Read]
metadata:
  skill-type: workflow
  design-pattern: inversion
  category: technical
---

# {{name}}

## STAGE_GATE 0

检查前置条件。

## STAGE_GATE 1

HALT. 等待用户确认。

## STAGE_GATE 2

继续执行。
"""


TEMPLATES = {
    "atomic": ATOMIC_TEMPLATE,
    "pipeline": PIPELINE_TEMPLATE,
    "inversion": INVERSION_TEMPLATE,
}


VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


def fill_template(template: str, vars: dict[str, str]) -> str:
    """替换模板中的变量。缺失变量保留原占位符。"""
    def _replace(m: re.Match) -> str:
        name = m.group(1)
        return vars.get(name, m.group(0))
    return VAR_PATTERN.sub(_replace, template)


def create_skill(
    name: str,
    output_dir: str | Path,
    *,
    skill_type: str = "atomic",
    description: str = "",
    pack: str = "default",
    version: str = "0.1.0",
    template_vars: dict[str, str] | None = None,
    design_pattern: str | None = None,
) -> Path:
    """创建标准 skill 目录结构。

    返回创建的 skill 目录路径。
    """
    # 校验
    SkillType(skill_type)
    if design_pattern:
        DesignPattern(design_pattern)

    # 确定模板
    if skill_type == "workflow":
        if design_pattern == "inversion":
            template_key = "inversion"
        else:
            template_key = "pipeline"
    else:
        template_key = "atomic"

    template = TEMPLATES[template_key]

    # 构建变量
    vars = {
        "name": name,
        "description": description,
        "version": version,
        "pack": pack,
    }
    if template_vars:
        vars.update(template_vars)

    # 填充
    content = fill_template(template, vars)

    # 创建目录
    if pack:
        skill_dir = Path(output_dir) / pack / name
    else:
        skill_dir = Path(output_dir) / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 写 SKILL.md
    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

    # 创建子目录
    for subdir in ("references", "scripts", "assets"):
        (skill_dir / subdir).mkdir(exist_ok=True)

    return skill_dir
