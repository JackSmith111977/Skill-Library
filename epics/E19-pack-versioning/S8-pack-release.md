# Story E19-S8: 更新 Release 流程支持包级发布

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E19-S8 |
| Epic | E19 技能包官方版本化 |
| 状态 | `done` |
| 依赖 | E19-S7 |

## 需求

在 Release 流程中增加 pack 版本清单，Release 正文列出所有包的版本信息。

## 验收标准

1. Release 正文包含所有 pack 的版本总览表
2. 每个 pack 的版本可被 Agent 解析读取
3. 扩展 `release.yml` 生成 pack-version manifest

## 改动

| 文件 | 改动 |
|------|------|
| `.github/workflows/release.yml` | 新增 pack version 报告步骤 |
