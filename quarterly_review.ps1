# 季度技能审查脚本
# 每季度运行一次，检查技能相似度和质量

param(
    [string]$ReportPath = "QUARTERLY_REVIEW_REPORT.md",
    [int]$SimilarityThreshold = 60  # 相似度阈值，超过则建议合并
)

Write-Host "=== Quarterly Skill Review ===" -ForegroundColor Green
Write-Host "Date: $(Get-Date -Format 'yyyy-MM-dd')" -ForegroundColor Cyan
Write-Host ""

$skillPath = "skills"
if (Test-Path "core-skills") { $skillPath = "core-skills" }

$skills = Get-ChildItem -Path $skillPath -Directory
$totalSkills = $skills.Count

Write-Host "Total skills: $totalSkills" -ForegroundColor Cyan
Write-Host ""

# 1. 技能数量趋势
Write-Host "[1/5] Skill Count Analysis..." -ForegroundColor Yellow

$lastQuarterCount = 87  # 上季度数量，应从历史记录读取
$countChange = $totalSkills - $lastQuarterCount

Write-Host "  Current: $totalSkills" -ForegroundColor White
Write-Host "  Last quarter: $lastQuarterCount" -ForegroundColor White
Write-Host "  Change: $countChange" -ForegroundColor $(if($countChange -gt 0){'Red'}else{'Green'})
Write-Host ""

# 2. 相似度分析
Write-Host "[2/5] Similarity Analysis..." -ForegroundColor Yellow

$similarGroups = @()
$skillNames = $skills | ForEach-Object { $_.Name }

# 按前缀分组
$prefixGroups = @{}
foreach ($name in $skillNames) {
    # 提取前缀 (ai-era-, personal-, etc.)
    if ($name -match '^([a-z]+-)+') {
        $prefix = $matches[0]
        if (-not $prefixGroups.ContainsKey($prefix)) {
            $prefixGroups[$prefix] = @()
        }
        $prefixGroups[$prefix] += $name
    }
}

# 识别高相似度组
$highSimilarityGroups = @()
foreach ($prefix in $prefixGroups.Keys) {
    $group = $prefixGroups[$prefix]
    if ($group.Count -ge 3) {
        $highSimilarityGroups += @{
            Prefix = $prefix
            Count = $group.Count
            Skills = $group
            Suggestion = "Consider merging into $($group.Count / 2) comprehensive skills"
        }
    }
}

Write-Host "  High similarity groups found: $($highSimilarityGroups.Count)" -ForegroundColor Cyan
foreach ($group in $highSimilarityGroups) {
    Write-Host "    - $($group.Prefix): $($group.Count) skills" -ForegroundColor Yellow
}
Write-Host ""

# 3. 质量检查
Write-Host "[3/5] Quality Check..." -ForegroundColor Yellow

$qualityIssues = @()
$skillsWithTests = 0
$skillsWithExamples = 0
$skillsComplete = 0

foreach ($skill in $skills) {
    $hasTest = Test-Path "$($skill.FullName)\test\test_cases.md"
    $hasExample = Test-Path "$($skill.FullName)\example\real_world_examples.md"
    $hasMetadata = Test-Path "$($skill.FullName)\metadata.json"
    
    if ($hasTest) { $skillsWithTests++ }
    if ($hasExample) { $skillsWithExamples++ }
    if ($hasTest -and $hasExample -and $hasMetadata) { $skillsComplete++ }
    
    if (-not $hasTest -or -not $hasExample) {
        $qualityIssues += @{
            Skill = $skill.Name
            MissingTest = -not $hasTest
            MissingExample = -not $hasExample
        }
    }
}

Write-Host "  Skills with tests: $skillsWithTests/$totalSkills ($([math]::Round($skillsWithTests/$totalSkills*100,1))%)" -ForegroundColor White
Write-Host "  Skills with examples: $skillsWithExamples/$totalSkills ($([math]::Round($skillsWithExamples/$totalSkills*100,1))%)" -ForegroundColor White
Write-Host "  Complete skills: $skillsComplete/$totalSkills ($([math]::Round($skillsComplete/$totalSkills*100,1))%)" -ForegroundColor White
Write-Host "  Quality issues: $($qualityIssues.Count)" -ForegroundColor $(if($qualityIssues.Count -gt 0){'Yellow'}else{'Green'})
Write-Host ""

# 4. 分类分布
Write-Host "[4/5] Category Distribution..." -ForegroundColor Yellow

$categories = @{}
foreach ($skill in $skills) {
    $metadataPath = "$($skill.FullName)\metadata.json"
    if (Test-Path $metadataPath) {
        $metadata = Get-Content $metadataPath -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
        $category = $metadata.category
        if ($category) {
            if (-not $categories.ContainsKey($category)) {
                $categories[$category] = 0
            }
            $categories[$category]++
        }
    }
}

Write-Host "  Categories: $($categories.Count)" -ForegroundColor Cyan
$categories.GetEnumerator() | Sort-Object Value -Descending | ForEach-Object {
    Write-Host "    - $($_.Key): $($_.Value) skills" -ForegroundColor White
}
Write-Host ""

# 5. 行动建议
Write-Host "[5/5] Action Items..." -ForegroundColor Yellow

$actionItems = @()

# 合并建议
if ($highSimilarityGroups.Count -gt 0) {
    $actionItems += "Review $($highSimilarityGroups.Count) skill groups for potential merging"
}

# 质量改进
if ($qualityIssues.Count -gt 0) {
    $actionItems += "Add tests/examples to $($qualityIssues.Count) incomplete skills"
}

# 数量控制
if ($totalSkills -gt 80) {
    $actionItems += "Consider skill consolidation (current: $totalSkills, target: <80)"
}

if ($actionItems.Count -eq 0) {
    $actionItems += "No immediate action required - maintain current standards"
}

$actionItems | ForEach-Object { Write-Host "  - $_" -ForegroundColor Cyan }
Write-Host ""

# 生成报告
Write-Host "Generating report..." -ForegroundColor Yellow

$report = @"
# Quarterly Skill Review Report

**Review Date**: $(Get-Date -Format 'yyyy-MM-dd')
**Quarter**: Q$([math]::Ceiling((Get-Date).Month / 3)) $(Get-Date -Format 'yyyy')
**Total Skills**: $totalSkills

---

## Executive Summary

| Metric | Value | Status |
|--------|-------|--------|
| Total Skills | $totalSkills | $(if($totalSkills -gt 80){'⚠ Review needed'}else{'✓ OK'}) |
| Skills with Tests | $skillsWithTests ($([math]::Round($skillsWithTests/$totalSkills*100,1))%) | $(if($skillsWithTests/$totalSkills -lt 0.5){'⚠ Low'}else{'✓ OK'}) |
| Skills with Examples | $skillsWithExamples ($([math]::Round($skillsWithExamples/$totalSkills*100,1))%) | $(if($skillsWithExamples/$totalSkills -lt 0.5){'⚠ Low'}else{'✓ OK'}) |
| Complete Skills | $skillsComplete ($([math]::Round($skillsComplete/$totalSkills*100,1))%) | $(if($skillsComplete/$totalSkills -lt 0.5){'⚠ Low'}else{'✓ OK'}) |
| Similarity Groups | $($highSimilarityGroups.Count) | $(if($highSimilarityGroups.Count -gt 0){'⚠ Review needed'}else{'✓ OK'}) |

---

## 1. Skill Count Trend

- **Current**: $totalSkills
- **Last Quarter**: $lastQuarterCount
- **Change**: $countChange ($(if($countChange -gt 0){'+'}else{''})$([math]::Round($countChange/$lastQuarterCount*100,1))%)

$(if($countChange -gt 5){'⚠ **Warning**: Significant increase in skill count. Consider consolidation.'}else{'✓ **Status**: Skill count change within normal range.'})

---

## 2. Similarity Analysis

$(if($highSimilarityGroups.Count -eq 0){'No high-similarity skill groups identified.'}else{"### Groups Requiring Review

| Prefix | Count | Skills | Suggestion |
|--------|-------|--------|------------|"})

$(foreach($group in $highSimilarityGroups){"| $($group.Prefix) | $($group.Count) | $($group.Skills -join ', ') | $($group.Suggestion) |"})

$(if($highSimilarityGroups.Count -gt 0){"**Recommendation**: Review these groups for potential merging to reduce maintenance overhead."})

---

## 3. Quality Metrics

### Coverage

| Requirement | Count | Percentage | Status |
|-------------|-------|------------|--------|
| Has Tests | $skillsWithTests | $([math]::Round($skillsWithTests/$totalSkills*100,1))% | $(if($skillsWithTests/$totalSkills -ge 0.8){'✓'}elseif($skillsWithTests/$totalSkills -ge 0.5){'⚠'}else{'❌'}) |
| Has Examples | $skillsWithExamples | $([math]::Round($skillsWithExamples/$totalSkills*100,1))% | $(if($skillsWithExamples/$totalSkills -ge 0.8){'✓'}elseif($skillsWithExamples/$totalSkills -ge 0.5){'⚠'}else{'❌'}) |
| Complete | $skillsComplete | $([math]::Round($skillsComplete/$totalSkills*100,1))% | $(if($skillsComplete/$totalSkills -ge 0.8){'✓'}elseif($skillsComplete/$totalSkills -ge 0.5){'⚠'}else{'❌'}) |

### Skills Needing Attention

$(if($qualityIssues.Count -eq 0){'All skills meet quality standards! 🎉'}else{"| Skill | Missing Test | Missing Example |
|-------|-------------|-----------------|
$(foreach($issue in $qualityIssues | Select-Object -First 20){"| $($issue.Skill) | $(if($issue.MissingTest){'❌'}else{'✓'}) | $(if($issue.MissingExample){'❌'}else{'✓'}) |"})"})

$(if($qualityIssues.Count -gt 20){"... and $($qualityIssues.Count - 20) more skills"})

---

## 4. Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
$(foreach($cat in $categories.GetEnumerator() | Sort-Object Value -Descending){"| $($cat.Key) | $($cat.Value) | $([math]::Round($cat.Value/$totalSkills*100,1))% |"})

---

## 5. Action Items

$(if($actionItems.Count -eq 0){'No action items for this quarter.'}else{$actionItems | ForEach-Object { "- [ ] $_" }})

---

## Next Review

**Scheduled**: $((Get-Date).AddMonths(3).ToString('yyyy-MM-dd'))

**Focus Areas**:
1. Skill consolidation progress
2. Quality coverage improvement
3. New skill standard compliance

---

*Generated by quarterly_review.ps1*
"@

$report | Out-File -FilePath $ReportPath -Encoding UTF8

Write-Host "Report saved: $ReportPath" -ForegroundColor Green
Write-Host ""
Write-Host "=== Review Complete ===" -ForegroundColor Green

# 输出关键指标
Write-Host ""
Write-Host "Key Metrics:" -ForegroundColor Cyan
Write-Host "  Skills: $totalSkills" -ForegroundColor White
Write-Host "  Complete: $skillsComplete ($([math]::Round($skillsComplete/$totalSkills*100,1))%)" -ForegroundColor White
Write-Host "  Issues: $($qualityIssues.Count)" -ForegroundColor $(if($qualityIssues.Count -gt 0){'Yellow'}else{'Green'})
