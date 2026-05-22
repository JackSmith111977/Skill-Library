# Story E7-S6: Agent 版本降级逻辑

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E7-S6 |
| Epic | E7 Agent 适配框架 |
| 状态 | `done` |
| 依赖 | E7-S1 |

## 需求

实现 agent 版本降级策略。

## 验收标准

1. 优先加载 `agents/<agent-name>/SKILL.md`
2. 无匹配时降级到通用 SKILL.md
3. 降级逻辑返回值明确

## 测试用例

```python
def test_prefer_agent_version(tmp_path): 优先 agent 版
def test_fallback_generic(tmp_path): 降级到通用版
def test_no_skill_md(tmp_path): 无文件返回 None
```
