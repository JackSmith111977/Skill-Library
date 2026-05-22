"""E2-S8: lint CLI 测试"""

import pytest
from click.testing import CliRunner
from pathlib import Path

from skill_library.cli.main import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def valid_skill(tmp_path):
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


def test_lint_pass(runner, valid_skill):
    """合法 skill → exit code 0"""
    result = runner.invoke(cli, ["lint", str(valid_skill)])
    assert result.exit_code == 0
    assert "PASSED" in result.output


def test_lint_fail(runner, invalid_skill):
    """非法 skill → exit code 1"""
    result = runner.invoke(cli, ["lint", str(invalid_skill)])
    assert result.exit_code == 1
    assert "FAILED" in result.output


def test_output_format(runner, invalid_skill):
    """输出包含 errors/warnings"""
    result = runner.invoke(cli, ["lint", str(invalid_skill)])
    assert "Error" in result.output or "Warning" in result.output


def test_json_output(runner, valid_skill):
    """--json 输出 JSON 格式"""
    result = runner.invoke(cli, ["lint", str(valid_skill), "--json"])
    assert result.exit_code == 0
    import json
    data = json.loads(result.output)
    assert "passed" in data
    assert "score" in data


def test_missing_path(runner):
    """路径不存在 → 报错"""
    result = runner.invoke(cli, ["lint", "/nonexistent/path"])
    assert result.exit_code != 0


def test_version(runner):
    """--version 输出版本"""
    result = runner.invoke(cli, ["--version"])
    assert "0.1.0" in result.output
