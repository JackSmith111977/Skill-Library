"""state.json 读写管理器"""

import json
import tempfile
from pathlib import Path
from typing import Any


class StateManager:
    """state.json 读写管理器，支持原子写入"""

    def __init__(self, state_path: str | Path):
        self.path = Path(state_path)

    def load(self) -> dict[str, Any]:
        """加载 state.json，不存在则返回空结构"""
        if not self.path.exists():
            return self._empty_state()

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"state.json 格式错误: {e}") from e

    def save(self, state: dict[str, Any]) -> None:
        """原子写入 state.json"""
        data = json.dumps(state, indent=2, ensure_ascii=False)
        self._atomic_write(data)

    def _atomic_write(self, data: str) -> None:
        """原子写入：临时文件 → rename"""
        self.path.parent.mkdir(parents=True, exist_ok=True)

        # 写入临时文件
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self.path.parent,
            suffix=".tmp",
            delete=False
        ) as tmp:
            tmp.write(data)
            tmp_path = Path(tmp.name)

        try:
            # 原子替换
            tmp_path.replace(self.path)
        except Exception:
            # 清理临时文件
            if tmp_path.exists():
                tmp_path.unlink()
            raise

    def _empty_state(self) -> dict[str, Any]:
        """返回空状态结构"""
        return {
            "library": {
                "path": "",
                "created-at": "",
                "last-sync": ""
            },
            "agents": {},
            "skills": {}
        }
