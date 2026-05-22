"""E1-S1: state.json Schema 测试"""

import json
import pytest
from pathlib import Path
from jsonschema import validate, ValidationError

SCHEMA_PATH = Path(__file__).parent.parent.parent / "src" / "skill_library" / "state" / "state.schema.json"


@pytest.fixture
def schema():
    """加载 state.json Schema"""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def valid_state():
    """合法的 state.json 数据"""
    return {
        "library": {
            "path": "D:\\WorkPlace\\VibeCoding\\Skill Library",
            "created-at": "2026-05-22",
            "last-sync": "2026-05-22T10:00:00Z"
        },
        "agents": {
            "claude-code-main": {
                "path": "C:\\Users\\Kei\\.claude\\skills",
                "agent-type": "claude-code",
                "skill-packs": ["development", "retrieval"],
                "skills": {
                    "skill-manager": {
                        "status": "mounted",
                        "version": "1.0.0",
                        "adapter": "claude-code",
                        "load-mode": "session",
                        "loaded-at": "2026-05-22",
                        "last-used": "2026-05-22"
                    }
                }
            }
        },
        "skills": {
            "skill-manager": {
                "pack": "meta",
                "type": "atomic",
                "design-pattern": "tool-wrapper",
                "skill-type": "technical",
                "version": "1.0.0",
                "quality-status": "passed",
                "agent-adapters": ["claude-code"],
                "default-adapter": "generic",
                "mounted-to": ["claude-code-main"]
            }
        }
    }


# ===== 正例测试 =====

def test_state_schema_valid(schema, valid_state):
    """合法 state.json 通过 Schema 校验"""
    validate(instance=valid_state, schema=schema)


def test_state_schema_empty_agents_and_skills(schema):
    """空 agents 和 skills 也合法"""
    state = {
        "library": {
            "path": "D:\\test",
            "created-at": "2026-05-22",
            "last-sync": "2026-05-22T10:00:00Z"
        },
        "agents": {},
        "skills": {}
    }
    validate(instance=state, schema=schema)


def test_state_schema_minimal_agent(schema):
    """最小 agent 配置"""
    state = {
        "library": {
            "path": "D:\\test",
            "created-at": "2026-05-22",
            "last-sync": "2026-05-22T10:00:00Z"
        },
        "agents": {
            "test-agent": {
                "path": "C:\\test",
                "agent-type": "generic",
                "skill-packs": [],
                "skills": {}
            }
        },
        "skills": {}
    }
    validate(instance=state, schema=schema)


def test_state_schema_minimal_skill(schema):
    """最小 skill 配置"""
    state = {
        "library": {
            "path": "D:\\test",
            "created-at": "2026-05-22",
            "last-sync": "2026-05-22T10:00:00Z"
        },
        "agents": {},
        "skills": {
            "test-skill": {
                "pack": "meta",
                "type": "atomic",
                "design-pattern": "tool-wrapper",
                "skill-type": "technical",
                "version": "1.0.0",
                "quality-status": "unchecked"
            }
        }
    }
    validate(instance=state, schema=schema)


# ===== 反例测试 =====

def test_state_schema_missing_library(schema, valid_state):
    """缺少 library 段 → 校验失败"""
    del valid_state["library"]
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_missing_agents(schema, valid_state):
    """缺少 agents 段 → 校验失败"""
    del valid_state["agents"]
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_missing_skills(schema, valid_state):
    """缺少 skills 段 → 校验失败"""
    del valid_state["skills"]
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_invalid_mount_status(schema, valid_state):
    """非法 mount status → 校验失败"""
    valid_state["agents"]["claude-code-main"]["skills"]["skill-manager"]["status"] = "invalid"
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_invalid_quality_status(schema, valid_state):
    """非法 quality status → 校验失败"""
    valid_state["skills"]["skill-manager"]["quality-status"] = "invalid"
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_invalid_design_pattern(schema, valid_state):
    """非法 design pattern → 校验失败"""
    valid_state["skills"]["skill-manager"]["design-pattern"] = "invalid"
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_invalid_skill_type(schema, valid_state):
    """非法 skill type → 校验失败"""
    valid_state["skills"]["skill-manager"]["type"] = "invalid"
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_invalid_load_mode(schema, valid_state):
    """非法 load mode → 校验失败"""
    valid_state["agents"]["claude-code-main"]["skills"]["skill-manager"]["load-mode"] = "invalid"
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_invalid_agent_type(schema, valid_state):
    """非法 agent type → 校验失败"""
    valid_state["agents"]["claude-code-main"]["agent-type"] = "invalid"
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_invalid_version_format(schema, valid_state):
    """非法版本号格式 → 校验失败"""
    valid_state["skills"]["skill-manager"]["version"] = "1.0"
    with pytest.raises(ValidationError):
        validate(instance=valid_state, schema=schema)


def test_state_schema_invalid_agent_id_format(schema):
    """非法 agent-id 格式（大写字母）→ 校验失败"""
    state = {
        "library": {
            "path": "D:\\test",
            "created-at": "2026-05-22",
            "last-sync": "2026-05-22T10:00:00Z"
        },
        "agents": {
            "Invalid-Agent": {
                "path": "C:\\test",
                "agent-type": "generic",
                "skill-packs": [],
                "skills": {}
            }
        },
        "skills": {}
    }
    with pytest.raises(ValidationError):
        validate(instance=state, schema=schema)


def test_state_schema_invalid_skill_name_format(schema):
    """非法 skill-name 格式（大写字母）→ 校验失败"""
    state = {
        "library": {
            "path": "D:\\test",
            "created-at": "2026-05-22",
            "last-sync": "2026-05-22T10:00:00Z"
        },
        "agents": {},
        "skills": {
            "Invalid-Skill": {
                "pack": "meta",
                "type": "atomic",
                "design-pattern": "tool-wrapper",
                "skill-type": "technical",
                "version": "1.0.0",
                "quality-status": "unchecked"
            }
        }
    }
    with pytest.raises(ValidationError):
        validate(instance=state, schema=schema)


# ===== 边界测试 =====

def test_state_schema_all_mount_statuses(schema, valid_state):
    """所有合法 mount status 值"""
    for status in ["mounted", "unmounted", "error", "outdated"]:
        valid_state["agents"]["claude-code-main"]["skills"]["skill-manager"]["status"] = status
        validate(instance=valid_state, schema=schema)


def test_state_schema_all_quality_statuses(schema, valid_state):
    """所有合法 quality status 值"""
    for status in ["passed", "failed", "unchecked"]:
        valid_state["skills"]["skill-manager"]["quality-status"] = status
        validate(instance=valid_state, schema=schema)


def test_state_schema_all_design_patterns(schema, valid_state):
    """所有合法 design pattern 值"""
    for pattern in ["tool-wrapper", "generator", "reviewer", "inversion", "pipeline"]:
        valid_state["skills"]["skill-manager"]["design-pattern"] = pattern
        validate(instance=valid_state, schema=schema)


def test_state_schema_all_skill_types(schema, valid_state):
    """所有合法 skill type 值"""
    for skill_type in ["atomic", "workflow"]:
        valid_state["skills"]["skill-manager"]["type"] = skill_type
        validate(instance=valid_state, schema=schema)


def test_state_schema_all_skill_categories(schema, valid_state):
    """所有合法 skill category 值"""
    for category in ["discipline", "technical", "mindset", "reference"]:
        valid_state["skills"]["skill-manager"]["skill-type"] = category
        validate(instance=valid_state, schema=schema)


def test_state_schema_all_load_modes(schema, valid_state):
    """所有合法 load mode 值"""
    for mode in ["once", "turn", "session"]:
        valid_state["agents"]["claude-code-main"]["skills"]["skill-manager"]["load-mode"] = mode
        validate(instance=valid_state, schema=schema)


def test_state_schema_all_agent_types(schema, valid_state):
    """所有合法 agent type 值"""
    for agent_type in ["generic", "claude-code", "hermes", "openclaw"]:
        valid_state["agents"]["claude-code-main"]["agent-type"] = agent_type
        validate(instance=valid_state, schema=schema)
