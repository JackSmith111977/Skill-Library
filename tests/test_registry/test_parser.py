"""E3-S2: frontmatter 解析器测试"""

import pytest
from pathlib import Path

from skill_library.registry.parser import parse_skill_md


class TestParseSkillMd:
    def test_parse_full_frontmatter(self, tmp_path):
        """解析完整字段"""
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            """---
name: test-skill
description: A test skill
version: 1.2.3
allowed-tools: [Read, Bash]
metadata:
  author: test
---

Body here.
""",
            encoding="utf-8",
        )
        result = parse_skill_md(skill)
        assert result["name"] == "test-skill"
        assert result["description"] == "A test skill"
        assert result["version"] == "1.2.3"
        assert result["allowed-tools"] == ["Read", "Bash"]
        assert result["metadata"]["author"] == "test"

    def test_parse_minimal_frontmatter(self, tmp_path):
        """仅含 name + description"""
        skill = tmp_path / "minimal"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            """---
name: minimal
description: Minimal skill
---
""",
            encoding="utf-8",
        )
        result = parse_skill_md(skill)
        assert result["name"] == "minimal"
        assert result["description"] == "Minimal skill"
        assert result["version"] == "0.0.0"  # 默认值
        assert result["allowed-tools"] == []

    def test_parse_no_frontmatter(self, tmp_path):
        """无 frontmatter 返回默认值"""
        skill = tmp_path / "no-fm"
        skill.mkdir()
        (skill / "SKILL.md").write_text("Just body content.", encoding="utf-8")
        result = parse_skill_md(skill)
        assert result["name"] == ""
        assert result["description"] == ""

    def test_parse_no_skill_md(self, tmp_path):
        """SKILL.md 不存在返回默认值"""
        result = parse_skill_md(tmp_path / "nonexistent")
        assert result["name"] == ""

    def test_parse_list_field_string(self, tmp_path):
        """allowed-tools 字符串转列表"""
        skill = tmp_path / "str-tools"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            """---
name: str-tools
description: Test
allowed-tools: Read Bash Write
---
""",
            encoding="utf-8",
        )
        result = parse_skill_md(skill)
        assert result["allowed-tools"] == ["Read", "Bash", "Write"]

    def test_parse_multiline_desc(self, tmp_path):
        """解析多行 description（> 折叠）"""
        skill = tmp_path / "multi-desc"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            """---
name: multi-desc
description: >
  This is a long
  description that spans
  multiple lines.
---
""",
            encoding="utf-8",
        )
        result = parse_skill_md(skill)
        assert "long" in result["description"]

    def test_parse_invalid_yaml(self, tmp_path):
        """无效 YAML 返回默认值"""
        skill = tmp_path / "bad-yaml"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            """---
name: [invalid yaml
---
""",
            encoding="utf-8",
        )
        result = parse_skill_md(skill)
        # 无效 YAML 应返回默认值
        assert result["name"] == ""
