# Story E3-S1: 目录扫描器

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E3-S1 |
| Epic | E3 Skill Registry |
| 状态 | `done` |
| 依赖 | E1-S1 |

## 需求

扫描 skill 目录，识别标准目录结构中的 skill。

## 验收标准

1. 扫描指定目录，返回所有包含 SKILL.md 的子目录
2. 跳过隐藏目录（以 `.` 开头）和特殊目录（`__pycache__` 等）
3. 返回 skill 路径列表

## 测试用例

```python
def test_scan_valid_dir(tmp_path): 找到包含 SKILL.md 的目录
def test_scan_empty_dir(tmp_path): 空目录返回空列表
def test_scan_skip_hidden(tmp_path): 跳过 .hidden 目录
def test_scan_skip_pycache(tmp_path): 跳过 __pycache__ 目录
def test_scan_nested(tmp_path): 只扫描一层，不递归
```
