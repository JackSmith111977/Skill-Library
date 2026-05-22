"""Skill 注册/注销/查询"""

import json
from pathlib import Path
from typing import Any

from ..state.manager import StateManager
from .parser import parse_skill_md
from .scanner import scan_skills


class SkillIndexer:
    """管理 state.json 中 skills 段的注册、注销、查询"""

    def __init__(self, state_manager: StateManager):
        self._sm = state_manager

    def register(self, skill_path: str | Path) -> dict[str, Any]:
        """注册 skill 到 state.json。

        读取 SKILL.md frontmatter → 构建 skill entry → 写入 state。
        重复注册时更新已有条目。
        """
        skill_path = Path(skill_path)
        meta = parse_skill_md(skill_path)
        name = meta["name"]
        if not name:
            raise ValueError(f"skill name 为空: {skill_path}")

        entry = self._build_entry(skill_path, meta)

        state = self._sm.load()
        if "skills" not in state:
            state["skills"] = {}
        state["skills"][name] = entry
        self._sm.save(state)

        return entry

    def unregister(self, name: str) -> bool:
        """从 state.json 注销 skill。不存在时抛出 KeyError。"""
        state = self._sm.load()
        skills = state.get("skills", {})
        if name not in skills:
            raise KeyError(f"skill 未注册: {name}")
        del skills[name]
        self._sm.save(state)
        return True

    def query(self, name: str) -> dict[str, Any] | None:
        """按名称查询单个 skill。不存在返回 None。"""
        state = self._sm.load()
        return state.get("skills", {}).get(name)

    def list_all(self) -> dict[str, dict[str, Any]]:
        """列出所有已注册 skill。"""
        state = self._sm.load()
        return dict(state.get("skills", {}))

    def query_by_category(self, category: str) -> dict[str, dict[str, Any]]:
        """按分类过滤 skill。"""
        state = self._sm.load()
        return {
            name: info
            for name, info in state.get("skills", {}).items()
            if info.get("category") == category
        }

    def query_by_type(self, skill_type: str) -> dict[str, dict[str, Any]]:
        """按类型过滤 skill。"""
        state = self._sm.load()
        return {
            name: info
            for name, info in state.get("skills", {}).items()
            if info.get("type") == skill_type
        }

    def query_by_design_pattern(self, pattern: str) -> dict[str, dict[str, Any]]:
        """按设计模式过滤 skill。"""
        state = self._sm.load()
        return {
            name: info
            for name, info in state.get("skills", {}).items()
            if info.get("design-pattern") == pattern
        }

    def scan_and_register(self, root_dir: str | Path) -> list[dict[str, Any]]:
        """扫描目录并注册所有发现的 skill。"""
        skills = scan_skills(root_dir)
        results = []
        for skill_path in skills:
            entry = self.register(skill_path)
            results.append(entry)
        return results

    def query_by_agent(self, agent_id: str) -> dict[str, dict[str, Any]]:
        """按 agent 过滤技能（返回挂载到此 agent 的 skill）。"""
        state = self._sm.load()
        agent = state.get("agents", {}).get(agent_id)
        if agent is None:
            return {}
        agent_skills = agent.get("skills", {})
        all_skills = state.get("skills", {})
        return {
            name: dict(all_skills[name])
            for name in agent_skills
            if name in all_skills
        }

    def query_by_agent_type(self, agent_type: str) -> dict[str, dict[str, Any]]:
        """按 agent 类型过滤 agent。"""
        state = self._sm.load()
        agents = state.get("agents", {})
        return {
            aid: info
            for aid, info in agents.items()
            if info.get("agent-type") == agent_type
        }

    def _build_entry(self, skill_path: Path, meta: dict[str, Any]) -> dict[str, Any]:
        """从解析结果构建 state.json 中的 skill entry

        从目录结构推断 pack 名（skills/<pack>/<skill>/），
        并读取 pack.json 获取 pack-version。
        """
        md = meta.get("metadata", {})

        # 从路径推断 pack 名
        pack = self._resolve_pack(skill_path)
        pack_version = self._read_pack_version(skill_path, pack)

        return {
            "name": meta["name"],
            "path": str(skill_path),
            "pack": pack,
            "pack-version": pack_version,
            "version": meta.get("version", "0.0.0"),
            "type": md.get("skill-type", "atomic"),
            "design-pattern": md.get("design-pattern", "tool-wrapper"),
            "category": md.get("category", "technical"),
            "mount-status": "unmounted",
            "quality-status": "unchecked",
            "description": meta.get("description", ""),
            "allowed-tools": meta.get("allowed-tools", []),
        }

    @staticmethod
    def _resolve_pack(skill_path: Path) -> str:
        """从路径推断 pack 名：skills/<pack>/<skill>/"""
        parts = skill_path.parts
        try:
            skills_idx = parts.index("skills")
            if len(parts) > skills_idx + 1:
                return parts[skills_idx + 1]
        except ValueError:
            pass
        return "unknown"

    @staticmethod
    def _read_pack_version(skill_path: Path, pack: str) -> str:
        """读取 pack.json 中的版本号"""
        pack_json = skill_path.parent / "pack.json"
        if pack_json.is_file():
            try:
                with open(pack_json, encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("version", "0.0.0")
            except (json.JSONDecodeError, OSError):
                pass
        return "0.0.0"
