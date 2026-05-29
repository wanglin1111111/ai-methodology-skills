#!/usr/bin/env python3
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
            print(f"\n  {r['file']}")
            for issue in r['issues']:
                print(f"    - {issue}")

if __name__ == "__main__":
    run_quality_gate()
