# 批量创建 metadata.json 脚本
# 为所有技能目录自动生成 metadata.json

param(
    [string]$BasePath = "."
)

Write-Host "=== 批量创建 metadata.json ===" -ForegroundColor Green
Write-Host "基础路径: $BasePath" -ForegroundColor Cyan
Write-Host ""

# 获取所有技能目录
$skillDirs = Get-ChildItem -Path "$BasePath\skills" -Directory
Write-Host "发现 $($skillDirs.Count) 个技能目录" -ForegroundColor Yellow
Write-Host ""

$created = 0
$skipped = 0
$errors = 0

foreach ($dir in $skillDirs) {
    $skillName = $dir.Name
    $metadataPath = "$($dir.FullName)\metadata.json"
    $skillMdPath = "$($dir.FullName)\SKILL.md"
    
    # 如果已存在则跳过
    if (Test-Path $metadataPath) {
        Write-Host "  ○ 跳过 $skillName (已存在)" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    # 尝试从 SKILL.md 提取信息
    $description = "AI技能: $skillName"
    $version = "1.0.0"
    
    if (Test-Path $skillMdPath) {
        try {
            $content = Get-Content $skillMdPath -Raw -ErrorAction SilentlyContinue
            # 尝试提取 description
            if ($content -match 'description:\s*"([^"]+)"') {
                $description = $matches[1]
            } elseif ($content -match 'description:\s*([^\r\n]+)') {
                $description = $matches[1]
            }
            # 尝试提取 version
            if ($content -match 'version:\s*"?([^"\r\n]+)"?') {
                $version = $matches[1]
            }
        } catch {
            # 忽略错误，使用默认值
        }
    }
    
    # 生成 metadata.json
    $metadata = @{
        name = $skillName
        slug = $skillName
        version = $version
        description = $description
        author = "wanglin1111111"
        tags = @("ai", "skill")
        category = "other"
        stability = "stable"
        requires = @{
            bins = @()
            env = @()
            os = @("linux", "darwin", "win32")
        }
        entry = "SKILL.md"
        created_at = (Get-Date -Format "yyyy-MM-dd")
        updated_at = (Get-Date -Format "yyyy-MM-dd")
    } | ConvertTo-Json -Depth 10
    
    try {
        $metadata | Out-File -FilePath $metadataPath -Encoding UTF8
        Write-Host "  ✓ 创建 $skillName/metadata.json" -ForegroundColor Green
        $created++
    } catch {
        Write-Host "  ✗ 失败 $skillName : $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host ""
Write-Host "=== 完成 ===" -ForegroundColor Green
Write-Host "创建: $created | 跳过: $skipped | 失败: $errors" -ForegroundColor Cyan
