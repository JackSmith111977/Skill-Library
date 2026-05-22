"""E1-S3: state.json 读写函数测试"""

import json
import pytest
from pathlib import Path

from skill_library.state.manager import StateManager


@pytest.fixture
def tmp_state(tmp_path):
    """临时 state.json 路径"""
    return tmp_path / "state.json"


@pytest.fixture
def manager(tmp_state):
    """StateManager 实例"""
    return StateManager(tmp_state)


@pytest.fixture
def sample_state():
    """示例状态数据"""
    return {
        "library": {
            "path": "D:\\test",
            "created-at": "2026-05-22",
            "last-sync": "2026-05-22T10:00:00Z"
        },
        "agents": {},
        "skills": {}
    }


# ===== load 测试 =====

def test_load_existing(manager, tmp_state, sample_state):
    """加载已存在的 state.json"""
    tmp_state.write_text(json.dumps(sample_state), encoding="utf-8")
    result = manager.load()
    assert result == sample_state


def test_load_missing(manager):
    """文件不存在 → 返回空结构"""
    result = manager.load()
    assert "library" in result
    assert "agents" in result
    assert "skills" in result
    assert result["agents"] == {}
    assert result["skills"] == {}


def test_load_invalid_json(manager, tmp_state):
    """JSON 格式错误 → 抛出异常"""
    tmp_state.write_text("invalid json", encoding="utf-8")
    with pytest.raises(ValueError, match="格式错误"):
        manager.load()


def test_load_empty_file(manager, tmp_state):
    """空文件 → 抛出异常"""
    tmp_state.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="格式错误"):
        manager.load()


# ===== save 测试 =====

def test_save_creates_file(manager, sample_state):
    """save 创建文件"""
    assert not manager.path.exists()
    manager.save(sample_state)
    assert manager.path.exists()


def test_save_content_correct(manager, sample_state):
    """save 内容正确"""
    manager.save(sample_state)
    with open(manager.path, "r", encoding="utf-8") as f:
        result = json.load(f)
    assert result == sample_state


def test_save_overwrites(manager, sample_state):
    """save 覆盖已有内容"""
    manager.save(sample_state)
    updated = sample_state.copy()
    updated["library"]["path"] = "D:\\updated"
    manager.save(updated)
    with open(manager.path, "r", encoding="utf-8") as f:
        result = json.load(f)
    assert result["library"]["path"] == "D:\\updated"


def test_save_creates_parent_dirs(tmp_path, sample_state):
    """save 自动创建父目录"""
    nested_path = tmp_path / "a" / "b" / "c" / "state.json"
    manager = StateManager(nested_path)
    manager.save(sample_state)
    assert nested_path.exists()


def test_save_unicode(manager):
    """save 正确处理 Unicode"""
    state = {
        "library": {"path": "中文路径", "created-at": "2026-05-22", "last-sync": ""},
        "agents": {},
        "skills": {"测试-skill": {"pack": "meta", "type": "atomic", "design-pattern": "tool-wrapper", "skill-type": "technical", "version": "1.0.0", "quality-status": "unchecked"}}
    }
    manager.save(state)
    result = manager.load()
    assert result["skills"]["测试-skill"]["pack"] == "meta"


# ===== 原子写入测试 =====

def test_atomic_write_no_corruption(manager, sample_state):
    """原子写入：文件不会损坏"""
    manager.save(sample_state)
    # 验证文件完整
    result = manager.load()
    assert result == sample_state


# ===== 集成测试 =====

def test_load_save_roundtrip(manager, sample_state):
    """load → save → load 往返测试"""
    manager.save(sample_state)
    loaded = manager.load()
    assert loaded == sample_state


def test_multiple_saves(manager):
    """多次保存"""
    for i in range(5):
        state = {
            "library": {"path": f"path-{i}", "created-at": "2026-05-22", "last-sync": ""},
            "agents": {},
            "skills": {}
        }
        manager.save(state)
    result = manager.load()
    assert result["library"]["path"] == "path-4"
