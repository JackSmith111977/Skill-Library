# Story E4-S7: init 初始化

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E4-S7 |
| Epic | E4 状态机引擎 |
| 状态 | `done` |
| 依赖 | E1-S3, E1-S4 |

## 需求

初始化 skill library 环境。

## 验收标准

1. 创建 state.json（不存在时）
2. 创建 config.json（不存在时）
3. 创建 skills 目录
4. 已存在时不覆盖

## 测试用例

```python
def test_init_creates_state(): 创建 state.json
def test_init_creates_config(): 创建 config.json
def test_init_creates_dirs(): 创建目录
def test_init_no_overwrite(): 已存在不覆盖
```
