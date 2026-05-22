"""E8-S3: L3 资源加载器测试"""

from skill_library.loader.resources import load_references, load_assets, load_all_resources


class TestLoadResources:
    def test_load_references(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        ref_dir = skill / "references"
        ref_dir.mkdir()
        (ref_dir / "doc1.md").write_text("doc1 content")
        (ref_dir / "doc2.md").write_text("doc2 content")
        result = load_references(skill)
        assert len(result) == 2
        assert "doc1.md" in result
        assert result["doc1.md"] == "doc1 content"

    def test_load_assets(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        assets_dir = skill / "assets"
        assets_dir.mkdir()
        (assets_dir / "template.j2").write_text("template")
        result = load_assets(skill)
        assert "template.j2" in result

    def test_no_references(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        assert load_references(skill) == {}

    def test_no_assets(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        assert load_assets(skill) == []

    def test_load_all_resources(self, tmp_path):
        skill = tmp_path / "test-skill"
        skill.mkdir()
        (skill / "references").mkdir()
        (skill / "references" / "doc.md").write_text("ref")
        (skill / "assets").mkdir()
        (skill / "assets" / "template.j2").write_text("tpl")
        result = load_all_resources(skill)
        assert "references" in result
        assert "assets" in result
