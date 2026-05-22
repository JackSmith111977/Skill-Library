"""E3-S3~S6: 注册/注销/查询/分类测试"""

import pytest
from pathlib import Path

from skill_library.state.manager import StateManager
from skill_library.registry.indexer import SkillIndexer


@pytest.fixture
def state_path(tmp_path):
    return tmp_path / "state.json"


@pytest.fixture
def indexer(state_path):
    sm = StateManager(state_path)
    return SkillIndexer(sm)


def _make_skill(tmp_path, name, description="Test skill", version="1.0.0", metadata=None):
    """创建测试 skill 目录"""
    skill_path = tmp_path / name
    skill_path.mkdir(exist_ok=True)
    fm_lines = [
        "---",
        f"name: {name}",
        f"description: {description}",
        f"version: {version}",
    ]
    if metadata:
        fm_lines.append("metadata:")
        for k, v in metadata.items():
            fm_lines.append(f"  {k}: {v}")
    fm_lines.append("---")
    fm_lines.append("Body content.")
    (skill_path / "SKILL.md").write_text("\n".join(fm_lines), encoding="utf-8")
    return skill_path


# ===== E3-S3: 注册 =====

class TestRegister:
    def test_register_new_skill(self, indexer, tmp_path):
        """新 skill 注册成功"""
        skill_path = _make_skill(tmp_path, "my-skill")
        entry = indexer.register(skill_path)
        assert entry["name"] == "my-skill"
        assert entry["version"] == "1.0.0"

    def test_register_update_existing(self, indexer, tmp_path):
        """重复注册更新"""
        skill_path = _make_skill(tmp_path, "my-skill", version="1.0.0")
        indexer.register(skill_path)
        # 更新版本
        _make_skill(tmp_path, "my-skill", version="2.0.0")
        entry = indexer.register(skill_path)
        assert entry["version"] == "2.0.0"

    def test_register_writes_state(self, indexer, tmp_path, state_path):
        """写入 state.json"""
        skill_path = _make_skill(tmp_path, "my-skill")
        indexer.register(skill_path)
        sm = StateManager(state_path)
        state = sm.load()
        assert "my-skill" in state["skills"]

    def test_register_schema_valid(self, indexer, tmp_path):
        """entry 包含所有必要字段"""
        skill_path = _make_skill(tmp_path, "my-skill", metadata={
            "skill-type": "atomic",
            "design-pattern": "tool-wrapper",
            "category": "technical",
        })
        entry = indexer.register(skill_path)
        assert "name" in entry
        assert "path" in entry
        assert "version" in entry
        assert "type" in entry
        assert "design-pattern" in entry
        assert "category" in entry
        assert "mount-status" in entry
        assert "quality-status" in entry

    def test_register_empty_name_raises(self, indexer, tmp_path):
        """name 为空时抛出异常"""
        skill_path = tmp_path / "no-name"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("---\ndescription: test\n---\n", encoding="utf-8")
        with pytest.raises(ValueError, match="name 为空"):
            indexer.register(skill_path)


# ===== E3-S4: 注销 =====

class TestUnregister:
    def test_unregister_existing(self, indexer, tmp_path):
        """注销成功"""
        skill_path = _make_skill(tmp_path, "my-skill")
        indexer.register(skill_path)
        assert indexer.unregister("my-skill") is True
        assert indexer.query("my-skill") is None

    def test_unregister_not_found(self, indexer):
        """不存在时抛出异常"""
        with pytest.raises(KeyError, match="未注册"):
            indexer.unregister("nonexistent")

    def test_unregister_writes_state(self, indexer, tmp_path, state_path):
        """state.json 更新"""
        skill_path = _make_skill(tmp_path, "my-skill")
        indexer.register(skill_path)
        indexer.unregister("my-skill")
        sm = StateManager(state_path)
        state = sm.load()
        assert "my-skill" not in state.get("skills", {})


# ===== E3-S5: 查询 =====

class TestQuery:
    def test_query_by_name(self, indexer, tmp_path):
        """按名称查询"""
        skill_path = _make_skill(tmp_path, "my-skill")
        indexer.register(skill_path)
        result = indexer.query("my-skill")
        assert result is not None
        assert result["name"] == "my-skill"

    def test_query_not_found(self, indexer):
        """不存在返回 None"""
        assert indexer.query("nonexistent") is None

    def test_query_list_all(self, indexer, tmp_path):
        """列出全部"""
        _make_skill(tmp_path, "skill-a")
        _make_skill(tmp_path, "skill-b")
        indexer.register(tmp_path / "skill-a")
        indexer.register(tmp_path / "skill-b")
        all_skills = indexer.list_all()
        assert len(all_skills) == 2

    def test_query_by_category(self, indexer, tmp_path):
        """按分类过滤"""
        _make_skill(tmp_path, "tech-skill", metadata={"category": "technical"})
        _make_skill(tmp_path, "disc-skill", metadata={"category": "discipline"})
        indexer.register(tmp_path / "tech-skill")
        indexer.register(tmp_path / "disc-skill")
        result = indexer.query_by_category("technical")
        assert len(result) == 1
        assert "tech-skill" in result

    def test_query_by_type(self, indexer, tmp_path):
        """按类型过滤"""
        _make_skill(tmp_path, "atomic-skill", metadata={"skill-type": "atomic"})
        _make_skill(tmp_path, "workflow-skill", metadata={"skill-type": "workflow"})
        indexer.register(tmp_path / "atomic-skill")
        indexer.register(tmp_path / "workflow-skill")
        result = indexer.query_by_type("atomic")
        assert len(result) == 1

    def test_query_by_design_pattern(self, indexer, tmp_path):
        """按设计模式过滤"""
        _make_skill(tmp_path, "tool-skill", metadata={"design-pattern": "tool-wrapper"})
        _make_skill(tmp_path, "pipeline-skill", metadata={"design-pattern": "pipeline"})
        indexer.register(tmp_path / "tool-skill")
        indexer.register(tmp_path / "pipeline-skill")
        result = indexer.query_by_design_pattern("pipeline")
        assert len(result) == 1


# ===== E3-S6: 分类标记 =====

class TestClassification:
    def test_extract_classification(self, indexer, tmp_path):
        """从 metadata 提取分类"""
        skill_path = _make_skill(tmp_path, "my-skill", metadata={
            "skill-type": "workflow",
            "design-pattern": "pipeline",
            "category": "discipline",
        })
        entry = indexer.register(skill_path)
        assert entry["type"] == "workflow"
        assert entry["design-pattern"] == "pipeline"
        assert entry["category"] == "discipline"

    def test_default_classification(self, indexer, tmp_path):
        """缺失时用默认值"""
        skill_path = _make_skill(tmp_path, "my-skill")
        entry = indexer.register(skill_path)
        assert entry["type"] == "atomic"
        assert entry["design-pattern"] == "tool-wrapper"
        assert entry["category"] == "technical"

    def test_scan_and_register(self, indexer, tmp_path):
        """扫描并批量注册"""
        _make_skill(tmp_path, "skill-a")
        _make_skill(tmp_path, "skill-b")
        results = indexer.scan_and_register(tmp_path)
        assert len(results) == 2
        all_skills = indexer.list_all()
        assert len(all_skills) == 2
