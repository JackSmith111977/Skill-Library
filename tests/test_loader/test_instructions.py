"""E8-S2: L2 指令加载器测试"""

from skill_library.loader.instructions import load_body


class TestLoadBody:
    def test_load_body(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\n---\nBody content here.")
        result = load_body(skill)
        assert "Body content" in result

    def test_load_body_no_frontmatter(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("Just body.")
        result = load_body(skill)
        assert result == "Just body."

    def test_load_empty_body(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\n---")
        result = load_body(skill)
        assert result == ""

    def test_no_skill_md(self, tmp_path):
        result = load_body(tmp_path / "nonexistent")
        assert result == ""
