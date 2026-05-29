#!/usr/bin/env python3
"""
AI技能知识库治理优化脚本
解决：命名混乱、文档质量参差、缺少标准化流程
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class SkillRepositoryOptimizer:
    def __init__(self, repo_path="C:/Users/22812/Documents/GitHub/-"):
        self.repo_path = Path(repo_path)
        self.issues = []
        self.recommendations = []
        
    def analyze_structure(self):
        """分析仓库结构"""
        print("=" * 70)
        print("AI技能知识库治理分析报告")
        print("=" * 70)
        
        # 统计目录
        skills_dir = self.repo_path / "skills"
        references_dir = self.repo_path / "references"
        
        skills_count = len(list(skills_dir.glob("*/SKILL.md"))) if skills_dir.exists() else 0
        refs_count = len(list(references_dir.glob("**/*.md"))) if references_dir.exists() else 0
        
        print(f"\n[仓库统计]")
        print(f"  - skills目录: {skills_count} 个技能")
        print(f"  - references目录: {refs_count} 个参考文件")
        print(f"  - 总计: {skills_count + refs_count} 个文档")
        
        return skills_count, refs_count
        
    def check_naming_conventions(self):
        """检查命名规范问题"""
        print(f"\n[命名规范检查]")
        
        skills_dir = self.repo_path / "skills"
        naming_issues = []
        
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    name = skill_dir.name
                    
                    # 检查是否使用kebab-case
                    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
                        naming_issues.append({
                            'path': str(skill_dir),
                            'name': name,
                            'issue': '命名格式不规范（应使用kebab-case小写）',
                            'suggestion': self.to_kebab_case(name)
                        })
                    
                    # 检查是否包含中文
                    if re.search(r'[\u4e00-\u9fff]', name):
                        naming_issues.append({
                            'path': str(skill_dir),
                            'name': name,
                            'issue': '包含中文字符',
                            'suggestion': self.to_kebab_case(name)
                        })
        
        print(f"  发现 {len(naming_issues)} 个命名问题")
        for issue in naming_issues[:5]:
            print(f"    [X] {issue['name']}")
            print(f"       建议: {issue['suggestion']}")
        
        if len(naming_issues) > 5:
            print(f"       ... 还有 {len(naming_issues) - 5} 个")
        
        return naming_issues
        
    def to_kebab_case(self, name):
        """转换为kebab-case"""
        # 替换下划线为连字符
        name = name.replace('_', '-')
        # 替换空格为连字符
        name = name.replace(' ', '-')
        # 移除特殊字符
        name = re.sub(r'[^a-zA-Z0-9\-]', '', name)
        # 转换为小写
        name = name.lower()
        # 移除连续的连字符
        name = re.sub(r'-+', '-', name)
        # 移除首尾连字符
        name = name.strip('-')
        return name
        
    def check_document_quality(self):
        """检查文档质量"""
        print(f"\n[文档质量检查]")
        
        skills_dir = self.repo_path / "skills"
        quality_issues = []
        
        required_sections = [
            'name',
            'description',
            '## ',  # 至少一个二级标题
        ]
        
        if skills_dir.exists():
            for skill_file in skills_dir.glob("*/SKILL.md"):
                content = skill_file.read_text(encoding='utf-8')
                issues = []
                
                # 检查YAML frontmatter
                if not content.startswith('---'):
                    issues.append("缺少YAML frontmatter")
                
                # 检查必需字段
                if 'name:' not in content:
                    issues.append("缺少name字段")
                if 'description:' not in content:
                    issues.append("缺少description字段")
                
                # 检查章节结构
                if '## ' not in content:
                    issues.append("缺少二级标题章节")
                
                # 检查示例
                if '```' not in content:
                    issues.append("缺少代码示例")
                
                if issues:
                    quality_issues.append({
                        'file': skill_file.name,
                        'issues': issues
                    })
        
        print(f"  发现 {len(quality_issues)} 个文档质量问题")
        for issue in quality_issues[:3]:
            print(f"    [X] {issue['file']}")
            for i in issue['issues']:
                print(f"       - {i}")
        
        return quality_issues
        
    def check_standardization(self):
        """检查标准化流程"""
        print(f"\n[标准化流程检查]")
        
        missing_standards = []
        
        # 检查必需文件
        required_files = [
            'README.md',
            'CONTRIBUTING.md',
            'SKILL_TEMPLATE.md',
            'quality_report.md',
        ]
        
        for req_file in required_files:
            if not (self.repo_path / req_file).exists():
                missing_standards.append(req_file)
        
        # 检查目录结构
        required_dirs = ['skills', 'docs', 'scripts']
        for req_dir in required_dirs:
            if not (self.repo_path / req_dir).exists():
                missing_standards.append(f"目录: {req_dir}/")
        
        print(f"  缺少 {len(missing_standards)} 个标准化元素")
        for item in missing_standards:
            print(f"    [!] {item}")
        
        return missing_standards
        
    def generate_optimization_plan(self):
        """生成优化计划"""
        print(f"\n" + "=" * 70)
        print("[治理优化方案]")
        print("=" * 70)
        
        plan = """
## Phase 1: 命名规范治理 (优先级: P0)

### 1.1 建立命名规范
```
技能目录命名规则:
- 格式: kebab-case (小写+连字符)
- 示例: content-topic-evaluator [OK]
- 反例: ContentTopicEvaluator [X], content_topic_evaluator [X]

文件命名规则:
- SKILL.md - 主技能文件 (必须)
- README.md - 项目说明 (必须)
- .gitignore - Git配置 (必须)
- examples/ - 示例目录 (可选)
```

### 1.2 批量重命名脚本
创建 rename_skills.py 自动规范化命名

## Phase 2: 质量门禁建设 (优先级: P0)

### 2.1 SKILL.md 必需字段检查清单
```yaml
---
name: skill-name                    # 必需: kebab-case命名
version: 1.0.0                     # 必需: 语义化版本
description: "描述"                # 必需: 50-200字符
display_name: "显示名称"          # 必需: 中文可读名称
aliases: [别名1, 别名2]            # 可选: 搜索关键词
stability: stable|beta|alpha     # 必需: 稳定性等级
error_handling: enabled            # 必需: 错误处理标识
last_updated: 2026-05-29          # 必需: 最后更新日期
---
```

### 2.2 必需章节结构
```markdown
# 技能标题

## 核心概念
## 方法论框架
## 行动检查清单
## 对话模板
## 参考案例
## 常见误区
## 核心结论
```

### 2.3 质量评分标准
| 维度 | 权重 | 检查项 |
|------|------|--------|
| 完整性 | 30% | 必需字段+章节齐全 |
| 实用性 | 25% | 有案例、有模板 |
| 可落地 | 20% | 有检查清单、有步骤 |
| 安全性 | 15% | 无敏感信息 |
| 规范性 | 10% | 格式统一 |

## Phase 3: 标准化流程建立 (优先级: P1)

### 3.1 技能创建流程
```
1. 需求分析 -> 确定技能定位
2. 框架设计 -> HKR/其他方法论
3. 内容编写 -> 按模板填充
4. 质量自检 -> 使用checklist
5. 同行评审 -> 至少1人review
6. 提交入库 -> PR合并
```

### 3.2 自动化工具链
- validate_skills.py - 格式验证
- quality_check.py - 质量评分
- generate_index.py - 索引生成
- add_cross_links.py - 交叉链接

### 3.3 文档模板
创建 SKILL_TEMPLATE.md 作为标准模板

## Phase 4: 持续优化 (优先级: P2)

### 4.1 定期质量审计
- 每月运行质量检查
- 生成质量报告
- 识别低质量技能

### 4.2 技能迭代机制
- 收集使用反馈
- 定期更新内容
- 版本管理

### 4.3 社区协作
- 贡献指南
- Review流程
- 奖励机制
"""
        
        print(plan)
        return plan
        
    def create_optimization_scripts(self):
        """创建优化脚本"""
        print(f"\n[创建优化脚本]")
        
        scripts_dir = self.repo_path / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        # 1. 命名规范化脚本
        naming_script = scripts_dir / "normalize_naming.py"
        naming_content = '''#!/usr/bin/env python3
"""
命名规范化脚本
将技能目录名统一转换为kebab-case
"""

import os
import re
from pathlib import Path

def to_kebab_case(name):
    """转换为kebab-case"""
    name = name.replace('_', '-').replace(' ', '-')
    name = re.sub(r'[^a-zA-Z0-9\-]', '', name)
    name = name.lower()
    name = re.sub(r'-+', '-', name).strip('-')
    return name

def normalize_skills_naming(repo_path="."):
    skills_dir = Path(repo_path) / "skills"
    
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            old_name = skill_dir.name
            new_name = to_kebab_case(old_name)
            
            if old_name != new_name:
                new_path = skill_dir.parent / new_name
                print(f"重命名: {old_name} -> {new_name}")
                skill_dir.rename(new_path)

if __name__ == "__main__":
    normalize_skills_naming()
    print("命名规范化完成!")
'''
        naming_script.write_text(naming_content, encoding='utf-8')
        print(f"  [OK] 创建: {naming_script}")
        
        # 2. 质量检查脚本
        quality_script = scripts_dir / "quality_gate.py"
        quality_content = '''#!/usr/bin/env python3
"""
质量门禁脚本
检查技能文件是否符合质量标准
"""

import re
from pathlib import Path

REQUIRED_FIELDS = ['name', 'version', 'description', 'stability']
REQUIRED_SECTIONS = ['## ', '### ']  # 至少一个二级或三级标题

def check_skill_quality(skill_file):
    """检查单个技能质量"""
    content = skill_file.read_text(encoding='utf-8')
    issues = []
    
    # 检查YAML frontmatter
    if not content.startswith('---'):
        issues.append("缺少YAML frontmatter")
    
    # 检查必需字段
    for field in REQUIRED_FIELDS:
        if f'{field}:' not in content:
            issues.append(f"缺少 {field} 字段")
    
    # 检查章节
    if not any(marker in content for marker in REQUIRED_SECTIONS):
        issues.append("缺少章节结构")
    
    return issues

def run_quality_gate(repo_path="."):
    skills_dir = Path(repo_path) / "skills"
    results = []
    
    for skill_file in skills_dir.glob("*/SKILL.md"):
        issues = check_skill_quality(skill_file)
        results.append({
            'file': str(skill_file),
            'issues': issues,
            'passed': len(issues) == 0
        })
    
    # 输出报告
    passed = sum(1 for r in results if r['passed'])
    failed = len(results) - passed
    
    print(f"质量门禁检查完成:")
    print(f"  [OK] 通过: {passed}")
    print(f"  [X] 失败: {failed}")
    
    for r in results:
        if not r['passed']:
            print(f"\\n  {r['file']}")
            for issue in r['issues']:
                print(f"    - {issue}")

if __name__ == "__main__":
    run_quality_gate()
'''
        quality_script.write_text(quality_content, encoding='utf-8')
        print(f"  [OK] 创建: {quality_script}")
        
        # 3. 创建标准模板
        template_file = self.repo_path / "SKILL_TEMPLATE.md"
        template_content = '''---
name: skill-name-example
version: 1.0.0
description: "技能描述，50-200字符，说明核心能力和适用场景"
display_name: "技能显示名称"
aliases: [别名1, 别名2, 关键词]
stability: stable
error_handling: enabled
last_updated: 2026-05-29
---

# 技能标题

> 核心理念：一句话概括技能核心思想

## 核心概念

### 概念A
- 要点1
- 要点2
- 要点3

### 概念B
- 要点1
- 要点2

## 方法论框架

### 框架名称

```
核心公式 = 要素A x 要素B x 要素C
```

| 维度 | 说明 | 权重 |
|------|------|------|
| 要素A | 说明 | 33% |
| 要素B | 说明 | 33% |
| 要素C | 说明 | 33% |

## 行动检查清单

- [ ] 检查项1
- [ ] 检查项2
- [ ] 检查项3

## 对话模板

**用户输入**:
"用户问题示例"

**系统输出**:
```
结构化回复示例
```

## 参考案例

### 案例1：场景描述
**背景**: 背景说明
**过程**: 执行步骤
**结果**: 最终效果

## 常见误区

| 误区 | 正确做法 |
|------|---------|
| 错误认知1 | 正确认知1 |
| 错误认知2 | 正确认知2 |

## 核心结论

> 关键洞察1

> 关键洞察2

## 核心公式

```
成功 = 要素A x 要素B x 要素C
```

## 更新日志

### v1.0.0 (2026-05-29)
- [+] 初始版本发布
- [+] 核心功能1
- [+] 核心功能2
'''
        template_file.write_text(template_content, encoding='utf-8')
        print(f"  [OK] 创建: {template_file}")
        
        return True
        
    def generate_report(self):
        """生成完整报告"""
        print(f"\n" + "=" * 70)
        print("[治理优化完成]")
        print("=" * 70)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'repository': str(self.repo_path),
            'phases': [
                {
                    'name': 'Phase 1: 命名规范治理',
                    'priority': 'P0',
                    'status': '脚本已创建',
                    'action': '运行 scripts/normalize_naming.py'
                },
                {
                    'name': 'Phase 2: 质量门禁建设',
                    'priority': 'P0',
                    'status': '脚本已创建',
                    'action': '运行 scripts/quality_gate.py'
                },
                {
                    'name': 'Phase 3: 标准化流程',
                    'priority': 'P1',
                    'status': '模板已创建',
                    'action': '使用 SKILL_TEMPLATE.md'
                },
                {
                    'name': 'Phase 4: 持续优化',
                    'priority': 'P2',
                    'status': '待实施',
                    'action': '建立定期审计机制'
                }
            ],
            'created_files': [
                'scripts/normalize_naming.py',
                'scripts/quality_gate.py',
                'SKILL_TEMPLATE.md'
            ]
        }
        
        # 保存报告
        report_file = self.repo_path / "governance_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n[已创建优化文件]")
        for f in report['created_files']:
            print(f"  [OK] {f}")
        
        print(f"\n[治理报告] {report_file}")
        
        print(f"\n[下一步行动]")
        print(f"  1. 运行: python scripts/normalize_naming.py")
        print(f"  2. 运行: python scripts/quality_gate.py")
        print(f"  3. 使用 SKILL_TEMPLATE.md 创建新技能")
        print(f"  4. 提交并推送优化结果")
        
        return report

def main():
    optimizer = SkillRepositoryOptimizer()
    
    # 分析现状
    skills_count, refs_count = optimizer.analyze_structure()
    naming_issues = optimizer.check_naming_conventions()
    quality_issues = optimizer.check_document_quality()
    missing_standards = optimizer.check_standardization()
    
    # 生成优化方案
    optimization_plan = optimizer.generate_optimization_plan()
    
    # 创建优化脚本
    optimizer.create_optimization_scripts()
    
    # 生成报告
    report = optimizer.generate_report()
    
    print(f"\n" + "=" * 70)
    print("[OK] AI技能知识库治理优化完成!")
    print("=" * 70)

if __name__ == "__main__":
    main()
