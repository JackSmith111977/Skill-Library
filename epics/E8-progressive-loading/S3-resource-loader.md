# Story E8-S3: L3 资源加载器

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E8-S3 |
| Epic | E8 渐进式加载 |
| 状态 | `done` |
| 依赖 | - |

## 需求

按需加载 references/ assets/ 等捆绑资源。

## 验收标准

1. 加载 references/ 下所有文件
2. 加载 assets/ 下文件列表
3. 无大小限制

## 测试用例

```python
def test_load_references(tmp_path): 加载 references
def test_load_assets(tmp_path): 加载 assets
def test_no_resources(tmp_path): 无资源返回空
```
