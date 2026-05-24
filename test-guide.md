# E2E 验证测试指南

> 版本：1.0.0 | 更新：2026-05-24
> 目的：新 Claude Code 会话中验证 Skill Library 管理功能端到端可用
> 前提：`git pull`，`pip install -r requirements.txt`，项目在 `D:\WorkPlace\VibeCoding\Skill Library`

---

## Phase 1：自动化测试门禁

验证 Python 模块层全部正常。

```bash
cd D:\WorkPlace\VibeCoding\Skill Library
python -m pytest tests/ -q
```

**预期**：334 passed，0 failed。

---

## Phase 2：Python 模块 CLI 测试

### 2.1 Skill 扫描

```bash
python -c "
from src.skill_library.registry.scanner import scan_skills
skills = scan_skills('skills')
for s in skills:
    print(s)
"
```

**预期**：列出所有 skill 目录路径，包含 writing/ 下 7 个。数量 ≥ 10。

### 2.2 Frontmatter 解析

```bash
python -c "
from src.skill_library.registry.parser import parse_skill_md
meta = parse_skill_md('skills/writing/research-assistant')
print('name:', meta['name'])
print('version:', meta['version'])
print('design-pattern:', meta['metadata'].get('design-pattern'))
print('allowed-tools:', meta.get('allowed-tools'))
"
```

**预期**：name=research-assistant, version=1.0.0, design-pattern=tool-wrapper, allowed-tools=[Read, WebSearch, WebFetch]

### 2.3 Lint 检测

```bash
# 原子 skill lint
python -m skill_library.quality.lint skills/writing/research-assistant

# 批量 lint 所有 skill
python -c "
from src.skill_library.quality.lint import QualityEngine
from src.skill_library.registry.scanner import scan_skills
engine = QualityEngine()
all_pass = True
for s in scan_skills('skills'):
    result = engine.lint_atomic(s)
    if not result.passed:
        print(f'FAIL: {s.name} score={result.score}')
        all_pass = False
if all_pass:
    print('All skills PASS')
"
```

**预期**：
- writing 包 5 原子 skill：全 PASS，score=100
- content-research、writing-pipeline：按原子规则检测，PASS
- 迁移模板（code-reviewer, data-validator, web-researcher）：PASS（已对齐标准格式）

### 2.4 State 读写

```bash
python -c "
from src.skill_library.state.manager import StateManager
sm = StateManager('state.json')
state = sm.load()
skills = state.get('skills', {})
print(f'Total registered: {len(skills)}')
for name, info in sorted(skills.items()):
    print(f'  {name}: mount={info[\"mount-status\"]} quality={info[\"quality-status\"]} pack={info[\"pack\"]}')
agents = state.get('agents', {})
print(f'Total agents: {len(agents)}')
"
```

**预期**：Total=10，所有 mount=unmounted, quality=unchecked。Agents 可能为空（未配置）。

### 2.5 Skill 查询

```bash
python -c "
from src.skill_library.state.manager import StateManager
from src.skill_library.registry.indexer import SkillIndexer
sm = StateManager('state.json')
idx = SkillIndexer(sm)

# 按 pack 查
writing = idx.query_by_category('technical')
print(f'Technical skills: {len(writing)}')

# 按 design-pattern 查
generators = idx.query_by_design_pattern('generator')
print(f'Generator skills: {len(generators)}')
for name in generators:
    print(f'  - {name}')
"
```

**预期**：
- Technical 应有 writing 包 + 迁移模板
- Generator 应有 article-writer, blog-post-writer, academic-writer

---

## Phase 3：Meta-skill 管理测试（AI 驱动）

在新 Claude Code 会话中执行。AI 应自动加载 `skill-manager` 元 skill 来完成管理操作。

### 3.1 触发 skill-manager 执行 lint

**用户输入**：
```
运行 lint 检查 skills/writing/research-assistant
```

**验证点**：
- AI 识别为管理任务，触发 skill-manager
- 正确调用 `python -m skill_library.quality.lint` 或 `QualityEngine.lint_atomic()`
- 输出 PASS/FAIL 结果

### 3.2 Quality 状态更新

**用户输入**：
```
lint 通过了，更新 state.json 中 research-assistant 的 quality-status 为 passed
```

**验证点**：
- AI 读取 state.json
- 找到 skills.research-assistant
- 将 quality-status 从 unchecked 改为 passed
- 写回 state.json

### 3.3 注册新 skill

**用户输入**：
```
注册 skills/utility/web-researcher 到 state
```

**验证点**：
- AI 读取 SKILL.md frontmatter
- 构建 entry（name, path, version, type, design-pattern, allowed-tools）
- 写入 state.json skills 段
- 不重复注册

### 3.4 查看注册表

**用户输入**：
```
列出所有已注册的 skill
```

**验证点**：
- AI 读取 state.json
- 遍历 skills 段
- 格式化输出（名称、版本、状态、包）

---

## Phase 4：Writing 包端到端测试（AI 驱动）

### 4.1 research-assistant

**用户输入**：
```
帮我调研一下 Agent Skill 格式规范的最新发展
```

**验证点**：
- AI 匹配到 research-assistant skill（description 触发短语）
- 使用 WebSearch 搜索，WebFetch 获取内容
- 输出结构化调研摘要
- 有来源引用

### 4.2 article-writer

**用户输入**：
```
标题：AI 编程工具对比，大纲：优势、劣势、选型建议，帮我写成文章
```

**验证点**：
- AI 匹配到 article-writer
- 输出有章节标题
- 有引言和结论
- 格式干净

### 4.3 copy-editor

**用户输入**：
```
"Artificial intelligence is a tools that help human to do there work more efficient. It have many application in different field. Some people think it will replace them. But actually it just a tool." 帮我 review 这段文字
```

**验证点**：
- AI 匹配到 copy-editor
- 输出按严重程度分类
- 只提建议，不重写
- 有 overall assessment

### 4.4 writing-pipeline 工作流

**用户输入**：
```
帮我从零开始写一篇关于远程工作的文章，调研+写作+审校完整流程
```

**验证点**：
- AI 按 pipeline 三步执行（research-assistant → article-writer → copy-editor）
- 每个阶段有 STAGE_GATE 检查
- 最终交付：文章 + edit report

---

## Phase 5：边界与异常测试

### 5.1 重复注册

```bash
python -c "
from src.skill_library.state.manager import StateManager
from src.skill_library.registry.indexer import SkillIndexer
sm = StateManager('state.json')
idx = SkillIndexer(sm)
idx.register('skills/writing/research-assistant')
state = sm.load()
count = len([s for s in state['skills'] if s.startswith('research-assistant')])
print(f'research-assistant entries: {count}')
"
```

**预期**：重复注册不会创建重复条目（indexer 按 name 覆盖，只保留最新 entry）。

### 5.2 不存在的 skill 注销

```bash
python -c "
from src.skill_library.state.manager import StateManager
from src.skill_library.registry.indexer import SkillIndexer
sm = StateManager('state.json')
idx = SkillIndexer(sm)
try:
    idx.unregister('non-existent-skill')
except KeyError as e:
    print(f'Expected error: {e}')
"
```

**预期**：抛出 KeyError。

### 5.3 空目录扫描

```bash
mkdir skills/test-empty
python -c "
from src.skill_library.registry.scanner import scan_skills
skills = scan_skills('skills/test-empty')
print(f'Skills in empty dir: {len(skills)}')
"
rmdir skills/test-empty
```

**预期**：0 skill 被发现。

---

## 测试结果记录

测试执行后，按以下格式填写报告：

```markdown
# E2E Test Report

日期：YYYY-MM-DD
测试环境：OS: Windows 11 | Python: 3.x | Claude Code: 版本

| Phase | 测试项 | 结果 | 备注 |
|-------|--------|------|------|
| 1 | pytest | ✅/❌ | |
| 2.1 | scan_skills | ✅/❌ | |
| 2.2 | parse_skill_md | ✅/❌ | |
| 2.3 | lint | ✅/❌ | |
| 2.4 | state read | ✅/❌ | |
| 2.5 | query | ✅/❌ | |
| 3.1 | skill-manager lint | ✅/❌ | |
| 3.2 | quality status update | ✅/❌ | |
| 3.3 | register new skill | ✅/❌ | |
| 3.4 | list registry | ✅/❌ | |
| 4.1 | research-assistant | ✅/❌ | |
| 4.2 | article-writer | ✅/❌ | |
| 4.3 | copy-editor | ✅/❌ | |
| 4.4 | writing-pipeline | ✅/❌ | |
| 5.1 | duplicate register | ✅/❌ | |
| 5.2 | non-existent unregister | ✅/❌ | |
| 5.3 | empty dir scan | ✅/❌ | |

结论：
- 通过率：X/16
- 阻塞项：
- 待修复：
```

---

## 已知限制

1. **lint CLI 不支持 --profile**：CLI 只能用默认 skill-library profile，API 调用正常
2. **lint CLI 不支持 workflow**：工作流 4 项额外规则无法通过 CLI 触发，需 API
3. **state.json 写操作分散**：绕过 StateManager 直接写 state.json 可能在测试中出现不一致
4. **mount/unmount 测试需 agent 目录**：目标路径需确认（如 `~/.claude/skills/`）
5. **IMPLEMENTATION.md 未同步**：当前标记 needs-update，不影响功能测试
