# 新技能创建标准

**版本**: 1.0.0  
**生效日期**: 2026-05-29  
**适用范围**: 所有新增技能

---

## 强制要求 (Must Have)

### 1. 基础文件

| 文件 | 要求 | 说明 |
|------|------|------|
| `SKILL.md` | ✅ 必须 | 主技能文档，符合模板格式 |
| `metadata.json` | ✅ 必须 | 元数据文件，包含所有必需字段 |
| `test/test_cases.md` | ✅ 必须 | 测试用例文档 |
| `example/real_world_examples.md` | ✅ 必须 | 真实示例文档 |

### 2. SKILL.md 内容要求

**必须包含的章节**:

```markdown
1. YAML Frontmatter (--- 开头)
   - name: 技能名称
   - version: 版本号
   - author: 作者
   - license: 许可证
   - description: 详细描述
   - keywords: 关键词列表
   - category: 分类

2. 标题 (# Skill Name)

3. 概述/简介章节
   - 核心理念
   - 适用场景

4. 核心内容章节 (至少3个)
   - 方法论/框架
   - 实践步骤
   - 应用案例

5. 相关技能链接
```

### 3. metadata.json 必填字段

```json
{
  "name": "技能名称",
  "version": "1.0.0",
  "author": "作者名",
  "license": "MIT",
  "description": "技能描述",
  "keywords": ["关键词1", "关键词2"],
  "category": "分类"
}
```

### 4. test/test_cases.md 要求

**最少测试用例**: 3个

**必须包含**:
- 基础功能测试
- 边界情况测试
- 集成场景测试

**格式**:
```markdown
## Test Suite: [功能名称]

### Test 1: [测试名称]
**Input**: [输入]

**Expected Output**: [预期输出]

**Validation Points**:
- [ ] 检查点1
- [ ] 检查点2
```

### 5. example/real_world_examples.md 要求

**最少示例**: 2个

**必须包含**:
- 背景描述
- 应用场景
- 具体步骤
- 结果/效果

**格式**:
```markdown
## Example 1: [示例名称]

### Background
[背景描述]

### Application
[应用过程]

### Results
[结果展示]
```

---

## 推荐要求 (Should Have)

### 6. 额外文件

| 文件 | 推荐度 | 说明 |
|------|--------|------|
| `test/README.md` | ⭐⭐⭐ | 测试说明 |
| `example/README.md` | ⭐⭐⭐ | 示例说明 |
| `CHANGELOG.md` | ⭐⭐ | 变更日志 |
| `FAQ.md` | ⭐⭐ | 常见问题 |

### 7. 内容深度

- **字数**: SKILL.md > 1000字
- **章节**: 核心章节 ≥ 3个
- **案例**: 具体案例 ≥ 2个
- **图表**: 适当使用表格/列表

---

## 质量检查清单

### 提交前自检

- [ ] `SKILL.md` 包含所有必需章节
- [ ] `metadata.json` 所有字段已填写
- [ ] `test/test_cases.md` 至少3个测试用例
- [ ] `example/real_world_examples.md` 至少2个示例
- [ ] 所有文件使用UTF-8编码
- [ ] 无拼写错误
- [ ] 相关技能链接正确

### 自动化检查

```bash
# 运行质量门禁
python scripts/quality_gate.py --check-new-skill

# 检查文件完整性
python scripts/check_skill_completeness.py
```

---

## 审核流程

### 1. 提交前

1. 使用模板创建技能
2. 填写所有必需内容
3. 运行自检清单
4. 本地测试验证

### 2. PR提交

```markdown
## 新增技能: [技能名称]

### 检查清单
- [ ] SKILL.md 符合模板
- [ ] metadata.json 完整
- [ ] test/test_cases.md 已创建 (3+测试)
- [ ] example/real_world_examples.md 已创建 (2+示例)
- [ ] 本地质量检查通过

### 技能分类
[选择分类]

### 相关技能
- [相关技能1]
- [相关技能2]
```

### 3. 审核标准

| 检查项 | 权重 | 通过标准 |
|--------|------|----------|
| 文件完整性 | 30% | 4个必需文件齐全 |
| 内容质量 | 40% | 符合深度要求 |
| 测试覆盖 | 20% | 3+测试用例 |
| 示例质量 | 10% | 2+真实示例 |

**通过分数**: ≥ 80%

---

## 模板使用

### 快速创建

```bash
# 使用脚本创建新技能
python scripts/create_new_skill.py --name [技能名] --category [分类]

# 或手动复制模板
cp -r templates/skill-template skills/[新技能名]
```

### 模板位置

- `templates/skill-template/` - 完整技能模板
- `meta/SKILL_TEMPLATE.md` - 文档模板

---

## 违规处理

### 轻微违规
- 缺少推荐文件
- 内容深度略低

**处理**: 要求补充，延迟合并

### 严重违规
- 缺少必需文件
- 无测试或示例
- 内容质量不达标

**处理**: 拒绝合并，要求重做

---

## 标准演进

### 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-05-29 | 初始标准建立 |

### 未来计划

- [ ] 增加自动化检查脚本
- [ ] 建立技能质量评分体系
- [ ] 引入同行评审机制

---

**强制执行日期**: 2026-06-01  
**适用范围**: 所有新提交技能  
**审核人**: 技能库维护团队
