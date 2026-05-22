"""E5: 工作流 lint 规则测试"""

import pytest
from pathlib import Path

from skill_library.quality.rules.workflow_refs import check_workflow_refs
from skill_library.quality.rules.workflow_steps import check_steps_complete
from skill_library.quality.rules.workflow_gates import check_gate_markers
from skill_library.quality.rules.workflow_deps import check_step_deps
from skill_library.quality.lint import QualityEngine


# ===== E5-S1: 引用存在性 =====

class TestWorkflowRefs:
    def test_ref_exists(self, tmp_path):
        """引用存在 → 通过"""
        skills_root = tmp_path / "skills"
        skills_root.mkdir()
        (skills_root / "my-atomic").mkdir()
        (skills_root / "my-atomic" / "SKILL.md").write_text("---\nname: my-atomic\n---\n")
        workflow_path = skills_root / "my-workflow"
        workflow_path.mkdir()
        body = 'Step 1: @my-atomic do something'
        errors = check_workflow_refs(workflow_path, body, skills_root)
        assert errors == []

    def test_ref_missing(self, tmp_path):
        """引用不存在 → ERROR"""
        skills_root = tmp_path / "skills"
        skills_root.mkdir()
        workflow_path = skills_root / "my-workflow"
        workflow_path.mkdir()
        body = 'Step 1: @nonexistent-skill do something'
        errors = check_workflow_refs(workflow_path, body, skills_root)
        assert len(errors) == 1
        assert "不存在" in errors[0].message

    def test_no_refs(self, tmp_path):
        """无引用 → 通过"""
        skills_root = tmp_path / "skills"
        skills_root.mkdir()
        workflow_path = skills_root / "my-workflow"
        workflow_path.mkdir()
        body = 'Step 1: do something without refs'
        errors = check_workflow_refs(workflow_path, body, skills_root)
        assert errors == []


# ===== E5-S2: 步骤完整性 =====

class TestStepsComplete:
    def test_steps_continuous(self):
        """序号连续 → 通过"""
        body = "Step 1: first\nStep 2: second\nStep 3: third"
        errors = check_steps_complete(body)
        assert errors == []

    def test_steps_gap(self):
        """序号有间隔 → ERROR"""
        body = "Step 1: first\nStep 3: third"
        errors = check_steps_complete(body)
        assert len(errors) == 1
        assert "不连续" in errors[0].message

    def test_steps_not_start_from_1(self):
        """不从 1 开始 → ERROR"""
        body = "Step 2: second\nStep 3: third"
        errors = check_steps_complete(body)
        assert any("从 1 开始" in e.message for e in errors)

    def test_no_steps(self):
        """无步骤 → 通过"""
        body = "No steps here"
        errors = check_steps_complete(body)
        assert errors == []


# ===== E5-S3: 门控标记 =====

class TestGateMarkers:
    def test_has_gate_marker(self):
        """有门控 → 通过"""
        body = "Inversion mode with STAGE_GATE checkpoint"
        warnings = check_gate_markers(body, "inversion")
        assert warnings == []

    def test_no_gate_marker(self):
        """无门控 → WARNING"""
        body = "This workflow uses inversion pattern for user confirmation"
        warnings = check_gate_markers(body, "inversion")
        assert len(warnings) == 1
        assert "门控" in warnings[0].message

    def test_not_inversion(self):
        """非 Inversion → 跳过"""
        body = "Some inversion mention but not the pattern"
        warnings = check_gate_markers(body, "pipeline")
        assert warnings == []


# ===== E5-S4: 依赖关系 =====

class TestStepDeps:
    def test_no_cycle(self):
        """无循环 → 通过"""
        body = "Step 1: start\nStep 2 depends on Step 1\nStep 3 depends on Step 2"
        errors = check_step_deps(body)
        assert errors == []

    def test_cycle_detected(self):
        """有循环 → ERROR"""
        body = "Step 1 depends on Step 3\nStep 2 depends on Step 1\nStep 3 depends on Step 2"
        errors = check_step_deps(body)
        assert len(errors) == 1
        assert "循环" in errors[0].message

    def test_no_deps(self):
        """无依赖 → 通过"""
        body = "Step 1: start\nStep 2: end"
        errors = check_step_deps(body)
        assert errors == []


# ===== E5-S5: 工作流 lint 入口 =====

class TestWorkflowLint:
    def test_workflow_lint_valid(self, tmp_path):
        """合法工作流 → 通过"""
        skill_path = tmp_path / "my-workflow"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text(
            """---
name: my-workflow
description: This skill should be used when user asks to "test workflow".
version: 1.0.0
metadata:
  design-pattern: pipeline
---

# Workflow

Step 1: First step
Step 2: Second step
""",
            encoding="utf-8",
        )
        engine = QualityEngine()
        result = engine.lint_workflow(skill_path)
        assert result.passed is True

    def test_workflow_lint_invalid(self, tmp_path):
        """非法工作流 → 失败"""
        skill_path = tmp_path / "my-workflow"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text(
            """---
name: Invalid-Workflow
description: Helps
---

Step 1: First
Step 3: Gap
""",
            encoding="utf-8",
        )
        engine = QualityEngine()
        result = engine.lint_workflow(skill_path)
        assert result.passed is False
