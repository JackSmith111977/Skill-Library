"""状态机引擎：驱动所有管理操作"""

from pathlib import Path
from typing import Any

from .manager import StateManager
from .enums import MountStatus, QualityStatus, SkillType, DesignPattern, SkillCategory


class PreconditionError(Exception):
    """前置条件不满足"""
    pass


class InvalidTransitionError(Exception):
    """非法状态转换"""
    pass


# mount-status 合法转换表
MOUNT_TRANSITIONS: dict[str, list[str]] = {
    "unmounted": ["mounted"],
    "mounted": ["unmounted", "outdated"],
    "outdated": ["mounted"],
}

# quality-status 合法转换表
QUALITY_TRANSITIONS: dict[str, list[str]] = {
    "unchecked": ["passed", "failed"],
    "failed": ["passed"],
    "passed": ["failed"],
}


class StateMachine:
    """状态机引擎，管理 skill 状态转换"""

    def __init__(self, state_manager: StateManager):
        self._sm = state_manager

    def transition_mount(self, skill_name: str, new_status: str) -> dict[str, Any]:
        """执行 mount-status 状态转换。

        合法转换：
        - unmounted → mounted
        - mounted → unmounted
        - mounted → outdated
        - outdated → mounted
        """
        MountStatus(new_status)  # 校验枚举值
        state = self._sm.load()
        skill = self._get_skill(state, skill_name)
        current = skill.get("mount-status", "unmounted")

        if new_status not in MOUNT_TRANSITIONS.get(current, []):
            raise InvalidTransitionError(
                f"非法 mount 状态转换: {current} → {new_status}"
            )

        skill["mount-status"] = new_status
        self._sm.save(state)
        return skill

    def transition_quality(self, skill_name: str, new_status: str) -> dict[str, Any]:
        """执行 quality-status 状态转换。

        合法转换：
        - unchecked → passed / failed
        - failed → passed
        - passed → failed
        """
        QualityStatus(new_status)  # 校验枚举值
        state = self._sm.load()
        skill = self._get_skill(state, skill_name)
        current = skill.get("quality-status", "unchecked")

        if new_status not in QUALITY_TRANSITIONS.get(current, []):
            raise InvalidTransitionError(
                f"非法 quality 状态转换: {current} → {new_status}"
            )

        skill["quality-status"] = new_status
        self._sm.save(state)
        return skill

    def mount(self, skill_name: str, agent_id: str) -> dict[str, Any]:
        """mount skill 到 agent。

        前置条件：quality-status == passed
        """
        state = self._sm.load()
        skill = self._get_skill(state, skill_name)

        # 前置检查
        if skill.get("quality-status") != "passed":
            raise PreconditionError(
                f"mount 前置条件不满足: quality-status={skill.get('quality-status')}, 需要 passed"
            )

        current_mount = skill.get("mount-status", "unmounted")
        if current_mount not in ("unmounted", "outdated"):
            raise PreconditionError(
                f"mount 前置条件不满足: mount-status={current_mount}"
            )

        skill["mount-status"] = "mounted"
        if "mounted-to" not in skill:
            skill["mounted-to"] = []
        if agent_id not in skill["mounted-to"]:
            skill["mounted-to"].append(agent_id)

        self._sm.save(state)
        return skill

    def unmount(self, skill_name: str, agent_id: str | None = None) -> dict[str, Any]:
        """unmount skill。

        前置条件：mount-status == mounted
        """
        state = self._sm.load()
        skill = self._get_skill(state, skill_name)

        if skill.get("mount-status") != "mounted":
            raise PreconditionError(
                f"unmount 前置条件不满足: mount-status={skill.get('mount-status')}"
            )

        skill["mount-status"] = "unmounted"
        if agent_id and "mounted-to" in skill:
            if agent_id in skill["mounted-to"]:
                skill["mounted-to"].remove(agent_id)

        self._sm.save(state)
        return skill

    def classify(self, skill_name: str, **kwargs) -> dict[str, Any]:
        """更新 skill 分类标签。

        支持字段：design-pattern, category, type
        """
        # 校验枚举值
        if "design-pattern" in kwargs:
            DesignPattern(kwargs["design-pattern"])
        if "category" in kwargs:
            SkillCategory(kwargs["category"])
        if "type" in kwargs:
            SkillType(kwargs["type"])

        state = self._sm.load()
        skill = self._get_skill(state, skill_name)

        for key in ("design-pattern", "category", "type"):
            if key in kwargs:
                skill[key] = kwargs[key]

        self._sm.save(state)
        return skill

    def status(self, skill_name: str) -> dict[str, Any] | None:
        """查询 skill 状态。"""
        state = self._sm.load()
        return state.get("skills", {}).get(skill_name)

    def init_library(self, library_path: str | Path, config_path: str | Path | None = None) -> dict[str, Any]:
        """初始化 skill library 环境。

        创建 state.json、config.json、skills 目录。已存在不覆盖。
        """
        library_path = Path(library_path)
        library_path.mkdir(parents=True, exist_ok=True)
        (library_path / "skills").mkdir(exist_ok=True)

        # state.json
        state = self._sm.load()
        if not state.get("library"):
            state["library"] = {
                "path": str(library_path),
                "created-at": "2026-05-22",
                "last-sync": "2026-05-22",
            }
            state.setdefault("agents", {})
            state.setdefault("skills", {})
            self._sm.save(state)

        # config.json
        if config_path:
            config_path = Path(config_path)
            if not config_path.exists():
                from .config import ConfigManager
                cm = ConfigManager(config_path)
                config = {
                    "library-path": str(library_path),
                    "agents": {},
                }
                cm.save(config)

        return state

    def _get_skill(self, state: dict, skill_name: str) -> dict[str, Any]:
        """获取 skill entry，不存在时抛出 KeyError"""
        skills = state.get("skills", {})
        if skill_name not in skills:
            raise KeyError(f"skill 未注册: {skill_name}")
        return skills[skill_name]
