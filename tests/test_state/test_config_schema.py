"""E1-S2: config.json Schema 测试"""

import json
import pytest
from pathlib import Path
from jsonschema import validate, ValidationError

SCHEMA_PATH = Path(__file__).parent.parent.parent / "src" / "skill_library" / "state" / "config.schema.json"


@pytest.fixture
def schema():
    """加载 config.json Schema"""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def valid_config():
    """合法的 config.json 数据"""
    return {
        "library-path": "D:\\WorkPlace\\VibeCoding\\Skill Library",
        "agents": {
            "claude-code-main": {
                "path": "C:\\Users\\Kei\\.claude\\skills",
                "description": "主开发环境"
            }
        }
    }


# ===== 正例测试 =====

def test_config_schema_valid(schema, valid_config):
    """合法 config.json 通过 Schema 校验"""
    validate(instance=valid_config, schema=schema)


def test_config_schema_empty_agents(schema):
    """空 agents 也合法"""
    config = {
        "library-path": "D:\\test",
        "agents": {}
    }
    validate(instance=config, schema=schema)


def test_config_schema_minimal_agent(schema):
    """最小 agent 配置（仅 path）"""
    config = {
        "library-path": "D:\\test",
        "agents": {
            "test-agent": {
                "path": "C:\\test"
            }
        }
    }
    validate(instance=config, schema=schema)


def test_config_schema_multiple_agents(schema):
    """多个 agent 配置"""
    config = {
        "library-path": "D:\\test",
        "agents": {
            "agent-1": {"path": "C:\\agent1"},
            "agent-2": {"path": "C:\\agent2", "description": "测试 agent"}
        }
    }
    validate(instance=config, schema=schema)


# ===== 反例测试 =====

def test_config_schema_missing_library_path(schema, valid_config):
    """缺少 library-path → 校验失败"""
    del valid_config["library-path"]
    with pytest.raises(ValidationError):
        validate(instance=valid_config, schema=schema)


def test_config_schema_missing_agents(schema, valid_config):
    """缺少 agents 段 → 校验失败"""
    del valid_config["agents"]
    with pytest.raises(ValidationError):
        validate(instance=valid_config, schema=schema)


def test_config_schema_missing_agent_path(schema, valid_config):
    """agent 缺少 path → 校验失败"""
    del valid_config["agents"]["claude-code-main"]["path"]
    with pytest.raises(ValidationError):
        validate(instance=valid_config, schema=schema)


def test_config_schema_invalid_agent_id_format(schema):
    """非法 agent-id 格式（大写字母）→ 校验失败"""
    config = {
        "library-path": "D:\\test",
        "agents": {
            "Invalid-Agent": {"path": "C:\\test"}
        }
    }
    with pytest.raises(ValidationError):
        validate(instance=config, schema=schema)


def test_config_schema_additional_property(schema, valid_config):
    """不允许额外属性"""
    valid_config["extra"] = "value"
    with pytest.raises(ValidationError):
        validate(instance=valid_config, schema=schema)


def test_config_schema_agent_additional_property(schema, valid_config):
    """agent 不允许额外属性"""
    valid_config["agents"]["claude-code-main"]["extra"] = "value"
    with pytest.raises(ValidationError):
        validate(instance=valid_config, schema=schema)
