"""E3-S1: 目录扫描器测试"""

import pytest
from pathlib import Path

from skill_library.registry.scanner import scan_skills


class TestScanSkills:
    def test_scan_valid_dir(self, tmp_path):
        """找到包含 SKILL.md 的目录"""
        skill = tmp_path / "my-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: my-skill\n---\n")
        results = scan_skills(tmp_path)
        assert len(results) == 1
        assert results[0] == skill

    def test_scan_multiple(self, tmp_path):
        """找到多个 skill"""
        for name in ["skill-a", "skill-b", "skill-c"]:
            d = tmp_path / name
            d.mkdir()
            (d / "SKILL.md").write_text(f"---\nname: {name}\n---\n")
        results = scan_skills(tmp_path)
        assert len(results) == 3

    def test_scan_empty_dir(self, tmp_path):
        """空目录返回空列表"""
        assert scan_skills(tmp_path) == []

    def test_scan_skip_hidden(self, tmp_path):
        """跳过隐藏目录"""
        hidden = tmp_path / ".hidden"
        hidden.mkdir()
        (hidden / "SKILL.md").write_text("---\nname: hidden\n---\n")
        assert scan_skills(tmp_path) == []

    def test_scan_skip_pycache(self, tmp_path):
        """跳过 __pycache__ 目录"""
        cache = tmp_path / "__pycache__"
        cache.mkdir()
        (cache / "SKILL.md").write_text("---\nname: cache\n---\n")
        assert scan_skills(tmp_path) == []

    def test_scan_skip_no_skill_md(self, tmp_path):
        """没有 SKILL.md 的目录不返回"""
        d = tmp_path / "not-a-skill"
        d.mkdir()
        (d / "README.md").write_text("not a skill")
        assert scan_skills(tmp_path) == []

    def test_scan_nonexistent_dir(self):
        """不存在的目录返回空列表"""
        assert scan_skills("/nonexistent/path") == []

    def test_scan_nested_not_recursive(self, tmp_path):
        """只扫描一层，不递归"""
        parent = tmp_path / "parent"
        parent.mkdir()
        child = parent / "child"
        child.mkdir()
        (child / "SKILL.md").write_text("---\nname: child\n---\n")
        # root 下没有直接的 SKILL.md（child 在第二层）
        assert scan_skills(tmp_path) == []
        # parent 下 child 是直接子目录，能找到
        assert len(scan_skills(parent)) == 1

    def test_scan_sorted(self, tmp_path):
        """结果按名称排序"""
        for name in ["z-skill", "a-skill", "m-skill"]:
            d = tmp_path / name
            d.mkdir()
            (d / "SKILL.md").write_text(f"---\nname: {name}\n---\n")
        results = scan_skills(tmp_path)
        assert [r.name for r in results] == ["a-skill", "m-skill", "z-skill"]
