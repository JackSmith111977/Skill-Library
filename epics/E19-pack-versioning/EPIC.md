# Epic 19: 技能包官方版本化

> **主题**：为每个分类包建立独立版本管理骨架，Agent 可按需挂载各能力模块。
>
> **范围限制**：本 Epic 只建立包骨架（pack.json + 目录结构 + state 扩展），不填充实际 skill 内容。每个技能包的具体 skill 实现需独立设计，不在本 Epic 范围内。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E19 |
| 优先级 | P1 |
| Story 数 | 9 |
| 依赖 | E13（分类包定义已确立），E18（CI/CD 基础设施）|
| 状态 | `done` |

## 影响范围

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| `PRD.md` | 修改 | 新增 §14 技能包版本化 |
| `IMPLEMENTATION.md` | 修改 | 新增 §9.4 技能包版本管理 |
| `research/ci-cd-and-version-management.md` | 新建 | 调研文档 |
| `skills/meta/pack.json` | 新建 | meta 包版本声明 |
| `skills/retrieval/pack.json` | 新建 | retrieval 包版本声明 |
| `skills/web/pack.json` | 新建 | web 包版本声明 |
| `skills/document/pack.json` | 新建 | document 包版本声明 |
| `skills/development/pack.json` | 新建 | development 包版本声明 |
| `skills/devops/pack.json` | 新建 | devops 包版本声明 |
| `skills/communication/pack.json` | 新建 | communication 包版本声明 |
| `skills/learning/pack.json` | 新建 | learning 包版本声明 |
| `skills/security/pack.json` | 新建 | security 包版本声明 |
| `skills/data/pack.json` | 新建 | data 包版本声明 |
| `skills/*/references/` | 新建 | 每个包的空 refs 目录 |
| `skills/*/assets/` | 新建 | 每个包的空 assets 目录 |
| `src/skill_library/state/enums.py` | 修改 | 扩展 state schema |
| `state.json` | 修改 | 新增 pack-version 字段 |
| `docs-alignment.json` | 修改 | 版本同步 |
| `PROGRESS.md` | 修改 | 进度日志 |

## 不改动的

- 现有 3 个 meta-skill 的 SKILL.md body — 仅新增 pack info
- 核心 Python 模块的现有接口 — 零改动
- 现有测试 — 零改动

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E19-S1 | PRD 更新 | `done` | - |
| E19-S2 | 网络调研 | `done` | - |
| E19-S3 | IMPLEMENTATION.md 更新 | `done` | E19-S1, S2 |
| E19-S4 | pack.json Schema 定义 | `done` | - |
| E19-S5 | 创建全部 10 个包目录 + pack.json | `done` | E19-S4 |
| E19-S6 | state.json 扩展包版本字段 | `done` | E19-S5 |
| E19-S7 | skill-manager 包级操作 | `done` | E19-S6 |
| E19-S8 | 更新 Release 流程支持包级发布 | `done` | E19-S7 |
| E19-S9 | Epic 文档 + 验证 | `done` | E19-S4~S8 |

## 测试门禁

```bash
pytest tests/ -q                                     # all tests pass
python -c "import json; json.load(open('skills/meta/pack.json'))"  # pack.json valid
python -c "
import json
s = json.load(open('state.json'))
assert 'pack-version' in s['skills']['skill-manager']
"                                                     # pack version tracked
```
