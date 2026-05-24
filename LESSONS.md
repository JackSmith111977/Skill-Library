# Lessons Learned

> 版本：1.0.0 | 更新：2026-05-24

项目开发过程中记录的问题、根因与改进措施。每次新问题发现后追加，定期复盘。

---

## 1. Shell 脚本写入 JSON 导致变量注入

**问题**：Phase 0 用 Bash heredoc 创建 pack.json，变量引用 `'$pack'` 外层单引号阻止 shell 展开，6 个 pack.json 的 name 和 description 被写入字面量 `'$pack'`，未被发现直到 writing 包开发完成后才修复。

**根因**：
- Shell 脚本操作 JSON 不可靠，引号层级易出错
- pack.json 创建后无人验证内容
- Git diff 被大量文件变更淹没，未逐行审查

**改进**：
- pack.json 创建/更新必须用 Python 脚本，禁用 Shell heredoc
- `git diff --stat` 后必须抽查文件内容
- 提交前检查清单加：`□ pack.json 验证：python -c "check all pack.json fields"`

---

## 2. CLI 参数裸解析导致功能不可用

**问题**：lint CLI 用 `sys.argv[1:]` 裸解析路径，`--profile` 标志被当作路径参数传入。用户无法通过 CLI 切换 profile 或执行 workflow lint。

**根因**：
- 初期偷懒未引入 argparse，认为"够用"
- `main()` 与 `QualityEngine` API 能力不同步（API 支持 profile 和 workflow，CLI 不支持）

**改进**：
- CLI 入口必须使用 argparse，从第一天起
- `main()` 功能必须是 `QualityEngine` 能力的超集或完整映射
- 参数解析与业务逻辑分离

---

## 3. 注册时机绑定导致版本漂移

**问题**：`SkillIndexer.register()` 在注册时刻读取 pack.json 版本。先注册后更新 pack.json 时，state.json 中的 `pack-version` 过期。

**根因**：
- 注册是一次性操作，无刷新机制
- 未区分"创建时快照"和"同步时更新"

**改进**：
- 加 `reindex` / `refresh` 命令：重新读取 pack.json 刷新 state
- 注册时记录 `registered-at` 时间戳，便于判断过期
- 考虑注册时存引用路径而非内联版本，查询时实时读取

---

## 4. state.json 编码未统一导致 Windows 崩溃

**问题**：Windows Python 3 `open()` 默认 GBK 编码，state.json 存为 UTF-8。直接调用 `json.load(f)` 在 Bash/Python 脚本中崩溃，仅在 Windows 平台复现。

**根因**：
- StateManager 内部使用 `encoding='utf-8'`，但外部 raw Python 脚本未遵循
- 无强制编码规范

**改进**：
- 所有文件操作显式 `encoding='utf-8'`，写入项目级 lint 规则
- StateManager 对外提供 `read_state()` / `write_state()` 静态方法，封装编码细节
- 禁止直接 `open('state.json')` — 审计发现即拒绝

---

## 5. 绕过 StateManager 直接写 state.json

**问题**：多处 raw Python 脚本直接 `open('state.json').write()`，绕过 StateManager 的 atomic write 保护。并发写可能损坏文件。

**根因**：
- StateManager 初期未提供批量操作接口，调用方被迫绕过
- 无架构合规检查

**改进**：
- StateManager 补齐缺失接口（batch_register, batch_update）
- 代码审查加规则：state.json 只能通过 StateManager 操作
- 考虑加写锁或临时文件 + rename 模式

---

## 6. 文档与代码不同步（IMPLEMENTATION.md 滞后）

**问题**：PRD 更新到 v2.0.0（Scope + 17 分类 + OpenCode），但 IMPLEMENTATION.md 停留在 v1.7.0，标记 "needs-update" 但一直未排期。

**根因**：
- 实现文档更新没有独立 Story，被当作"做完有空再补"
- docs-alignment.json 允许 needs-update 状态，但无自动提醒或门禁

**改进**：
- IMPLEMENTATION.md 更新必须作为独立 Story 排入迭代
- 提交前检查清单加：`□ IMPLEMENTATION.md 与当前架构一致`
- 考虑加 CI 机制：docs-alignment 中有 needs-update 时阻止合并

---

## 模式总结

| 模式 | 表现 | 应对 |
|------|------|------|
| 偷懒引入技术债 | CLI 用 sys.argv，文件操作用 Shell heredoc | 基础设施代码必须用 argparse + Python |
| 一次性操作产生漂移 | register 后版本不同步 | 设计时考虑刷新/同步机制 |
| 平台差异被忽视 | Windows GBK vs UTF-8 | 跨平台项目统一编码规范 |
| 架构边界被绕过 | 直接写 state.json | 补齐接口 + 审查门禁 |
| 文档滞后无人管 | IMPLEMENTATION.md 长期 needs-update | Story 化 + CI 门禁 |
