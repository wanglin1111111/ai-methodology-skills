# 潜在风险扫描脚本
# 检查: 技能膨胀、版本管理、交叉链接、测试覆盖、文档一致性

Write-Host "=== AI技能库风险扫描 ===" -ForegroundColor Green
Write-Host ""

$skillPath = "skills"
if (Test-Path "core-skills") { $skillPath = "core-skills" }

$skills = Get-ChildItem -Path $skillPath -Directory
Write-Host "发现 $($skills.Count) 个技能目录" -ForegroundColor Cyan
Write-Host ""

# 1. 技能膨胀检查 - 分析技能名称相似度
Write-Host "[1/5] 技能膨胀检查..." -ForegroundColor Yellow
$similarNames = @()
$skillNames = $skills | ForEach-Object { $_.Name }

for ($i = 0; $i -lt $skillNames.Count; $i++) {
    for ($j = $i + 1; $j -lt $skillNames.Count; $j++) {
        $name1 = $skillNames[$i] -replace '-', '' -replace '_', ''
        $name2 = $skillNames[$j] -replace '-', '' -replace '_', ''
        
        # 简单相似度检查
        if ($name1 -like "*$name2*" -or $name2 -like "*$name1*") {
            if ($name1.Length -gt 5 -and $name2.Length -gt 5) {
                $similarNames += "$($skillNames[$i]) <-> $($skillNames[$j])"
            }
        }
    }
}

if ($similarNames.Count -gt 0) {
    Write-Host "  ⚠ 发现 $($similarNames.Count) 对相似技能:" -ForegroundColor Yellow
    $similarNames | Select-Object -First 10 | ForEach-Object { Write-Host "    - $_" -ForegroundColor Gray }
} else {
    Write-Host "  ✓ 未发现明显相似技能" -ForegroundColor Green
}
Write-Host ""

# 2. 版本管理检查 - 抽查10个技能
Write-Host "[2/5] 版本管理检查 (抽查10个)..." -ForegroundColor Yellow
$sampleSkills = $skills | Get-Random -Count 10
$versionIssues = @()

foreach ($skill in $sampleSkills) {
    $metadataPath = "$($skill.FullName)\metadata.json"
    if (Test-Path $metadataPath) {
        $metadata = Get-Content $metadataPath -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
        if ($metadata.version -notmatch '^\d+\.\d+\.\d+$') {
            $versionIssues += "$($skill.Name): $($metadata.version)"
        }
    } else {
        $versionIssues += "$($skill.Name): 缺少metadata.json"
    }
}

if ($versionIssues.Count -gt 0) {
    Write-Host "  ⚠ 发现 $($versionIssues.Count) 个版本问题:" -ForegroundColor Yellow
    $versionIssues | ForEach-Object { Write-Host "    - $_" -ForegroundColor Gray }
} else {
    Write-Host "  ✓ 版本格式正确" -ForegroundColor Green
}
Write-Host ""

# 3. 交叉链接检查
Write-Host "[3/5] 交叉链接检查..." -ForegroundColor Yellow
$brokenLinks = @()
$skillFiles = Get-ChildItem -Path $skillPath -Recurse -Filter "*.md"

foreach ($file in $skillFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    # 查找相对链接
    $links = [regex]::Matches($content, '\]\(([^)]+)\)') | ForEach-Object { $_.Groups[1].Value }
    
    foreach ($link in $links) {
        if ($link -match '^\.\.?\/') {
            $targetPath = Join-Path (Split-Path $file.FullName) $link
            if (-not (Test-Path $targetPath)) {
                $brokenLinks += "$($file.Name) -> $link"
            }
        }
    }
}

if ($brokenLinks.Count -gt 0) {
    Write-Host "  ⚠ 发现 $($brokenLinks.Count) 个断裂链接:" -ForegroundColor Yellow
    $brokenLinks | Select-Object -First 10 | ForEach-Object { Write-Host "    - $_" -ForegroundColor Gray }
} else {
    Write-Host "  ✓ 未发现断裂链接" -ForegroundColor Green
}
Write-Host ""

# 4. 测试覆盖率检查
Write-Host "[4/5] 测试覆盖率检查..." -ForegroundColor Yellow
$noTest = @()
$noExample = @()

foreach ($skill in $skills) {
    $testPath = "$($skill.FullName)\test"
    $examplePath = "$($skill.FullName)\example"
    
    if (-not (Test-Path $testPath)) {
        $noTest += $skill.Name
    }
    if (-not (Test-Path $examplePath)) {
        $noExample += $skill.Name
    }
}

Write-Host "  统计结果:" -ForegroundColor Cyan
Write-Host "    - 有 test/ 目录: $($skills.Count - $noTest.Count) / $($skills.Count)" -ForegroundColor White
Write-Host "    - 有 example/ 目录: $($skills.Count - $noExample.Count) / $($skills.Count)" -ForegroundColor White

if ($noTest.Count -gt 0) {
    Write-Host "  ⚠ $($noTest.Count) 个技能缺少 test/ 目录" -ForegroundColor Yellow
}
if ($noExample.Count -gt 0) {
    Write-Host "  ⚠ $($noExample.Count) 个技能缺少 example/ 目录" -ForegroundColor Yellow
}
Write-Host ""

# 5. 文档一致性抽查 - 随机5个技能
Write-Host "[5/5] 文档一致性抽查 (5个技能)..." -ForegroundColor Yellow
$sampleForCheck = $skills | Get-Random -Count 5

foreach ($skill in $sampleForCheck) {
    $skillMd = "$($skill.FullName)\SKILL.md"
    $metadataPath = "$($skill.FullName)\metadata.json"
    
    Write-Host "  检查: $($skill.Name)" -ForegroundColor Cyan
    
    if (Test-Path $skillMd) {
        $content = Get-Content $skillMd -Raw -ErrorAction SilentlyContinue
        
        # 检查关键章节
        $hasDesc = $content -match "## 描述|## 简介|## 概述"
        $hasUsage = $content -match "## 使用|## 用法|## 示例"
        $hasYaml = $content -match "^---"
        
        Write-Host "    - YAML frontmatter: $(if($hasYaml){'✓'}else{'✗'})" -ForegroundColor $(if($hasYaml){'Green'}else{'Red'})
        Write-Host "    - 描述章节: $(if($hasDesc){'✓'}else{'✗'})" -ForegroundColor $(if($hasDesc){'Green'}else{'Red'})
        Write-Host "    - 使用章节: $(if($hasUsage){'✓'}else{'✗'})" -ForegroundColor $(if($hasUsage){'Green'}else{'Red'})
    } else {
        Write-Host "    - 缺少 SKILL.md!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== 扫描完成 ===" -ForegroundColor Green

# 生成风险报告
$report = @"
# 风险扫描报告

**扫描时间**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**技能总数**: $($skills.Count)

## 风险摘要

| 检查项 | 状态 | 风险等级 |
|--------|------|----------|
| 技能膨胀 | $(if($similarNames.Count -gt 5){'⚠ 需关注'}else{'✓ 正常'}) | $(if($similarNames.Count -gt 5){'中'}else{'低'}) |
| 版本管理 | $(if($versionIssues.Count -gt 0){'⚠ 需修复'}else{'✓ 正常'}) | $(if($versionIssues.Count -gt 0){'高'}else{'低'}) |
| 交叉链接 | $(if($brokenLinks.Count -gt 0){'⚠ 需修复'}else{'✓ 正常'}) | $(if($brokenLinks.Count -gt 0){'中'}else{'低'}) |
| 测试覆盖 | ⚠ 不足 | 高 |
| 文档一致性 | 已抽查 | 中 |

## 建议行动

1. **测试覆盖**: 为 $($noTest.Count) 个技能添加 test/ 目录
2. **示例补充**: 为 $($noExample.Count) 个技能添加 example/ 目录
3. **版本规范**: 统一版本号格式为 SemVer (x.y.z)
4. **链接检查**: 定期运行交叉链接检查

"@

$report | Out-File -FilePath "RISK_SCAN_REPORT.md" -Encoding UTF8
Write-Host "报告已保存: RISK_SCAN_REPORT.md" -ForegroundColor Cyan
