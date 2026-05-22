"""E8-S5: 加载生命周期测试"""

import pytest
from skill_library.loader.lifecycle import LoadManager, LoadLevel


class TestLoadLifecycle:
    def test_initial_l1(self, tmp_path):
        """初始为 L1"""
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\ndescription: test skill\nversion: 1.0.0\n---\nBody")
        mgr = LoadManager()
        result = mgr.load("test", skill)
        assert result["level"] == "L1"
        assert "body" not in result

    def test_trigger_l2(self, tmp_path):
        """加载 L2"""
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\nBody content")
        mgr = LoadManager()
        result = mgr.load("test", skill, "L2")
        assert result["level"] == "L2"
        assert result["body"] == "Body content"

    def test_trigger_l3(self, tmp_path):
        """加载 L3"""
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\nBody")
        (skill / "references").mkdir()
        (skill / "references" / "doc.md").write_text("ref")
        mgr = LoadManager()
        result = mgr.load("test", skill, "L3")
        assert result["level"] == "L3"
        assert "resources" in result

    def test_upgrade(self, tmp_path):
        """从 L1 升级到 L2"""
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\nBody")
        mgr = LoadManager()
        mgr.load("test", skill, "L1")
        result = mgr.upgrade("test", skill, "L2")
        assert result["level"] == "L2"
        assert "body" in result

    def test_downgrade(self, tmp_path):
        """L2 降级回 L1"""
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\nBody")
        mgr = LoadManager()
        mgr.load("test", skill, "L2")
        result = mgr.downgrade("test", "L1")
        assert result["level"] == "L1"
        assert "body" not in result

    def test_loaded_list(self, tmp_path):
        """列出已加载 skill"""
        skill = tmp_path / "test"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\n---\n")
        mgr = LoadManager()
        mgr.load("test", skill)
        assert "test" in mgr.loaded()

    def test_clear(self, tmp_path):
        """清空缓存"""
        skill = tmp_path / "test"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\n---\n")
        mgr = LoadManager()
        mgr.load("test", skill)
        mgr.clear()
        assert mgr.loaded() == []

    def test_get_nonexistent(self):
        mgr = LoadManager()
        assert mgr.get("nonexistent") is None
