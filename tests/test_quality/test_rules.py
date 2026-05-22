"""E2-S1~S6: lint 规则测试"""

import pytest
from pathlib import Path

from skill_library.quality.rules.name_format import check_name_format
from skill_library.quality.rules.description import check_description
from skill_library.quality.rules.body_length import check_body_length, estimate_tokens
from skill_library.quality.rules.references import check_references
from skill_library.quality.rules.allowed_tools import check_allowed_tools
from skill_library.quality.rules.metadata import check_metadata


# ===== E2-S1: name 格式 =====

class TestNameFormat:
    def test_valid_name(self):
        errors = check_name_format("skill-name", "skill-name")
        assert errors == []

    def test_valid_short(self):
        errors = check_name_format("a", "a")
        assert errors == []

    def test_valid_with_numbers(self):
        errors = check_name_format("skill-123", "skill-123")
        assert errors == []

    def test_empty_name(self):
        errors = check_name_format("", "skill")
        assert len(errors) == 1
        assert "不能为空" in errors[0].message

    def test_uppercase(self):
        errors = check_name_format("Skill-Name", "skill-name")
        assert len(errors) >= 1

    def test_start_hyphen(self):
        errors = check_name_format("-skill", "skill")
        assert any("连字符开头" in e.message for e in errors)

    def test_end_hyphen(self):
        errors = check_name_format("skill-", "skill")
        assert any("连字符结尾" in e.message for e in errors)

    def test_double_hyphen(self):
        errors = check_name_format("skill--name", "skill--name")
        assert any("连续连字符" in e.message for e in errors)

    def test_too_long(self):
        long_name = "a" * 65
        errors = check_name_format(long_name, long_name)
        assert any("超过 64" in e.message for e in errors)

    def test_dir_mismatch(self):
        errors = check_name_format("skill-name", "other-name")
        assert any("不一致" in e.message for e in errors)


# ===== E2-S2: description =====

class TestDescription:
    def test_valid(self):
        desc = 'This skill should be used when user asks to "create a skill" or "add a skill"'
        errors, warnings = check_description(desc)
        assert errors == []
        assert warnings == []

    def test_empty(self):
        errors, warnings = check_description("")
        assert len(errors) == 1
        assert "不能为空" in errors[0].message

    def test_too_long(self):
        desc = "x" * 1025
        errors, warnings = check_description(desc)
        assert any("超过 1024" in e.message for e in errors)

    def test_no_triggers(self):
        desc = "This skill helps with tasks"
        errors, warnings = check_description(desc)
        assert errors == []
        assert any("触发短语" in w.message for w in warnings)

    def test_has_triggers(self):
        desc = 'Use when user asks to "create a skill"'
        errors, warnings = check_description(desc)
        assert not any("触发短语" in w.message for w in warnings)

    def test_third_person(self):
        desc = 'This skill should be used when user asks to "xxx"'
        errors, warnings = check_description(desc)
        assert not any("第三人称" in w.message for w in warnings)

    def test_no_third_person(self):
        desc = 'Use when user asks to "xxx"'
        errors, warnings = check_description(desc)
        assert any("第三人称" in w.message for w in warnings)


# ===== E2-S3: body 长度 =====

class TestBodyLength:
    def test_short_body(self):
        body = "line\n" * 100
        warnings = check_body_length(body)
        assert warnings == []

    def test_long_body(self):
        body = "line\n" * 501
        warnings = check_body_length(body)
        assert any("行数" in w.message for w in warnings)

    def test_empty_body(self):
        warnings = check_body_length("")
        assert warnings == []

    def test_token_estimate(self):
        text = "a" * 1000
        assert estimate_tokens(text) == 250

    def test_long_tokens(self):
        body = "x" * 20001  # 20001/4 = 5000.25 tokens
        warnings = check_body_length(body)
        # 20001 chars / 4 = 5000, just at threshold, need more
        body = "x" * 20005
        warnings = check_body_length(body)
        assert any("token" in w.message for w in warnings)


# ===== E2-S4: 文件引用 =====

class TestReferences:
    def test_valid_ref(self, tmp_path):
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        (skill_path / "doc.md").write_text("content")
        body = "See [doc](doc.md) for details"
        errors = check_references(skill_path, body)
        assert errors == []

    def test_missing_ref(self, tmp_path):
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        body = "See [doc](missing.md) for details"
        errors = check_references(skill_path, body)
        assert len(errors) == 1
        assert "不存在" in errors[0].message

    def test_external_url(self, tmp_path):
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        body = "See [site](https://example.com) for details"
        errors = check_references(skill_path, body)
        assert errors == []

    def test_no_refs(self, tmp_path):
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        body = "No references here"
        errors = check_references(skill_path, body)
        assert errors == []


# ===== E2-S5: allowed-tools =====

class TestAllowedTools:
    def test_valid_string(self):
        errors = check_allowed_tools("Read Bash Write")
        assert errors == []

    def test_valid_list(self):
        errors = check_allowed_tools(["Read", "Bash"])
        assert errors == []

    def test_none(self):
        errors = check_allowed_tools(None)
        assert errors == []

    def test_empty_string(self):
        errors = check_allowed_tools("")
        assert errors == []

    def test_double_space(self):
        errors = check_allowed_tools("Read  Bash")
        assert any("连续空格" in e.message for e in errors)


# ===== E2-S6: metadata =====

class TestMetadata:
    def test_valid(self):
        warnings = check_metadata({"version": "1.0.0", "author": "test"})
        assert warnings == []

    def test_none(self):
        warnings = check_metadata(None)
        assert warnings == []

    def test_invalid_version(self):
        warnings = check_metadata({"version": "1.0"})
        assert any("语义化版本" in w.message for w in warnings)

    def test_valid_version(self):
        warnings = check_metadata({"version": "1.0.0"})
        assert warnings == []

    def test_no_version(self):
        warnings = check_metadata({"author": "test"})
        assert warnings == []
