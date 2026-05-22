"""通用适配器：原样输出"""

from typing import Any

from .base import AgentAdapter


class GenericAdapter(AgentAdapter):
    """通用适配器，不做任何转换。"""

    @property
    def name(self) -> str:
        return "generic"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def target_patterns(self) -> list[str]:
        return []

    def adapt_content(self, content: str, frontmatter: dict[str, Any]) -> str:
        return content
