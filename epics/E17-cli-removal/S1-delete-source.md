# Story E17-S1: 删除 CLI 源代码 + 测试文件

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E17-S1 |
| Epic | E17 CLI 层完全移除 |
| 状态 | `done` |
| 依赖 | - |

## 需求

删除 CLI 全部源代码和测试文件。

## 验收标准

1. `src/skill_library/cli/` 目录完全删除
2. `tests/test_cli/` 目录完全删除
3. `tests/test_templates/test_create_cli.py` 文件删除
4. `src/skill_library/__init__.py` 中无 cli 导入残留
5. `grep -rn "click\|CliRunner" src/` 返回 0

## 改动文件

| 文件 | 操作 |
|------|------|
| `src/skill_library/cli/` (7 文件) | 删除 |
| `tests/test_cli/` (3 文件) | 删除 |
| `tests/test_templates/test_create_cli.py` | 删除 |
