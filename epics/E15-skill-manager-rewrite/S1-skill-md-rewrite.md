# Story E15-S1: SKILL.md body 重写

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E15-S1 |
| Epic | E15 skill-manager 元 Skill 重写 |
| 状态 | `done` |
| 依赖 | - |

## 需求

将 `skills/skill-manager/SKILL.md` 的 body 从 CLI 命令手册重写为 skill-based 操作流程。保留 frontmatter 不变。

## 验收标准

1. body 不再将 `skill-manager xxx` 列为主要/唯一操作方式
2. mount 操作为 `cp -r` + state.json 更新流程
3. unmount 操作为 `rm -rf` + state.json 更新流程
4. lint 操作为 `python -m skill_library.quality.lint` Bash 调用
5. register 操作为扫描目录 + parse + 写 state.json 流程
6. 保留 state management / classification / directory layout 等概念说明
7. CLI 命令仅以「附录」或「选配」形式提及
8. 通过 lint 检测（原子 skill 7 项，score >= 90）

## 内容大纲

- 项目定位（Skill 即接口哲学）
- 前置条件：Skill Library 目录结构 + Python 依赖
- 管理操作（每个操作含具体步骤）：
  - mount：检查 quality → cp 目录 → 更新 state.json
  - unmount：检查挂载状态 → rm 目录 → 更新 state.json
  - lint：Bash 调用 Python 质量引擎
  - register：扫描目录 → parse frontmatter → 写 state.json
  - status：读 state.json
- 多 Agent 挂载说明
- State Management（状态转换规则）
- 附录：CLI 选配层说明

## 涉及的 Python 模块（供 Bash 调用参考）

| 操作 | 命令 |
|------|------|
| lint | `python -m skill_library.quality.lint <path>` |
| scanner | `python -c "from skill_library.registry.scanner import scan_skills; print(scan_skills('skills'))"` |
| parser | `python -c "from skill_library.registry.parser import parse_skill_md; print(parse_skill_md('skills/pack/name'))"` |
| state 读写 | `python -c "from skill_library.state.manager import StateManager; sm=StateManager('state.json'); s=sm.load(); sm.save(s)"` |
