#!/usr/bin/env python3
"""
分析技能库的元数据缺失率、测试覆盖率和目录结构问题
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict

def check_skill_structure(skill_path):
    """检查单个技能的目录结构"""
    skill_dir = Path(skill_path)
    skill_name = skill_dir.name
    
    results = {
        'name': skill_name,
        'has_skill_md': False,
        'has_metadata_json': False,
        'has_test_dir': False,
        'has_test_cases': False,
        'has_example_dir': False,
        'has_real_examples': False,
        'has_docs_dir': False,
        'has_scripts_dir': False,
        'skill_md_valid': False,
        'yaml_valid': False,
        'naming_valid': True,
        'issues': []
    }
    
    # 检查命名规范 (kebab-case)
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', skill_name):
        results['naming_valid'] = False
        results['issues'].append('命名不符合 kebab-case')
    
    # 检查 SKILL.md
    skill_md = skill_dir / 'SKILL.md'
    if skill_md.exists():
        results['has_skill_md'] = True
        
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查 YAML frontmatter
            if content.startswith('---'):
                results['yaml_valid'] = True
                yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                if yaml_match:
                    yaml_content = yaml_match.group(1)
                    required_fields = ['name', 'version', 'description', 'category', 'stability']
                    for field in required_fields:
                        if field not in yaml_content:
                            results['issues'].append(f'SKILL.md 缺少 {field}')
            else:
                results['issues'].append('SKILL.md 缺少 YAML frontmatter')
                
        except Exception as e:
            results['issues'].append(f'SKILL.md 读取错误: {e}')
    else:
        results['issues'].append('缺少 SKILL.md')
    
    # 检查 metadata.json
    metadata_json = skill_dir / 'metadata.json'
    if metadata_json.exists():
        results['has_metadata_json'] = True
        try:
            with open(metadata_json, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError:
            results['issues'].append('metadata.json 格式错误')
    else:
        results['issues'].append('缺少 metadata.json')
    
    # 检查 test/ 目录
    test_dir = skill_dir / 'test'
    if test_dir.exists() and test_dir.is_dir():
        results['has_test_dir'] = True
        test_cases = test_dir / 'test_cases.md'
        if test_cases.exists():
            results['has_test_cases'] = True
    
    # 检查 example/ 目录
    example_dir = skill_dir / 'example'
    if example_dir.exists() and example_dir.is_dir():
        results['has_example_dir'] = True
        real_examples = example_dir / 'real_world_examples.md'
        if real_examples.exists():
            results['has_real_examples'] = True
    
    # 检查 docs/ 目录
    docs_dir = skill_dir / 'docs'
    if docs_dir.exists() and docs_dir.is_dir():
        results['has_docs_dir'] = True
    
    # 检查 scripts/ 目录
    scripts_dir = skill_dir / 'scripts'
    if scripts_dir.exists() and scripts_dir.is_dir():
        results['has_scripts_dir'] = True
    
    return results

def analyze_all_skills(skills_dir='skills'):
    """分析所有技能"""
    skills_path = Path(skills_dir)
    
    if not skills_path.exists():
        print(f"Error: {skills_dir}/ directory not found")
        return None
    
    results = []
    for skill_dir in sorted(skills_path.iterdir()):
        if skill_dir.is_dir():
            result = check_skill_structure(skill_dir)
            results.append(result)
    
    return results

def generate_report(results):
    """生成分析报告"""
    total = len(results)
    
    # 统计各项指标
    stats = {
        'total': total,
        'has_skill_md': sum(1 for r in results if r['has_skill_md']),
        'has_metadata_json': sum(1 for r in results if r['has_metadata_json']),
        'has_test_dir': sum(1 for r in results if r['has_test_dir']),
        'has_test_cases': sum(1 for r in results if r['has_test_cases']),
        'has_example_dir': sum(1 for r in results if r['has_example_dir']),
        'has_real_examples': sum(1 for r in results if r['has_real_examples']),
        'has_docs_dir': sum(1 for r in results if r['has_docs_dir']),
        'has_scripts_dir': sum(1 for r in results if r['has_scripts_dir']),
        'naming_valid': sum(1 for r in results if r['naming_valid']),
        'yaml_valid': sum(1 for r in results if r['yaml_valid']),
    }
    
    # 计算百分比
    percentages = {k: round(v / total * 100, 1) for k, v in stats.items() if k != 'total'}
    
    # 找出有问题的技能
    problem_skills = [r for r in results if r['issues']]
    
    return stats, percentages, problem_skills

def main():
    print("=== Skill Metadata Analysis ===\n")
    
    results = analyze_all_skills()
    if not results:
        return
    
    stats, percentages, problem_skills = generate_report(results)
    
    print(f"Total Skills: {stats['total']}\n")
    
    print("=" * 60)
    print("METADATA COVERAGE")
    print("=" * 60)
    print(f"SKILL.md:          {stats['has_skill_md']}/{stats['total']} ({percentages['has_skill_md']}%)")
    print(f"metadata.json:     {stats['has_metadata_json']}/{stats['total']} ({percentages['has_metadata_json']}%)")
    print(f"YAML valid:        {stats['yaml_valid']}/{stats['total']} ({percentages['yaml_valid']}%)")
    print(f"Naming valid:      {stats['naming_valid']}/{stats['total']} ({percentages['naming_valid']}%)")
    
    print("\n" + "=" * 60)
    print("TEST COVERAGE")
    print("=" * 60)
    print(f"test/ directory:   {stats['has_test_dir']}/{stats['total']} ({percentages['has_test_dir']}%)")
    print(f"test_cases.md:     {stats['has_test_cases']}/{stats['total']} ({percentages['has_test_cases']}%)")
    print(f"example/ directory:{stats['has_example_dir']}/{stats['total']} ({percentages['has_example_dir']}%)")
    print(f"real_examples.md:  {stats['has_real_examples']}/{stats['total']} ({percentages['has_real_examples']}%)")
    
    print("\n" + "=" * 60)
    print("DIRECTORY STRUCTURE")
    print("=" * 60)
    print(f"docs/ directory:   {stats['has_docs_dir']}/{stats['total']} ({percentages['has_docs_dir']}%)")
    print(f"scripts/ directory:{stats['has_scripts_dir']}/{stats['total']} ({percentages['has_scripts_dir']}%)")
    
    print("\n" + "=" * 60)
    print("PROBLEM SUMMARY")
    print("=" * 60)
    print(f"Skills with issues: {len(problem_skills)}/{stats['total']}")
    
    # 统计问题类型
    issue_counts = defaultdict(int)
    for skill in problem_skills:
        for issue in skill['issues']:
            issue_counts[issue] += 1
    
    print("\nTop issues:")
    for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  - {issue}: {count}")
    
    # 保存详细报告
    report_path = "METADATA_ANALYSIS_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Skill Metadata Analysis Report\n\n")
        f.write(f"**Generated**: 2026-05-29\n")
        f.write(f"**Total Skills**: {stats['total']}\n\n")
        
        f.write("## Summary\n\n")
        f.write("| Metric | Count | Percentage |\n")
        f.write("|--------|-------|------------|\n")
        f.write(f"| SKILL.md | {stats['has_skill_md']} | {percentages['has_skill_md']}% |\n")
        f.write(f"| metadata.json | {stats['has_metadata_json']} | {percentages['has_metadata_json']}% |\n")
        f.write(f"| test/ directory | {stats['has_test_dir']} | {percentages['has_test_dir']}% |\n")
        f.write(f"| test_cases.md | {stats['has_test_cases']} | {percentages['has_test_cases']}% |\n")
        f.write(f"| example/ directory | {stats['has_example_dir']} | {percentages['has_example_dir']}% |\n")
        f.write(f"| real_examples.md | {stats['has_real_examples']} | {percentages['has_real_examples']}% |\n")
        f.write(f"| docs/ directory | {stats['has_docs_dir']} | {percentages['has_docs_dir']}% |\n")
        f.write(f"| scripts/ directory | {stats['has_scripts_dir']} | {percentages['has_scripts_dir']}% |\n")
        f.write(f"| Naming valid | {stats['naming_valid']} | {percentages['naming_valid']}% |\n\n")
        
        f.write("## Skills with Issues\n\n")
        f.write("| Skill | Issues |\n")
        f.write("|-------|--------|\n")
        for skill in sorted(problem_skills, key=lambda x: len(x['issues']), reverse=True)[:30]:
            issues_str = "; ".join(skill['issues'][:3])
            if len(skill['issues']) > 3:
                issues_str += f" (+{len(skill['issues'])-3} more)"
            f.write(f"| {skill['name']} | {issues_str} |\n")
        
        f.write("\n## Issue Breakdown\n\n")
        for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
            f.write(f"- {issue}: {count}\n")
    
    print(f"\n\nDetailed report saved: {report_path}")
    
    # 返回关键指标
    return {
        'metadata_json_rate': percentages['has_metadata_json'],
        'test_coverage_rate': percentages['has_test_cases'],
        'example_coverage_rate': percentages['has_real_examples'],
        'naming_valid_rate': percentages['naming_valid'],
        'problem_count': len(problem_skills)
    }

if __name__ == "__main__":
    metrics = main()
    print(f"\n\nKey Metrics:")
    print(f"  metadata.json coverage: {metrics['metadata_json_rate']}%")
    print(f"  Test coverage: {metrics['test_coverage_rate']}%")
    print(f"  Example coverage: {metrics['example_coverage_rate']}%")
    print(f"  Naming valid: {metrics['naming_valid_rate']}%")
