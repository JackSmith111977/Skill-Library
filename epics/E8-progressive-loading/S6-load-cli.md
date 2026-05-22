# Story E8-S6: load CLI 命令

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E8-S6 |
| Epic | E8 渐进式加载 |
| 状态 | `done` |
| 依赖 | E8-S1 |

## 需求

`skill-manager load` 命令手动加载 skill。

## 验收标准

1. `skill-manager load <name>` 加载 skill
2. 支持 --level L1/L2/L3
3. 输出加载状态

## 测试用例

```python
def test_load_cmd(runner): 加载命令
def test_load_with_level(runner): 指定级别
```
