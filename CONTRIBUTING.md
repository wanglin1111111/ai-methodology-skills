# CONTRIBUTING.md - AI技能贡献指南

## 如何贡献技能

### 1. 技能开发流程

```
1. Fork 仓库
2. 创建技能目录: skills/your-skill-name/
3. 编写 SKILL.md (遵循 SKILL_TEMPLATE.md)
4. 添加 metadata.json
5. 本地测试验证
6. 提交 PR
7. 代码审查
8. 合并发布
```

### 2. 技能结构要求

```
your-skill-name/
├── SKILL.md              # 必须：主文档
├── metadata.json         # 必须：机器可读元数据
├── examples/             # 推荐：使用示例
└── references/           # 可选：参考资料
```

### 3. SKILL.md 规范

参考根目录 `SKILL_TEMPLATE.md`，必须包含：
- YAML 元数据头部 (name, version, description)
- 核心概念
- 方法论框架
- 行动检查清单
- 对话模板
- 参考案例

### 4. metadata.json 规范

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "简短描述",
  "author": "你的名字",
  "tags": ["标签1", "标签2"],
  "category": "分类ID",
  "stability": "stable|beta|experimental",
  "requires": {
    "bins": [],
    "env": [],
    "os": ["linux", "darwin", "win32"]
  },
  "entry": "SKILL.md",
  "created_at": "2026-05-29",
  "updated_at": "2026-05-29"
}
```

### 5. 标签规范

参考 `skills_index.json` 中的15个分类：
- 人类价值、职业转型、专业重定义
- 品牌增长、消费市场、B2B销售
- 超级个体、创业指南、AI产品
- 内容创作、学习成长、效率工具
- 行业应用、技术实现、其他

### 6. 版本规范

遵循语义化版本（SemVer）：
- MAJOR: 不兼容的API更改
- MINOR: 向后兼容的功能添加
- PATCH: 向后兼容的问题修复

### 7. 测试要求

提交前必须：
- [ ] 技能可以被正确加载
- [ ] SKILL.md 格式正确
- [ ] metadata.json 有效
- [ ] 更新 skills_index.json

### 8. 代码审查清单

审查者将检查：
- [ ] 符合 SKILL_TEMPLATE.md 规范
- [ ] 描述清晰准确
- [ ] 边界定义明确
- [ ] 版本号正确
- [ ] 已更新索引

### 9. 更新 skills_index.json

添加新技能后，更新索引文件：
```json
{
  "total_skills": 80,
  "categories": [
    {
      "id": "XX",
      "name": "分类名",
      "count": 7
    }
  ]
}
```

### 10. 联系方式

- 问题反馈: GitHub Issues
- 讨论: GitHub Discussions

## 技能改进建议

### 如何提议改进

1. 提交 Issue，描述改进建议
2. 等待社区讨论
3. 如被接受，提交 PR 实现

### 改进类型

- **Bug 修复**: 修复现有技能的问题
- **功能增强**: 添加新功能
- **文档改进**: 改进文档质量

## 行为准则

- 尊重他人
- 建设性反馈
- 专注于技术讨论
- 遵守开源协议

---

感谢你的贡献！🎉
