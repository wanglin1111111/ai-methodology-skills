#!/usr/bin/env python3
"""
AI变现策略师技能质量测试脚本
"""

import re
import sys

def test_skill_quality(file_path):
    """测试技能质量"""
    print("=" * 60)
    print("AI变现策略师技能质量测试")
    print("=" * 60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tests = []
    score = 0
    max_score = 100
    
    # 1. YAML Frontmatter检查 (15分)
    yaml_score = 0
    required_fields = ['name', 'version', 'description', 'display_name', 'stability', 'last_updated']
    for field in required_fields:
        if re.search(f'^{field}:', content, re.MULTILINE):
            yaml_score += 2.5
    tests.append(("YAML Frontmatter", yaml_score, 15))
    
    # 2. 核心章节检查 (20分)
    section_score = 0
    required_sections = [
        '核心变现路径框架',
        '产品矩阵策略',
        '用户付费心理分析',
        '快速验证方法论',
        '实战工具包',
        '使用示例',
        '常见误区警示'
    ]
    for section in required_sections:
        if section in content:
            section_score += 20/7
    tests.append(("核心章节", section_score, 20))
    
    # 3. 表格使用 (10分)
    table_count = len(re.findall(r'\|.*\|.*\|', content))
    table_score = min(10, table_count * 0.5)
    tests.append(("表格丰富度", table_score, 10))
    
    # 4. 代码示例 (10分)
    code_blocks = len(re.findall(r'```[\w]*\n', content))
    code_score = min(10, code_blocks * 5)
    tests.append(("代码示例", code_score, 10))
    
    # 5. 使用场景 (15分)
    scenario_score = 0
    if '使用示例' in content:
        scenario_score += 5
    if '场景' in content:
        scenario_score += 5
    if '用户输入' in content:
        scenario_score += 5
    tests.append(("使用场景", scenario_score, 15))
    
    # 6. 可操作性 (15分)
    action_score = 0
    if '检查清单' in content or '清单' in content:
        action_score += 5
    if '步骤' in content or '三步法' in content:
        action_score += 5
    if '方法论' in content:
        action_score += 5
    tests.append(("可操作性", action_score, 15))
    
    # 7. 完整性 (15分)
    completeness_score = 0
    if len(content) > 5000:
        completeness_score += 5
    if '更新日志' in content or 'CHANGELOG' in content:
        completeness_score += 5
    if '核心公式' in content or '总结' in content:
        completeness_score += 5
    tests.append(("完整性", completeness_score, 15))
    
    # 打印结果
    print("\n测试项目:")
    total_score = 0
    for name, got, max_val in tests:
        print(f"  {name}: {got:.1f}/{max_val}")
        total_score += got
    
    print(f"\n总分: {total_score:.1f}/100")
    
    if total_score >= 90:
        print("评级: ⭐⭐⭐⭐⭐ 优秀")
    elif total_score >= 80:
        print("评级: ⭐⭐⭐⭐ 良好")
    elif total_score >= 70:
        print("评级: ⭐⭐⭐ 一般")
    else:
        print("评级: ⭐⭐ 需改进")
    
    print("=" * 60)
    
    return total_score

if __name__ == "__main__":
    score = test_skill_quality(r"C:\Users\22812\.stepfun\skills\ai-monetization-strategist\SKILL.md")
    sys.exit(0 if score >= 80 else 1)
