# Story E17-S2: 更新项目配置

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E17-S2 |
| Epic | E17 CLI 层完全移除 |
| 状态 | `done` |
| 依赖 | - |

## 需求

从 pyproject.toml 和 requirements.txt 中移除 click 和 rich 依赖。

## 验收标准

1. `pyproject.toml` 无 click/rich 依赖行
2. `pyproject.toml` 无 `[project.scripts]` 块
3. `requirements.txt` 无 click/rich 行
4. `pip install -e .` 正常安装，不报错

## 改动文件

| 文件 | 改动 |
|------|------|
| `pyproject.toml` | 移除 `click>=8.0`, `rich>=13.0`, `[project.scripts]` |
| `requirements.txt` | 移除 `click>=8.0`, `rich>=13.0` |
