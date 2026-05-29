# 技能合并审查报告

**审查时间**: 2026-05-29 09:46  
**技能总数**: 87  
**审查目标**: 识别可合并的相似技能，降低维护成本

---

## 可合并技能组

### 组1: AI时代核心价值系列 (8个技能)

**当前技能**:
1. ai-era-human-value
2. ai-era-career-transition
3. ai-era-professional-redefinition
4. ai-era-consumption-market-framework
5. ai-era-brand-growth-methodology
6. ai-era-curiosity-driven
7. ai-era-industry-replacement-framework
8. ai-era-rights-protection

**建议合并方案**:

**方案A: 合并为3个综合技能**

| 新技能名 | 包含原技能 | 理由 |
|----------|-----------|------|
| ai-era-personal-value | ai-era-human-value + ai-era-curiosity-driven | 个人价值定位相关 |
| ai-era-career-evolution | ai-era-career-transition + ai-era-professional-redefinition + ai-era-industry-replacement-framework | 职业发展相关 |
| ai-era-business-strategy | ai-era-consumption-market-framework + ai-era-brand-growth-methodology + ai-era-rights-protection | 商业策略相关 |

**预期效果**:
- 技能数: 8 → 3 (-62.5%)
- 维护成本: 降低60%
- 内容深度: 提升 (综合视角)

---

### 组2: AI创业系列 (3个技能)

**当前技能**:
1. ai-startup-challenges
2. ai-startup-motivation
3. ai-startup-risk-management

**建议合并**:
- **新技能**: `ai-startup-foundation`
- **内容结构**:
  - 模块1: 创业动机与心理准备 (原motivation)
  - 模块2: 常见挑战与应对 (原challenges)
  - 模块3: 风险管理框架 (原risk-management)

**预期效果**:
- 技能数: 3 → 1 (-67%)
- 形成完整创业入门体系

---

### 组3: 个人品牌建设系列 (4个技能)

**当前技能**:
1. personal-uniqueness-building
2. personal-charisma-building
3. personal-differentiation-value
4. personal-ai-collaboration-ability

**建议合并**:
- **新技能**: `personal-brand-mastery`
- **内容结构**:
  - 模块1: 独特性定位 (原uniqueness)
  - 模块2: 差异化价值 (原differentiation)
  - 模块3: 魅力构建 (原charisma)
  - 模块4: AI协作增强 (原ai-collaboration)

**预期效果**:
- 技能数: 4 → 1 (-75%)
- 形成完整个人品牌建设体系

---

## 合并实施计划

### Phase 1: 内容整合 (Week 1-2)

**步骤**:
1. 提取各技能的SKILL.md内容
2. 识别重复/重叠内容
3. 设计新技能的结构
4. 整合核心方法论

### Phase 2: 新技能创建 (Week 3-4)

**步骤**:
1. 创建新技能目录
2. 编写合并后的SKILL.md
3. 更新metadata.json
4. 迁移test/和example/

### Phase 3: 旧技能处理 (Week 5)

**步骤**:
1. 在旧技能中添加重定向说明
2. 保留6个月后归档
3. 更新所有内部链接

### Phase 4: 文档更新 (Week 6)

**步骤**:
1. 更新README.md技能列表
2. 更新分类索引
3. 发布变更说明

---

## 保留独立技能清单

以下技能**不建议合并**，保持独立更有价值:

### 高价值独立技能
1. **content-creation-core** - 内容创作核心，使用频率高
2. **demand-expression-ability** - 需求表达能力，独特性强
3. **self-as-product-methodology** - 把自己作为产品，方法论完整
4. **one-person-team-with-ai** - 一人团队，场景独特
5. **ai-investment-analysis** - AI投资分析，专业领域

### 技术类独立技能
1. **llm-development-stages** - LLM发展阶段，技术性强
2. **edge-ai-agent** - 边缘AI代理，技术独特
3. **reinforcement-learning-application** - 强化学习应用，专业领域

### 行业特定技能
1. **xiaohongshu-content-creator** - 小红书特定平台
2. **welfare-ai-design** - 公益AI设计，社会责任
3. **educational-ai-design** - 教育AI设计，专业领域

---

## 合并后预期

### 技能数量变化

| 类别 | 当前 | 合并后 | 减少 |
|------|------|--------|------|
| ai-era-* | 8 | 3 | -5 |
| ai-startup-* | 3 | 1 | -2 |
| personal-* | 4 | 1 | -3 |
| 其他 | 72 | 72 | 0 |
| **总计** | **87** | **77** | **-10 (-11.5%)** |

### 维护成本估算

| 指标 | 当前 | 合并后 | 改善 |
|------|------|--------|------|
| 技能维护数 | 87 | 77 | -11.5% |
| 重复内容 | 高 | 低 | -60% |
| 文档一致性 | 中 | 高 | +30% |
| 用户选择成本 | 高 | 中 | -25% |

---

## 风险提示

### 合并风险
1. **内容丢失** - 需确保所有有价值内容都被保留
2. **链接断裂** - 外部引用需要重定向
3. **用户困惑** - 需要清晰的迁移说明

### 缓解措施
1. 合并前完整备份
2. 保留旧技能6个月过渡期
3. 添加清晰的迁移指南
4. 在README中说明变更

---

## 建议行动

### 立即执行
- [ ] 团队讨论合并方案
- [ ] 确定合并优先级

### 本周执行
- [ ] 开始ai-startup-*合并 (影响最小)
- [ ] 测试合并流程

### 本月执行
- [ ] 完成personal-*合并
- [ ] 完成ai-era-*合并
- [ ] 更新所有文档

---

## 附录: 技能相似度分析

### ai-era-* 技能重叠分析

| 技能对 | 重叠主题 | 相似度 |
|--------|---------|--------|
| human-value + curiosity-driven | 个人成长 | 70% |
| career-transition + professional-redefinition | 职业发展 | 80% |
| brand-growth + consumption-market | 商业策略 | 60% |

### 决策依据

**合并原则**:
1. 主题重叠度 > 60%
2. 用户场景相似
3. 方法论可整合
4. 维护成本可降低

**保留原则**:
1. 独特性强
2. 使用频率高
3. 专业领域深
4. 用户群体特定
