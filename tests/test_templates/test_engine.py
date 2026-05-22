"""E6-S1,S2,S4: 模板测试"""

import pytest
from pathlib import Path

from skill_library.templates.engine import fill_template, create_skill, TEMPLATES
from skill_library.quality.lint import QualityEngine


# ===== E6-S4: 模板参数填充 =====

class TestFillTemplate:
    def test_fill_name(self):
        result = fill_template("Hello {{name}}!", {"name": "World"})
        assert result == "Hello World!"

    def test_fill_all_vars(self):
        result = fill_template("{{a}}-{{b}}", {"a": "x", "b": "y"})
        assert result == "x-y"

    def test_missing_var_keeps_placeholder(self):
        result = fill_template("Hello {{name}}!", {})
        assert result == "Hello {{name}}!"

    def test_no_vars(self):
        result = fill_template("Hello World!", {"name": "test"})
        assert result == "Hello World!"


# ===== E6-S1: 原子模板通过 lint =====

class TestAtomicTemplate:
    def test_atomic_template_passes_lint(self, tmp_path):
        """模板生成的 skill 通过 lint"""
        skill_dir = create_skill(
            name="test-atomic",
            output_dir=str(tmp_path),
            description="test something",
        )
        engine = QualityEngine()
        result = engine.lint_atomic(skill_dir)
        assert result.passed is True, f"Lint errors: {result.errors}"

    def test_template_directory_structure(self, tmp_path):
        """目录结构正确"""
        skill_dir = create_skill(
            name="test-atomic",
            output_dir=str(tmp_path),
            description="test",
        )
        assert (skill_dir / "SKILL.md").exists()
        assert (skill_dir / "references").is_dir()
        assert (skill_dir / "scripts").is_dir()
        assert (skill_dir / "assets").is_dir()


# ===== E6-S2: 工作流模板通过 lint =====

class TestWorkflowTemplate:
    def test_pipeline_template_passes_lint(self, tmp_path):
        """Pipeline 模板通过 lint"""
        skill_dir = create_skill(
            name="test-pipeline",
            output_dir=str(tmp_path),
            skill_type="workflow",
            description="process data",
            design_pattern="pipeline",
            template_vars={"step1": "Load", "step2": "Process"},
        )
        engine = QualityEngine()
        result = engine.lint_workflow(skill_dir)
        assert result.passed is True, f"Lint errors: {result.errors}"

    def test_inversion_template_passes_lint(self, tmp_path):
        """Inversion 模板通过 lint"""
        skill_dir = create_skill(
            name="test-inversion",
            output_dir=str(tmp_path),
            skill_type="workflow",
            description="approve request",
            design_pattern="inversion",
        )
        engine = QualityEngine()
        result = engine.lint_workflow(skill_dir)
        assert result.passed is True, f"Lint errors: {result.errors}"

    def test_invalid_skill_type(self, tmp_path):
        """非法类型抛出异常"""
        with pytest.raises(ValueError):
            create_skill("test", tmp_path, skill_type="invalid")

    def test_invalid_design_pattern(self, tmp_path):
        """非法设计模式抛出异常"""
        with pytest.raises(ValueError):
            create_skill("test", tmp_path, design_pattern="invalid")
