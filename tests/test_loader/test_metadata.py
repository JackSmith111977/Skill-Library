"""E8-S1: L1 元数据加载器测试"""

from pathlib import Path

from skill_library.loader.metadata import load_metadata


class TestLoadMetadata:
    def test_load_metadata(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test skill\nversion: 1.0.0\n---\nBody"
        )
        result = load_metadata(skill)
        assert result["name"] == "test-skill"
        assert result["description"] == "A test skill"
        assert result["version"] == "1.0.0"
        # body 不加载
        assert "body" not in result

    def test_load_metadata_no_version(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\nBody")
        result = load_metadata(skill)
        assert result["version"] == "0.0.0"

    def test_load_metadata_no_skill(self, tmp_path):
        result = load_metadata(tmp_path / "nonexistent")
        assert result["name"] == ""
