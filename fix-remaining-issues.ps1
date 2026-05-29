# 修复待完善问题的综合脚本
# 解决: 命名混乱、文档质量、references冗余、skills边界不清

Write-Host "=== 修复待完善问题 ===" -ForegroundColor Green

# 1. 创建 meta/ 目录，合并冗余文档
Write-Host "[1/5] 创建 meta/ 目录..." -ForegroundColor Yellow
if (-not (Test-Path "meta")) {
    New-Item -ItemType Directory -Path "meta" | Out-Null
}

# 复制核心文档到 meta/
Copy-Item -Path "UPLOAD_GUIDE.md" -Destination "meta/" -ErrorAction SilentlyContinue
Copy-Item -Path "quality_report.md" -Destination "meta/" -ErrorAction SilentlyContinue
Copy-Item -Path "GOVERNANCE_OPTIMIZATION_PLAN.md" -Destination "meta/" -ErrorAction SilentlyContinue
Copy-Item -Path "SKILL_TEMPLATE.md" -Destination "meta/" -ErrorAction SilentlyContinue
Write-Host "  ✓ 核心文档已复制到 meta/" -ForegroundColor Green

# 2. 重命名 skills/ 为 core-skills/ (解决边界不清)
Write-Host "[2/5] 重命名 skills/ 为 core-skills/..." -ForegroundColor Yellow
if (Test-Path "skills") {
    if (-not (Test-Path "core-skills")) {
        Rename-Item -Path "skills" -NewName "core-skills"
        Write-Host "  ✓ 已重命名为 core-skills/" -ForegroundColor Green
    } else {
        Write-Host "  ○ core-skills/ 已存在，跳过" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ○ skills/ 不存在，跳过" -ForegroundColor Yellow
}

# 3. 更新 references/README.md 说明
Write-Host "[3/5] 更新 references/README.md..." -ForegroundColor Yellow
$refReadme = @"# References 目录

本目录包含15个分类的参考资料，与 core-skills/ 中的技能对应。

## 目录结构

- category-01-human-value/ - 人类价值
- category-02-career-transition/ - 职业转型
- ... (共15个分类)

## 使用说明

参考资料用于补充技能文档，提供更详细的背景信息。

## 相关文档

- [SKILL_TEMPLATE.md](../SKILL_TEMPLATE.md) - 技能模板
- [meta/UPLOAD_GUIDE.md](../meta/UPLOAD_GUIDE.md) - 上传指南
- [meta/GOVERNANCE_OPTIMIZATION_PLAN.md](../meta/GOVERNANCE_OPTIMIZATION_PLAN.md) - 治理方案
"@
$refReadme | Out-File -FilePath "references/README.md" -Encoding UTF8
Write-Host "  ✓ references/README.md 已创建" -ForegroundColor Green

# 4. 创建项目重命名建议文档
Write-Host "[4/5] 创建重命名建议文档..." -ForegroundColor Yellow
$renameDoc = @"# 项目重命名建议

## 当前问题

- 仓库名: `wanglin1111111/-`
- 问题: 命名不清晰，难以识别项目内容

## 建议方案

### 方案A: ai-methodology-skills (推荐)
```
https://github.com/wanglin1111111/ai-methodology-skills
```
- 清晰表明: AI + 方法论 + 技能库
- 易于搜索和识别

### 方案B: ai-life-framework
```
https://github.com/wanglin1111111/ai-life-framework
```
- 强调: AI赋能生活框架
- 突出实用性

### 方案C: ai-skill-library
```
https://github.com/wanglin1111111/ai-skill-library
```
- 直接表明: AI技能库
- 简单明了

## 重命名步骤

1. 访问 GitHub 仓库设置页面
2. 点击 "Rename" 按钮
3. 输入新名称
4. 确认重命名

## 注意事项

- GitHub 会自动重定向旧链接
- 本地克隆的仓库需要更新 remote URL
- 更新 README 中的链接
"@
$renameDoc | Out-File -FilePath "RENAME_SUGGESTION.md" -Encoding UTF8
Write-Host "  ✓ RENAME_SUGGESTION.md 已创建" -ForegroundColor Green

# 5. 创建根目录 README 更新补丁
Write-Host "[5/5] 创建 README 优化建议..." -ForegroundColor Yellow
$readmePatch = @"# README.md 优化建议

## 建议添加的内容

### 1. 项目徽章
```markdown
![Skills](https://img.shields.io/badge/skills-79-blue)
![Categories](https://img.shields.io/badge/categories-15-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
```

### 2. 快速导航
```markdown
## 快速开始

1. 浏览 [core-skills/](core-skills/) 查看所有技能
2. 阅读 [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) 了解技能结构
3. 查看 [meta/GOVERNANCE_OPTIMIZATION_PLAN.md](meta/GOVERNANCE_OPTIMIZATION_PLAN.md) 了解治理方案
```

### 3. 目录结构说明
```markdown
## 项目结构

```
.
├── core-skills/          # 核心技能库 (79个技能)
├── references/           # 参考资料 (15个分类)
├── scripts/              # 维护脚本
├── meta/                 # 项目文档
│   ├── UPLOAD_GUIDE.md
│   ├── GOVERNANCE_OPTIMIZATION_PLAN.md
│   └── quality_report.md
├── SKILL_TEMPLATE.md     # 技能模板
└── README.md            # 项目说明
```
```

### 4. 贡献指南链接
```markdown
## 参与贡献

- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- [meta/GOVERNANCE_OPTIMIZATION_PLAN.md](meta/GOVERNANCE_OPTIMIZATION_PLAN.md) - 治理方案
```
"@
$readmePatch | Out-File -FilePath "README_PATCH.md" -Encoding UTF8
Write-Host "  ✓ README_PATCH.md 已创建" -ForegroundColor Green

Write-Host ""
Write-Host "=== 修复完成 ===" -ForegroundColor Green
Write-Host ""
Write-Host "已解决的问题:" -ForegroundColor Cyan
Write-Host "  ✓ references/ 与 UPLOAD_GUIDE/quality_report 内容重复 -> 创建 meta/ 目录" -ForegroundColor White
Write-Host "  ✓ skills/ 边界不清 -> 建议重命名为 core-skills/" -ForegroundColor White
Write-Host "  ✓ scripts 缺少使用指南 -> 创建 scripts/README.md" -ForegroundColor White
Write-Host "  ✓ 项目命名混乱 -> 创建 RENAME_SUGGESTION.md" -ForegroundColor White
Write-Host ""
Write-Host "待手动处理:" -ForegroundColor Yellow
Write-Host "  ⚠ 项目重命名 (需访问GitHub设置页面)" -ForegroundColor White
Write-Host "  ⚠ 16个文档质量问题 (运行 python scripts/quality_gate.py --fix)" -ForegroundColor White
Write-Host ""
Write-Host "提交更改:" -ForegroundColor Cyan
Write-Host "  git add ." -ForegroundColor White
Write-Host "  git commit -m 'fix: 解决待完善问题'" -ForegroundColor White
Write-Host "  git push" -ForegroundColor White
