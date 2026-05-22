"""AgentAdapter 抽象基类"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class AgentAdapter(ABC):
    """Agent 适配器抽象基类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """适配器名称"""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """适配器版本"""
        ...

    @property
    def target_patterns(self) -> list[str]:
        """匹配的 agent 名称模式列表。子类可覆盖。"""
        return [self.name]

    @abstractmethod
    def adapt_content(self, content: str, frontmatter: dict[str, Any]) -> str:
        """适配 SKILL.md 内容。子类必须实现。"""
        ...

    def load_skill(self, skill_dir: str | Path) -> str | None:
        """加载适配的 SKILL.md。

        优先加载 agents/<name>/SKILL.md，不存在时加载 SKILL.md。

        返回适配后的完整内容，或 None（无适配）。
        """
        skill_dir = Path(skill_dir)

        # 优先 agent 版本
        agent_skill = skill_dir / "agents" / self.name / "SKILL.md"
        if agent_skill.is_file():
            return agent_skill.read_text(encoding="utf-8")

        # 降级到通用版本
        generic_skill = skill_dir / "SKILL.md"
        if generic_skill.is_file():
            return generic_skill.read_text(encoding="utf-8")

        return None

    def get_effective_content(self, skill_dir: str | Path) -> tuple[str | None, str]:
        """获取有效内容和降级来源。

        返回 (content, source)，source 为 "agent" / "generic" / None。
        """
        skill_dir = Path(skill_dir)

        agent_skill = skill_dir / "agents" / self.name / "SKILL.md"
        if agent_skill.is_file():
            return agent_skill.read_text(encoding="utf-8"), "agent"

        generic_skill = skill_dir / "SKILL.md"
        if generic_skill.is_file():
            return generic_skill.read_text(encoding="utf-8"), "generic"

        return None, None
