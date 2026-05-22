# Story E8-S2: L2 指令加载器

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E8-S2 |
| Epic | E8 渐进式加载 |
| 状态 | `done` |
| 依赖 | E3-S2 |

## 需求

加载 SKILL.md 完整 body。

## 验收标准

1. 加载完整 body 内容
2. 返回 body 文本

## 测试用例

```python
def test_load_body(tmp_path): 加载 body
def test_load_empty_body(tmp_path): 空 body
```
