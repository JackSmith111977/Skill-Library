#!/bin/bash
# Skill Library 升级脚本
# 检查当前版本 → 查询最新 Release → 执行升级

set -euo pipefail

REPO="user/skill-library"  # TODO: 替换为实际仓库地址

echo "=== Skill Library Upgrade ==="

# 检查当前版本
if ! git describe --tags >/dev/null 2>&1; then
    echo "No version tag found. Run 'git fetch --tags' first."
    CURRENT="none"
else
    CURRENT=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")
fi
echo "Current version: $CURRENT"

# 查询最新 Release
echo "Checking latest release..."
LATEST=$(curl -sf "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null | grep '"tag_name"' | cut -d'"' -f4 || echo "")

if [ -z "$LATEST" ]; then
    echo "Failed to fetch latest release info."
    echo "Check network or update REPO variable in this script."
    exit 1
fi

echo "Latest version: $LATEST"

# 版本比较
if [ "$CURRENT" = "$LATEST" ]; then
    echo "Already up to date."
    exit 0
fi

echo ""
echo "Upgrade available: $CURRENT → $LATEST"
echo "Proceed? [y/N]"
read -r CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Upgrade cancelled."
    exit 0
fi

# 执行升级
echo "Pulling latest code..."
git pull origin main

echo "Reinstalling dependencies..."
pip install -r requirements.txt

echo ""
echo "=== Upgrade complete ==="
echo "Current version: $(git describe --tags --abbrev=0 2>/dev/null || echo 'unknown')"
echo "Run 'pytest tests/ -q' to verify."
