# AI技能库使用文档

## 概述

本仓库包含79个AI技能文档，涵盖15个类别，帮助用户在AI时代提升个人价值、职业能力和创业技能。

## 目录结构

```
references/
├── README.md                          # 技能总览
├── ai-era-human-value.md              # AI时代人类价值
├── category-01-human-value/           # 类别1: 人类价值
├── category-02-career-transition/     # 类别2: 职业转型
├── category-03-professional-redefinition/  # 类别3: 专业重定义
├── category-04-brand-growth/          # 类别4: 品牌增长
├── category-05-consumption-market/      # 类别5: 消费市场
├── category-06-ai-companion/            # 类别6: AI陪伴
├── category-07-digital-ip/              # 类别7: 数字IP
├── category-08-industry-competition/    # 类别8: 行业竞争
├── category-09-embodied-ai/             # 类别9: 具身智能
├── category-10-llm-tech/                # 类别10: LLM技术
├── category-11-startup/                 # 类别11: 创业
├── category-12-core-methodology/        # 类别12: 核心方法论
├── category-13-app-design/              # 类别13: 应用设计
├── category-14-community/               # 类别14: 社区
└── category-15-industry-analysis/       # 类别15: 行业分析
```

## 快速入门

### 1. 浏览技能

每个技能文档包含：
- **描述**: 技能的核心概念
- **功能**: 技能的具体能力
- **使用场景**: 适用情境
- **工具**: 可用工具列表
- **示例**: 实际使用示例

### 2. 查找技能

使用 `skills_index.json` 快速索引：
```json
{
  "skills": [
    {
      "name": "AI时代人类价值",
      "file": "ai-era-human-value.md",
      "category": "人类价值",
      "tags": ["价值", "AI时代", "个人发展"]
    }
  ]
}
```

### 3. 使用技能

阅读技能文档后，根据示例和指南实践应用。

## 使用示例

### 示例1: 职业转型

**场景**: 从传统行业转向AI相关领域

**步骤**:
1. 阅读 `category-02-career-transition/ai-era-career-transition.md`
2. 了解AI替代边界 (`ai-replacement-boundary.md`)
3. 学习AI工具人机共生 (`ai-tool-human-symbiosis.md`)
4. 掌握内容创作核心 (`content-creation-core.md`)

### 示例2: 创业准备

**场景**: 启动AI创业项目

**步骤**:
1. 阅读 `category-11-startup/ai-startup-challenges.md`
2. 了解创业动机 (`ai-startup-motivation.md`)
3. 学习风险管理 (`ai-startup-risk-management.md`)
4. 掌握创始人行动指南 (`founder-action-guide.md`)

### 示例3: 品牌增长

**场景**: 使用AI提升品牌影响力

**步骤**:
1. 阅读 `category-04-brand-growth/ai-era-brand-growth-methodology.md`
2. 学习AI营销效率方法论 (`ai-marketing-efficiency-methodology.md`)
3. 了解品牌数据平台建设 (`brand-data-platform-construction.md`)

## 高级功能

### 1. 技能关系图谱

查看 `skills_relationship.mmd` 了解技能间的关联：
- 依赖关系
- 进阶路径
- 组合应用

### 2. 自动验证

运行 `validate_skills.py` 检查技能文档质量：
```bash
python validate_skills.py
```

### 3. 质量报告

查看 `quality_report.md` 了解技能库质量状况：
- 文档完整性
- 格式规范性
- 内容覆盖率

## 贡献指南

### 添加新技能

1. 在对应类别目录创建 `.md` 文件
2. 遵循文档格式规范
3. 更新 `skills_index.json`
4. 运行验证脚本
5. 提交PR

### 格式规范

每个技能文档必须包含：
```markdown
# 技能名称

## 描述
简要描述技能的核心概念。

## 功能
- 功能1
- 功能2

## 使用场景
- 场景1
- 场景2

## 工具
- `tool-name`: 工具描述

## 示例
使用示例代码或步骤。
```

## 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-05-27 | 1.0.0 | 初始发布，79个技能 |

## 联系方式

- 仓库: https://github.com/wanglin1111111/-
- 作者: wanglin1111111

---

**开始使用**: 从 `references/README.md` 开始探索AI技能库！
