# 管理操作示例

Skill-based 操作指南。所有操作通过 AI Agent 直接执行，不依赖 CLI。

## 完整工作流

### 1. Lint 检查质量

```bash
python -m skill_library.quality.lint skills/dev/data-validator
# 输出: passed=True, score=100
```

指定 profile 适配不同 skill 格式：

```bash
python -m skill_library.quality.lint ~/.claude/skills/research --profile claude-code
python -m skill_library.quality.lint skills/my-skill --profile skill-library
```

### 2. Register 注册到仓库

扫描目录，解析 frontmatter，写入 state.json：

```bash
python -c "
from skill_library.registry.scanner import scan_skills
from skill_library.registry.parser import parse_skill_md
from skill_library.state.manager import StateManager

sm = StateManager('state.json')
state = sm.load()
for s in scan_skills('skills/dev'):
    meta = parse_skill_md(s)
    name = meta['name']
    state.setdefault('skills', {})[name] = {
        'name': name,
        'path': str(s),
        'version': meta.get('version', '0.0.0'),
        'mount-status': 'unmounted',
        'quality-status': 'unchecked',
    }
sm.save(state)
"
```

### 3. Mount 挂载到 Agent

```bash
# 前置条件：skill quality-status == 'passed'
# 复制到 Claude Code 技能目录
cp -r skills/dev/data-validator ~/.claude/skills/data-validator

# 更新 state.json
python -c "
from skill_library.state.manager import StateManager
sm = StateManager('state.json')
state = sm.load()
state['agents']['claude-code']['skills']['data-validator'] = {
    'status': 'mounted',
    'version': '1.0.0',
    'adapter': 'generic',
}
state['skills']['data-validator']['mount-status'] = 'mounted'
state['skills']['data-validator'].setdefault('mounted-to', []).append('claude-code')
sm.save(state)
"
```

### 4. 验证挂载状态

```bash
python -c "
from skill_library.state.manager import StateManager
sm = StateManager('state.json')
state = sm.load()
s = state['skills']['data-validator']
print(f'mount-status: {s[\"mount-status\"]}')
print(f'mounted-to: {s.get(\"mounted-to\", [])}')
"
```

### 5. Unmount 卸载

```bash
# 从 Agent 移除
rm -rf ~/.claude/skills/data-validator

# 更新 state.json
python -c "
from skill_library.state.manager import StateManager
sm = StateManager('state.json')
state = sm.load()
del state['agents']['claude-code']['skills']['data-validator']
state['skills']['data-validator']['mount-status'] = 'unmounted'
state['skills']['data-validator'].get('mounted-to', []).remove('claude-code')
sm.save(state)
"
```

## 多 Agent 场景

同一 skill 挂载到多个 agent：

```bash
# 挂载到 Agent A 和 Agent B
cp -r skills/dev/data-validator ~/agent-a/skills/data-validator
cp -r skills/dev/data-validator ~/agent-b/skills/data-validator

# 分别写 state 记录
# ... 重复 mount step 3 逻辑, 不同 agent-id

# 卸载其中一个不影响另一个
rm -rf ~/agent-a/skills/data-validator
# state: 只清除 agent-a 的记录, agent-b 保留
```

## 批量操作

```bash
# 批量 lint
for dir in skills/*/; do
  python -m skill_library.quality.lint "$dir"
done

# 批量注册
python -c "
from skill_library.registry.scanner import scan_skills
from skill_library.state.manager import StateManager
from skill_library.registry.parser import parse_skill_md
sm = StateManager('state.json')
state = sm.load()
for s in scan_skills('skills'):
    meta = parse_skill_md(s)
    name = meta['name']
    state.setdefault('skills', {})[name] = {'name': name, 'path': str(s), 'mount-status': 'unmounted', 'quality-status': 'unchecked'}
sm.save(state)
"
```

## 附录：CLI 等效命令

CLI 工具 `skill-manager` 提供相同功能（需 `pip install -e .`）：

```bash
skill-manager lint skills/dev/data-validator
skill-manager register skills/dev/data-validator
skill-manager mount data-validator
skill-manager unmount data-validator
skill-manager list
```

效果与 skill-based 方式一致，CLI 为选配。
