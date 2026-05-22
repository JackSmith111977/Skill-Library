"""E2-S7: lint 聚合器测试"""

import pytest
from pathlib import Path

from skill_library.quality.lint import QualityEngine
from skill_library.quality.models import LintResult


@pytest.fixture
def engine():
    return QualityEngine()


@pytest.fixture
def valid_skill(tmp_path):
    """创建合法的 skill 目录"""
    skill_path = tmp_path / "test-skill"
    skill_path.mkdir()
    (skill_path / "SKILL.md").write_text(
        """---
name: test-skill
description: This skill should be used when user asks to "test" or "check".
version: 1.0.0
---

# Test Skill

This is a test skill body.
""",
        encoding="utf-8",
    )
    return skill_path


@pytest.fixture
def invalid_skill(tmp_path):
    """创建非法的 skill 目录"""
    skill_path = tmp_path / "Invalid-Skill"
    skill_path.mkdir()
    (skill_path / "SKILL.md").write_text(
        """---
name: Invalid-Skill
description: Helps with tasks
---

Body here.
""",
        encoding="utf-8",
    )
    return skill_path


# ===== 聚合器测试 =====

def test_lint_valid(engine, valid_skill):
    """合法 skill → passed=True"""
    result = engine.lint_atomic(valid_skill)
    assert result.passed is True
    assert result.errors == []
    assert result.score == 100


def test_lint_invalid(engine, invalid_skill):
    """非法 skill → passed=False"""
    result = engine.lint_atomic(invalid_skill)
    assert result.passed is False
    assert len(result.errors) > 0


def test_lint_missing_skill_md(engine, tmp_path):
    """SKILL.md 不存在 → passed=False, score=0"""
    skill_path = tmp_path / "empty-skill"
    skill_path.mkdir()
    result = engine.lint_atomic(skill_path)
    assert result.passed is False
    assert result.score == 0


def test_lint_score_calculation(engine, invalid_skill):
    """分数计算正确"""
    result = engine.lint_atomic(invalid_skill)
    expected_score = max(0, 100 - len(result.errors) * 10 - len(result.warnings) * 2)
    assert result.score == expected_score


def test_lint_result_to_dict(engine, valid_skill):
    """LintResult.to_dict() 格式正确"""
    result = engine.lint_atomic(valid_skill)
    d = result.to_dict()
    assert "passed" in d
    assert "score" in d
    assert "errors" in d
    assert "warnings" in d
    assert isinstance(d["errors"], list)
    assert isinstance(d["warnings"], list)


# ===== frontmatter 解析 =====

def test_parse_frontmatter(engine):
    """解析 YAML frontmatter"""
    content = """---
name: test-skill
description: A test skill
version: 1.0.0
---

Body content here.
"""
    frontmatter, body = engine._parse_frontmatter(content)
    assert frontmatter["name"] == "test-skill"
    assert frontmatter["description"] == "A test skill"
    assert frontmatter["version"] == "1.0.0"
    assert "Body content here." in body


def test_parse_no_frontmatter(engine):
    """无 frontmatter"""
    content = "Just body content."
    frontmatter, body = engine._parse_frontmatter(content)
    assert frontmatter == {}
    assert body == content


def test_parse_list_in_frontmatter(engine):
    """解析列表值"""
    content = """---
name: test
allowed-tools: [Read, Bash, Write]
---

Body.
"""
    frontmatter, _ = engine._parse_frontmatter(content)
    assert frontmatter["allowed-tools"] == ["Read", "Bash", "Write"]
