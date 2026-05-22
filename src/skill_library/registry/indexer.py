"""Skill 注册/注销/查询"""

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

    def _build_entry(self, skill_path: Path, meta: dict[str, Any]) -> dict[str, Any]:
        """从解析结果构建 state.json 中的 skill entry"""
        md = meta.get("metadata", {})
        return {
            "name": meta["name"],
            "path": str(skill_path),
            "version": meta.get("version", "0.0.0"),
            "type": md.get("skill-type", "atomic"),
            "design-pattern": md.get("design-pattern", "tool-wrapper"),
            "category": md.get("category", "technical"),
            "mount-status": "unmounted",
            "quality-status": "unchecked",
            "description": meta.get("description", ""),
            "allowed-tools": meta.get("allowed-tools", []),
        }
