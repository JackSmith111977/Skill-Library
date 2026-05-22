# Epic 17: CLI 层完全移除

> **主题**：删除全部 CLI 代码、测试、依赖和文档引用，实现纯 Skill 即接口架构。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E17 |
| 优先级 | P1 |
| Story 数 | 5 |
| 依赖 | E15（Skill 即接口设计已确立）, E16（README/PRD 规范已对齐）|
| 状态 | `done` |

## 影响范围

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| `src/skill_library/cli/` | 删除 | 全部 7 文件 |
| `tests/test_cli/` | 删除 | 全部 3 文件 |
| `tests/test_templates/test_create_cli.py` | 删除 | CLI 创建测试 |
| `pyproject.toml` | 修改 | 移除 console_scripts + click/rich 依赖 |
| `requirements.txt` | 修改 | 移除 click/rich |
| `PRD.md` | 修改 | 移除 §5.3 CLI 附录 |
| `IMPLEMENTATION.md` | 修改 | 移除 CLI 引用 |
| `CLAUDE.md` | 修改 | 移除 CLI 可选说明 |
| `README.md` | 修改 | 移除 CLI 段落 |
| `skills/skill-manager/SKILL.md` | 修改 | 移除附录 CLI |
| `skills/skill-manager/references/cli-examples.md` | 修改 | 移除附录 CLI |
| `docs-alignment.json` | 修改 | 版本 bump |

## 不改动的

- 核心 Python 模块（state/quality/registry/loader/templates/adapters）— 零改动
- 非 CLI 测试 — 零改动
- skill-manager/creator/workflow-creator 的 SKILL.md body — 仅删附录
- jsonschema/pyyaml/gitpython 依赖 — 保留

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E17-S1 | 删除 CLI 源代码 + 测试文件 | `done` | - |
| E17-S2 | 更新项目配置 | `done` | - |
| E17-S3 | 更新文档（PRD/IMPLEMENTATION/CLAUDE） | `done` | - |
| E17-S4 | 更新 README + skill 文档 | `done` | - |
| E17-S5 | 最终验证 + 文档对齐 | `done` | E17-S1~S4 |

## 测试门禁

```bash
cd "D:\WorkPlace\VibeCoding\Skill Library"
python -m pytest tests/ -q                       # 333 passed
python -m skill_library.quality.lint skills/skill-manager  # >=90
grep -rn "click\|CliRunner" src/                 # 0 hits
grep -rn "click\|CliRunner" tests/               # 0 hits
```
