# Epic 3: Skill Registry

> **主题**：实现 skill 目录扫描、注册、索引、查询功能。

## 元数据

| 属性 | 值 |
|------|-----|
| ID | E3 |
| 优先级 | P0 |
| Story 数 | 6 |
| 依赖 | E1 |
| 状态 | `pending` |

## Story 列表

| ID | Story | 状态 | 依赖 |
|----|-------|------|------|
| E3-S1 | 目录扫描器 | `pending` | E1-S1 |
| E3-S2 | frontmatter 解析器 | `pending` | - |
| E3-S3 | skill 注册函数 | `pending` | E3-S1, E3-S2 |
| E3-S4 | skill 注销函数 | `pending` | E1-S3 |
| E3-S5 | skill 查询接口 | `pending` | E1-S3 |
| E3-S6 | 二维分类标记 | `pending` | E3-S3 |

## 测试门禁

```bash
# 单元测试
pytest tests/test_registry/test_scanner.py -v
pytest tests/test_registry/test_indexer.py -v

# 集成测试
pytest tests/test_registry/test_query.py -v

# 验收条件
- [ ] 扫描器能识别标准目录结构
- [ ] frontmatter 解析覆盖所有标准字段
- [ ] 注册/注销操作状态同步正确
- [ ] 查询接口返回格式正确
- [ ] 二维分类字段写入正确
```
