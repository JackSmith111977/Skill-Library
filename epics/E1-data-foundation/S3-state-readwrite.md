# Story E1-S3: state.json 读写函数

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E1-S3 |
| Epic | E1 数据基础层 |
| 状态 | `pending` |
| 依赖 | E1-S1 |

## 需求

实现 state.json 的 load/save 函数，支持原子写入和异常处理

## 验收标准

1. load 函数：读取并解析 state.json，返回 dict
2. save 函数：原子写入（先写临时文件，再 rename）
3. 文件不存在时返回默认空结构
4. JSON 格式错误时抛出明确异常
5. 并发写入安全（文件锁）

## 接口设计

```python
class StateManager:
    def __init__(self, state_path: str):
        self.path = state_path

    def load(self) -> dict:
        """加载 state.json，不存在则返回空结构"""

    def save(self, state: dict) -> None:
        """原子写入 state.json"""

    def _atomic_write(self, data: str) -> None:
        """原子写入：临时文件 → rename"""
```

## 测试用例

```python
def test_load_existing():
    """加载已存在的 state.json"""

def test_load_missing():
    """文件不存在 → 返回空结构"""

def test_load_invalid_json():
    """JSON 格式错误 → 抛出异常"""

def test_save_atomic():
    """写入过程中断 → 文件不损坏"""

def test_save_concurrent():
    """并发写入 → 数据一致"""
```
