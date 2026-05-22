# Skill Library 升级脚本 (PowerShell)
# 检查当前版本 → 查询最新 Release → 执行升级

$Repo = "user/skill-library"  # TODO: 替换为实际仓库地址

Write-Host "=== Skill Library Upgrade ===" -ForegroundColor Cyan

# 检查当前版本
$Current = "none"
try {
    $Current = git describe --tags --abbrev-of 2>$null
    if (-not $Current) { $Current = "none" }
} catch {
    $Current = "none"
}
Write-Host "Current version: $Current"

# 查询最新 Release
Write-Host "Checking latest release..."
try {
    $LatestInfo = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases/latest" -ErrorAction Stop
    $Latest = $LatestInfo.tag_name
} catch {
    Write-Host "Failed to fetch latest release info." -ForegroundColor Red
    Write-Host "Check network or update `$Repo variable in this script."
    exit 1
}

Write-Host "Latest version: $Latest"

# 版本比较
if ($Current -eq $Latest) {
    Write-Host "Already up to date." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "Upgrade available: $Current → $Latest" -ForegroundColor Yellow
$Confirm = Read-Host "Proceed? [y/N]"
if ($Confirm -ne "y" -and $Confirm -ne "Y") {
    Write-Host "Upgrade cancelled."
    exit 0
}

# 执行升级
Write-Host "Pulling latest code..."
git pull origin main

Write-Host "Reinstalling dependencies..."
pip install -r requirements.txt

Write-Host ""
Write-Host "=== Upgrade complete ===" -ForegroundColor Green
Write-Host "Run 'pytest tests/ -q' to verify."
