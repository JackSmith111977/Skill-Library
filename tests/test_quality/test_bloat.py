"""E13-S2: Skill 膨胀检测测试"""

from pathlib import Path
from skill_library.quality.rules.bloat import check_bloat


class TestBloatDetection:

    def test_body_not_bloated(self, tmp_path):
        skill = tmp_path / "test"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\n---\n" + "\n".join(f"line {i}" for i in range(10)))
        warnings = check_bloat(skill)
        assert warnings == []

    def test_body_too_many_lines(self, tmp_path):
        skill = tmp_path / "test"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\n---\n" + "\n".join(f"line {i}" for i in range(501)))
        warnings = check_bloat(skill)
        assert any("行" in w.message for w in warnings)

    def test_body_too_many_words(self, tmp_path):
        skill = tmp_path / "test"
        skill.mkdir()
        words = " ".join(f"word{i}" for i in range(5001))
        (skill / "SKILL.md").write_text("---\nname: test\n---\n" + words)
        warnings = check_bloat(skill)
        assert any("词" in w.message for w in warnings)

    def test_too_many_references(self, tmp_path):
        skill = tmp_path / "test"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\n---\nBody")
        ref_dir = skill / "references"
        ref_dir.mkdir()
        for i in range(11):
            (ref_dir / f"ref-{i}.md").write_text(f"ref {i}")
        warnings = check_bloat(skill)
        assert any("references/" in w.message for w in warnings)

    def test_no_skill_md(self, tmp_path):
        warnings = check_bloat(tmp_path / "nonexistent")
        assert warnings == []

    def test_no_references_dir(self, tmp_path):
        skill = tmp_path / "test"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\n---\nBody")
        warnings = check_bloat(skill)
        assert warnings == []
