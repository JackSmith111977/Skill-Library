"""Claude Code 适配器"""

import re
from typing import Any

from .base import AgentAdapter
from .registry import get_registry


# argument-hint 格式
ARG_HINT_PATTERN = re.compile(r"\{\{(\w+(?:-\w+)*)\}\}")


class ClaudeCodeAdapter(AgentAdapter):
    """Claude Code 专用适配器。处理扩展 frontmatter 字段。"""

    @property
    def name(self) -> str:
        return "claude-code"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def target_patterns(self) -> list[str]:
        return ["claude-code", "claude-code-cli"]

    def adapt_content(self, content: str, frontmatter: dict[str, Any]) -> str:
        """适配内容。

        处理 Claude Code 扩展字段和注入语法。
        """
        # 提取扩展字段
        arg_hint = self._extract_arg_hint(frontmatter)
        model = self._extract_model(frontmatter)

        # 处理注入语法
        content = self._process_injections(content)

        # 添加参数提示（如果有）
        if arg_hint:
            hint_line = f"\n> Argument hint: {arg_hint}\n"
            content = hint_line + content

        return content

    def extract_extensions(self, frontmatter: dict[str, Any]) -> dict[str, Any]:
        """提取 Claude Code 扩展字段。"""
        return {
            "argument-hint": self._extract_arg_hint(frontmatter),
            "model": self._extract_model(frontmatter),
        }

    def _extract_arg_hint(self, frontmatter: dict[str, Any]) -> str | None:
        """提取 argument-hint 字段。"""
        hint = frontmatter.get("argument-hint")
        if hint:
            return str(hint)
        return None

    def _extract_model(self, frontmatter: dict[str, Any]) -> str | None:
        """提取 model 字段。"""
        model = frontmatter.get("model")
        if model:
            return str(model)
        return None

    def _process_injections(self, content: str) -> str:
        """处理动态注入语法。"""
        # 保留 {{argument}} 和 $(shell) 格式
        return content

    def parse_argument_hint(self, hint: str) -> list[str]:
        """解析 argument-hint 中的占位符。"""
        return ARG_HINT_PATTERN.findall(hint)


# 注册到全局注册表
def _register():
    registry = get_registry()
    from .generic import GenericAdapter
    registry.register(GenericAdapter(), default=True)
    registry.register(ClaudeCodeAdapter())


_register()
