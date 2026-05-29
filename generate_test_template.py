#!/usr/bin/env python3
"""
批量生成技能测试模板
为没有测试的技能生成基础测试用例
"""

import os
import re
from pathlib import Path

def extract_skill_info(skill_path):
    """从SKILL.md提取技能信息"""
    skill_md = Path(skill_path) / "SKILL.md"
    
    if not skill_md.exists():
        return None
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = {
            'name': '',
            'description': '',
            'keywords': [],
            'category': 'general'
        }
        
        # 提取 name
        name_match = re.search(r'^name:\s*(.+)', content, re.MULTILINE)
        if name_match:
            info['name'] = name_match.group(1).strip()
        
        # 提取 description
        desc_match = re.search(r'^description:\s*[\|\>]?\s*\n?\s*(.+)', content, re.MULTILINE | re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).strip()
            # 取第一行
            info['description'] = desc.split('\n')[0][:100]
        
        # 提取 keywords
        keywords_match = re.search(r'^keywords:\s*\n((?:\s*-\s*.+\n?)+)', content, re.MULTILINE)
        if keywords_match:
            keywords_text = keywords_match.group(1)
            info['keywords'] = [k.strip().strip('- ') for k in keywords_text.strip().split('\n') if k.strip()][:5]
        
        # 提取 category
        category_match = re.search(r'^category:\s*(.+)', content, re.MULTILINE)
        if category_match:
            info['category'] = category_match.group(1).strip()
        
        return info
    except Exception as e:
        print(f"Error reading {skill_path}: {e}")
        return None

def generate_test_template(skill_info):
    """生成测试模板"""
    name = skill_info['name']
    description = skill_info['description']
    keywords = skill_info['keywords']
    category = skill_info['category']
    
    # 生成测试用例
    test_cases = []
    
    # 基础功能测试
    test_cases.append({
        'id': 'TC-001',
        'name': f'{name} - 基础功能测试',
        'input': f'用户请求: "请帮我使用{name}技能"',
        'expected': f'技能正常触发，返回{category}相关结果',
        'validation': [
            '响应时间 < 5秒',
            '输出包含关键词',
            '结果符合预期格式'
        ]
    })
    
    # 边界场景测试
    test_cases.append({
        'id': 'TC-002',
        'name': f'{name} - 边界场景测试',
        'input': '用户请求: 空输入或无效输入',
        'expected': '技能优雅处理，返回友好提示',
        'validation': [
            '不抛出异常',
            '返回错误提示',
            '提供正确用法示例'
        ]
    })
    
    # 集成测试
    test_cases.append({
        'id': 'TC-003',
        'name': f'{name} - 集成测试',
        'input': f'用户请求: 复杂场景，结合多个关键词: {", ".join(keywords[:3]) if keywords else "相关功能"}',
        'expected': '技能与其他技能协同工作',
        'validation': [
            '数据传递正确',
            '无冲突或重复',
            '结果一致性'
        ]
    })
    
    # 生成分类
    category_tests = {
        'productivity': ['效率提升测试', '自动化流程测试'],
        'business': ['商业模式测试', '盈利分析测试'],
        'technology': ['技术实现测试', '兼容性测试'],
        'content': ['内容质量测试', '创作流程测试'],
        'general': ['通用功能测试', '稳定性测试']
    }
    
    # 根据分类添加特定测试
    if category in category_tests:
        for i, test_name in enumerate(category_tests[category][:2], 4):
            test_cases.append({
                'id': f'TC-{i:03d}',
                'name': f'{name} - {test_name}',
                'input': f'用户请求: {test_name}场景',
                'expected': f'符合{category}分类的预期结果',
                'validation': [
                    '功能正确',
                    '性能达标',
                    '用户体验良好'
                ]
            })
    
    # 生成Markdown
    md_content = f"""# 测试用例 - {name}

> {description}

## 测试覆盖范围

- 基础功能验证
- 边界场景处理
- 集成兼容性
- {category}特定场景

## 测试用例列表

"""
    
    for tc in test_cases:
        md_content += f"""### {tc['id']}: {tc['name']}

**输入**:
```
{tc['input']}
```

**预期输出**:
```
{tc['expected']}
```

**验证点**:
"""
        for point in tc['validation']:
            md_content += f"- [ ] {point}\n"
        md_content += "\n---\n\n"
    
    md_content += f"""## 测试执行记录

| 测试ID | 状态 | 执行时间 | 备注 |
|--------|------|----------|------|
"""
    for tc in test_cases:
        md_content += f"| {tc['id']} | ⏳ 待执行 | - | - |\n"
    
    md_content += f"""
---

*测试模板生成时间: 2026-05-29*  
*技能分类: {category}*
"""
    
    return md_content

def generate_test_for_skill(skill_name):
    """为单个技能生成测试"""
    skill_path = Path('skills') / skill_name
    
    if not skill_path.exists():
        print(f"[SKIP] {skill_name}: Directory not found")
        return False
    
    # 检查是否已有测试
    test_file = skill_path / 'test' / 'test_cases.md'
    if test_file.exists():
        print(f"[SKIP] {skill_name}: Already has test_cases.md")
        return False
    
    # 提取技能信息
    skill_info = extract_skill_info(skill_path)
    if not skill_info:
        print(f"[ERROR] {skill_name}: Could not extract info")
        return False
    
    # 创建 test/ 目录
    test_dir = skill_path / 'test'
    test_dir.mkdir(exist_ok=True)
    
    # 生成测试模板
    test_content = generate_test_template(skill_info)
    
    # 保存测试文件
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"[CREATED] {skill_name}: test/test_cases.md")
    return True

def main():
    # 候选技能列表
    candidate_skills = [
        'ai-agent-operation-framework',
        'ai-business-model-innovation',
        'ai-community-builder',
        'ai-empowered-brand-ip-strategy',
        'ai-native-marketing-strategy',
        'founder-action-guide',
        'iterative-product-dev',
        'opportunity-window-strategy',
        'tech-commercialization-timing',
        'vertical-ai-startup-guide'
    ]
    
    print("=== Generating Test Templates ===\n")
    
    created_count = 0
    skipped_count = 0
    error_count = 0
    
    for skill_name in candidate_skills:
        try:
            if generate_test_for_skill(skill_name):
                created_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"[ERROR] {skill_name}: {e}")
            error_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Created: {created_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"Total: {len(candidate_skills)}")
    
    # 生成报告
    report_path = "TEST_GENERATION_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Test Generation Report\n\n")
        f.write(f"**Generated**: 2026-05-29\n")
        f.write(f"**Target Skills**: {len(candidate_skills)}\n")
        f.write(f"**Created**: {created_count}\n")
        f.write(f"**Skipped**: {skipped_count}\n\n")
        
        f.write("## Candidate Skills\n\n")
        for skill_name in candidate_skills:
            status = "✅ Created" if (Path('skills') / skill_name / 'test' / 'test_cases.md').exists() else "⏭️ Skipped"
            f.write(f"- {skill_name}: {status}\n")
    
    print(f"\nReport saved: {report_path}")

if __name__ == "__main__":
    main()
