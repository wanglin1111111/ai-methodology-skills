# 批量创建 metadata.json
param([string]$BasePath = ".")

Write-Host "=== 批量创建 metadata.json ==="
Write-Host "基础路径: $BasePath"

$skillDirs = Get-ChildItem -Path "$BasePath\skills" -Directory
Write-Host "发现 $($skillDirs.Count) 个技能目录"

$created = 0

foreach ($dir in $skillDirs) {
    $skillName = $dir.Name
    $metadataPath = "$($dir.FullName)\metadata.json"
    
    if (Test-Path $metadataPath) {
        Write-Host "跳过: $skillName (已存在)"
        continue
    }
    
    $metadata = @{
        name = $skillName
        version = "1.0.0"
        description = "AI skill: $skillName"
        author = "wanglin1111111"
        tags = @("ai", "skill")
        category = "other"
        stability = "stable"
        entry = "SKILL.md"
        created_at = "2026-05-29"
        updated_at = "2026-05-29"
    } | ConvertTo-Json
    
    $metadata | Out-File -FilePath $metadataPath -Encoding UTF8
    Write-Host "创建: $skillName/metadata.json"
    $created++
}

Write-Host "=== 完成 ==="
Write-Host "创建: $created 个 metadata.json"
