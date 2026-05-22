# Story E1-S4: config.json 读写函数

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E1-S4 |
| Epic | E1 数据基础层 |
| 状态 | `pending` |
| 依赖 | E1-S2 |

## 需求

实现 config.json 的 load/save 函数，支持路径校验

## 验收标准

1. load 函数：读取并解析 config.json
2. save 函数：写入 config.json
3. 路径校验：library-path 必须是绝对路径
4. Agent path 必须是绝对路径
5. 文件不存在时抛出异常（config 必须手动创建）

## 接口设计

```python
class ConfigManager:
    def __init__(self, config_path: str):
        self.path = config_path

    def load(self) -> dict:
        """加载 config.json"""

    def save(self, config: dict) -> None:
        """保存 config.json"""

    def validate_paths(self, config: dict) -> list:
        """校验路径合法性，返回错误列表"""
```

## 测试用例

```python
def test_load_valid():
    """加载合法 config.json"""

def test_load_missing():
    """文件不存在 → 抛出异常"""

def test_validate_absolute_path():
    """绝对路径 → 校验通过"""

def test_validate_relative_path():
    """相对路径 → 校验失败"""
```
