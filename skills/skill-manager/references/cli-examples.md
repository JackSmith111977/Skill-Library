# CLI 使用示例

## 完整工作流

```bash
# 1. 创建新 skill
skill-manager create data-validator --pack dev --type atomic --design-pattern pipeline

# 2. 编写内容后 lint
skill-manager lint skills/dev/data-validator

# 3. 注册到 registry
skill-manager register skills/dev/data-validator --category data

# 4. 验证后再 mount
skill-manager mount data-validator

# 5. 加载到上下文使用
skill-manager load data-validator --level L2

# 6. 列出已注册 skills
skill-manager list

# 7. 按类型过滤
skill-manager list --type atomic

# 8. 卸载
skill-manager unmount data-validator
```

## JSON 输出

```bash
# lint 结果 JSON
skill-manager lint skills/dev/data-validator --json

# 列表 JSON
skill-manager list --json
```

## 批量操作

```bash
# 注册目录下所有 skill
for dir in skills/dev/*/; do
  skill-manager register "$dir"
done

# 批量 lint
for dir in skills/*/; do
  skill-manager lint "$dir" || echo "FAIL: $dir"
done
```

## 包管理

```bash
# 按包查看
skill-manager list --pack dev
skill-manager list --pack ai

# 按设计模式
skill-manager list --design-pattern pipeline
```
