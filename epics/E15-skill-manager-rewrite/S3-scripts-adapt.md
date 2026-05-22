# Story E15-S3: scripts 适配

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E15-S3 |
| Epic | E15 skill-manager 元 Skill 重写 |
| 状态 | `done` |
| 依赖 | - |

## 需求

更新 `skills/skill-manager/scripts/scan-and-register.sh`，去掉 `skill-manager register` CLI 依赖，改用直接调用 Python 模块。

## 验收标准

1. scan-and-register.sh 不再依赖 `skill-manager` CLI 命令
2. 改为调用 `python -m skill_library.registry.scanner` 或直接 import Python 模块
3. 脚本功能不变：扫描目录 → parse frontmatter → 写 state.json
4. 错误处理保留（目录不存在、parse 失败等）

## 实现方案

将 `skill-manager register` 替换为类似：

```bash
python -c "
from pathlib import Path
from skill_library.registry.scanner import scan_skills
from skill_library.registry.parser import parse_skill_md
from skill_library.state.manager import StateManager

sm = StateManager('state.json')
state = sm.load()
skills = scan_skills('$1')

for s in skills:
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
