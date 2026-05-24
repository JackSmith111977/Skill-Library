"""E1-S4: config.json 读写函数测试"""

import json
import pytest
from pathlib import Path

from skill_library.state.config import ConfigManager


@pytest.fixture
def tmp_config(tmp_path):
    """临时 config.json 路径"""
    return tmp_path / "config.json"


@pytest.fixture
def manager(tmp_config):
    """ConfigManager 实例"""
    return ConfigManager(tmp_config)


def _abs_config(base):
    """用 tmp_path 生成平台无关绝对路径的配置"""
    return {
        "library-path": str(base / "lib"),
        "agents": {
            "claude-code-main": {
                "path": str(base / "claude" / "skills"),
                "description": "主开发环境"
            }
        }
    }


# ===== load 测试 =====

def test_load_valid(manager, tmp_config, tmp_path):
    """加载合法 config.json"""
    config = _abs_config(tmp_path)
    tmp_config.write_text(json.dumps(config), encoding="utf-8")
    result = manager.load()
    assert result == config


def test_load_missing(manager):
    """文件不存在 → 抛出异常"""
    with pytest.raises(FileNotFoundError):
        manager.load()


def test_load_invalid_json(manager, tmp_config):
    """JSON 格式错误 → 抛出异常"""
    tmp_config.write_text("invalid json", encoding="utf-8")
    with pytest.raises(ValueError, match="格式错误"):
        manager.load()


# ===== save 测试 =====

def test_save_creates_file(manager, tmp_path):
    """save 创建文件"""
    config = _abs_config(tmp_path)
    assert not manager.path.exists()
    manager.save(config)
    assert manager.path.exists()


def test_save_content_correct(manager, tmp_path):
    """save 内容正确"""
    config = _abs_config(tmp_path)
    manager.save(config)
    with open(manager.path, "r", encoding="utf-8") as f:
        result = json.load(f)
    assert result == config


def test_save_creates_parent_dirs(tmp_path):
    """save 自动创建父目录"""
    nested_path = tmp_path / "a" / "b" / "config.json"
    manager = ConfigManager(nested_path)
    config = _abs_config(tmp_path)
    manager.save(config)
    assert nested_path.exists()


def test_save_invalid_library_path(manager):
    """library-path 不是绝对路径 → 抛出异常"""
    config = {
        "library-path": "relative/path",
        "agents": {}
    }
    with pytest.raises(ValueError, match="路径校验失败"):
        manager.save(config)


def test_save_invalid_agent_path(manager, tmp_path):
    """agent path 不是绝对路径 → 抛出异常"""
    config = {
        "library-path": str(tmp_path / "lib"),
        "agents": {
            "test-agent": {"path": "relative/path"}
        }
    }
    with pytest.raises(ValueError, match="路径校验失败"):
        manager.save(config)


def test_save_missing_library_path(manager):
    """缺少 library-path → 抛出异常"""
    config = {"agents": {}}
    with pytest.raises(ValueError, match="路径校验失败"):
        manager.save(config)


# ===== validate_paths 测试 =====

def test_validate_absolute_paths(manager, tmp_path):
    """绝对路径 → 校验通过"""
    config = _abs_config(tmp_path)
    errors = manager.validate_paths(config)
    assert errors == []


def test_validate_relative_library_path(manager):
    """相对 library-path → 校验失败"""
    config = {"library-path": "relative", "agents": {}}
    errors = manager.validate_paths(config)
    assert len(errors) == 1
    assert "绝对路径" in errors[0]


def test_validate_relative_agent_path(manager, tmp_path):
    """相对 agent path → 校验失败"""
    config = {
        "library-path": str(tmp_path / "lib"),
        "agents": {"test-agent": {"path": "relative"}}
    }
    errors = manager.validate_paths(config)
    assert len(errors) == 1
    assert "绝对路径" in errors[0]


def test_validate_missing_library_path(manager):
    """缺少 library-path → 校验失败"""
    config = {"agents": {}}
    errors = manager.validate_paths(config)
    assert len(errors) == 1
    assert "缺少" in errors[0]


def test_validate_missing_agent_path(manager, tmp_path):
    """agent 缺少 path → 校验失败"""
    config = {
        "library-path": str(tmp_path / "lib"),
        "agents": {"test-agent": {"description": "test"}}
    }
    errors = manager.validate_paths(config)
    assert len(errors) == 1
    assert "缺少" in errors[0]


def test_validate_multiple_errors(manager):
    """多个错误"""
    config = {
        "library-path": "relative",
        "agents": {
            "agent-1": {"path": "relative1"},
            "agent-2": {"path": "relative2"}
        }
    }
    errors = manager.validate_paths(config)
    assert len(errors) == 3


# ===== 集成测试 =====

def test_load_save_roundtrip(manager, tmp_path):
    """load → save → load 往返测试"""
    config = _abs_config(tmp_path)
    manager.save(config)
    loaded = manager.load()
    assert loaded == config
