# 批量修复质量门禁问题
# 主要修复: 添加 stability 字段到所有技能文件

param(
    [string]$SkillsPath = "skills",
    [string]$StabilityValue = "stable"
)

Write-Host "=== Fixing Quality Gate Issues ===" -ForegroundColor Green
Write-Host "Target: Add 'stability' field to all SKILL.md files" -ForegroundColor Cyan
Write-Host ""

$skills = Get-ChildItem -Path $SkillsPath -Directory
$fixedCount = 0
$errorCount = 0

foreach ($skill in $skills) {
    $skillMdPath = Join-Path $skill.FullName "SKILL.md"
    
    if (-not (Test-Path $skillMdPath)) {
        Write-Host "[SKIP] $($skill.Name): SKILL.md not found" -ForegroundColor Yellow
        continue
    }
    
    try {
        $content = Get-Content $skillMdPath -Raw -Encoding UTF8
        
        # 检查是否已有 stability 字段
        if ($content -match '^stability:') {
            Write-Host "[OK] $($skill.Name): Already has stability field" -ForegroundColor Gray
            continue
        }
        
        # 在 YAML frontmatter 中添加 stability 字段
        # 找到 category: 行，在其后添加 stability
        if ($content -match '^(category:\s*.+)$') {
            $categoryLine = $matches[0]
            $newContent = $content -replace [regex]::Escape($categoryLine), "$categoryLine`nstability: $StabilityValue"
            
            # 保存修改
            $newContent | Out-File -FilePath $skillMdPath -Encoding UTF8 -NoNewline
            $fixedCount++
            Write-Host "[FIXED] $($skill.Name): Added stability field" -ForegroundColor Green
        }
        else {
            Write-Host "[WARN] $($skill.Name): Could not find category field" -ForegroundColor Yellow
        }
    }
    catch {
        $errorCount++
        Write-Host "[ERROR] $($skill.Name): $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Green
Write-Host "Fixed: $fixedCount" -ForegroundColor Green
Write-Host "Errors: $errorCount" -ForegroundColor $(if($errorCount -gt 0){'Red'}else{'Green'})
Write-Host ""

# 运行质量门禁检查修复结果
Write-Host "Running quality gate check..." -ForegroundColor Yellow
python scripts/quality_gate.py
