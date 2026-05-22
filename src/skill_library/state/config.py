"""config.json 读写管理器"""

import json
from pathlib import Path
from typing import Any


class ConfigManager:
    """config.json 读写管理器，支持路径校验"""

    def __init__(self, config_path: str | Path):
        self.path = Path(config_path)

    def load(self) -> dict[str, Any]:
        """加载 config.json，不存在则抛出异常"""
        if not self.path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.path}")

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"config.json 格式错误: {e}") from e

    def save(self, config: dict[str, Any]) -> None:
        """保存 config.json"""
        errors = self.validate_paths(config)
        if errors:
            raise ValueError(f"路径校验失败: {'; '.join(errors)}")

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def validate_paths(self, config: dict[str, Any]) -> list[str]:
        """校验路径合法性，返回错误列表"""
        errors = []

        # 校验 library-path
        library_path = config.get("library-path", "")
        if not library_path:
            errors.append("缺少 library-path")
        elif not Path(library_path).is_absolute():
            errors.append(f"library-path 必须是绝对路径: {library_path}")

        # 校验 agent paths
        agents = config.get("agents", {})
        for agent_id, agent_config in agents.items():
            agent_path = agent_config.get("path", "")
            if not agent_path:
                errors.append(f"Agent {agent_id} 缺少 path")
            elif not Path(agent_path).is_absolute():
                errors.append(f"Agent {agent_id} path 必须是绝对路径: {agent_path}")

        return errors
