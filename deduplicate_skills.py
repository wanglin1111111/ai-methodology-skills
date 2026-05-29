#!/usr/bin/env python3
"""
技能去重审查 - 识别并合并相似度>80%的技能
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def extract_skill_content(skill_path):
    """提取技能文件的核心内容"""
    skill_md = Path(skill_path) / "SKILL.md"
    
    if not skill_md.exists():
        return None
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取YAML frontmatter
        yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        yaml_content = yaml_match.group(1) if yaml_match else ""
        
        # 提取正文（去掉YAML和代码块）
        body = re.sub(r'^---\s*\n.*?\n---', '', content, flags=re.DOTALL)
        body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
        body = re.sub(r'`[^`]+`', '', body)
        
        # 提取关键信息
        info = {
            'name': '',
            'description': '',
            'keywords': [],
            'category': '',
            'body': body.lower()[:500]  # 前500字符用于比较
        }
        
        # 从YAML提取
        name_match = re.search(r'^name:\s*(.+)', yaml_content, re.MULTILINE)
        if name_match:
            info['name'] = name_match.group(1).strip()
        
        desc_match = re.search(r'^description:\s*[\|\>]?\s*\n?\s*(.+)', yaml_content, re.MULTILINE | re.DOTALL)
        if desc_match:
            info['description'] = desc_match.group(1).strip()[:200]
        
        keywords_match = re.search(r'^keywords:\s*\n((?:\s*-\s*.+\n?)+)', yaml_content, re.MULTILINE)
        if keywords_match:
            keywords_text = keywords_match.group(1)
            info['keywords'] = [k.strip('- ') for k in keywords_text.strip().split('\n') if k.strip()]
        
        category_match = re.search(r'^category:\s*(.+)', yaml_content, re.MULTILINE)
        if category_match:
            info['category'] = category_match.group(1).strip()
        
        return info
    except Exception as e:
        print(f"Error reading {skill_path}: {e}")
        return None

def calculate_similarity(skill1, skill2):
    """计算两个技能的相似度 (0-100)"""
    if not skill1 or not skill2:
        return 0
    
    scores = []
    
    # 1. 关键词重叠度 (40%)
    keywords1 = set(k.lower() for k in skill1['keywords'])
    keywords2 = set(k.lower() for k in skill2['keywords'])
    if keywords1 and keywords2:
        overlap = len(keywords1 & keywords2)
        union = len(keywords1 | keywords2)
        keyword_score = (overlap / union * 100) if union > 0 else 0
        scores.append(('keywords', keyword_score * 0.4))
    
    # 2. 分类相同 (20%)
    category_score = 100 if skill1['category'] == skill2['category'] else 0
    scores.append(('category', category_score * 0.2))
    
    # 3. 描述相似度 (20%)
    desc1 = skill1['description'].lower().split()
    desc2 = skill2['description'].lower().split()
    if desc1 and desc2:
        desc_overlap = len(set(desc1) & set(desc2))
        desc_union = len(set(desc1) | set(desc2))
        desc_score = (desc_overlap / desc_union * 100) if desc_union > 0 else 0
        scores.append(('description', desc_score * 0.2))
    
    # 4. 正文相似度 (20%)
    body1 = skill1['body'].split()
    body2 = skill2['body'].split()
    if body1 and body2:
        body_overlap = len(set(body1) & set(body2))
        body_union = len(set(body1) | set(body2))
        body_score = (body_overlap / body_union * 100) if body_union > 0 else 0
        scores.append(('body', body_score * 0.2))
    
    total_score = sum(score for _, score in scores)
    return round(total_score, 1)

def find_similar_skills(skills_dir="skills", threshold=80):
    """查找相似度超过阈值的技能对"""
    skills_path = Path(skills_dir)
    
    if not skills_path.exists():
        print(f"Error: {skills_dir}/ directory not found")
        return []
    
    # 加载所有技能
    print("Loading skills...")
    skills = {}
    for skill_dir in sorted(skills_path.iterdir()):
        if skill_dir.is_dir():
            content = extract_skill_content(skill_dir)
            if content:
                skills[skill_dir.name] = content
    
    print(f"Loaded {len(skills)} skills\n")
    
    # 计算相似度
    print(f"Calculating similarities (threshold: {threshold}%)...")
    similar_pairs = []
    skill_names = list(skills.keys())
    
    for i in range(len(skill_names)):
        for j in range(i + 1, len(skill_names)):
            name1 = skill_names[i]
            name2 = skill_names[j]
            
            similarity = calculate_similarity(skills[name1], skills[name2])
            
            if similarity >= threshold:
                similar_pairs.append({
                    'skill1': name1,
                    'skill2': name2,
                    'similarity': similarity,
                    'category': skills[name1]['category']
                })
    
    # 按相似度排序
    similar_pairs.sort(key=lambda x: x['similarity'], reverse=True)
    
    return similar_pairs, skills

def group_by_prefix(skills):
    """按前缀分组技能"""
    prefix_groups = defaultdict(list)
    
    for name in skills.keys():
        # 提取前缀 (如 ai-era-, personal-)
        parts = name.split('-')
        if len(parts) >= 2:
            prefix = '-'.join(parts[:2]) + '-'
            prefix_groups[prefix].append(name)
    
    # 只保留有多个技能的组
    return {k: v for k, v in prefix_groups.items() if len(v) >= 2}

def main():
    print("=== Skill Deduplication Review ===\n")
    
    # 查找相似技能
    similar_pairs, skills = find_similar_skills(threshold=80)
    
    # 按前缀分组
    prefix_groups = group_by_prefix(skills)
    
    print(f"\nFound {len(similar_pairs)} similar pairs\n")
    
    # 显示高相似度对
    if similar_pairs:
        print("High Similarity Pairs (>80%):")
        print("-" * 80)
        for pair in similar_pairs[:10]:  # 只显示前10个
            print(f"{pair['similarity']}% | {pair['skill1']} <-> {pair['skill2']}")
        print()
    
    # 显示前缀分组
    print("Prefix Groups (potential merge candidates):")
    print("-" * 80)
    for prefix, group_skills in sorted(prefix_groups.items(), key=lambda x: -len(x[1])):
        if len(group_skills) >= 3:
            print(f"\n{prefix}* ({len(group_skills)} skills):")
            for skill in sorted(group_skills):
                print(f"  - {skill}")
    
    # 生成合并建议
    print("\n" + "=" * 80)
    print("MERGE RECOMMENDATIONS")
    print("=" * 80)
    
    recommendations = []
    
    # 基于前缀分组推荐
    for prefix, group_skills in prefix_groups.items():
        if len(group_skills) >= 3:
            recommendations.append({
                'type': 'prefix_group',
                'prefix': prefix,
                'skills': group_skills,
                'suggestion': f"Merge {len(group_skills)} skills into {max(1, len(group_skills) // 2)} comprehensive skills"
            })
    
    # 基于高相似度对推荐
    high_similarity_groups = defaultdict(list)
    for pair in similar_pairs:
        if pair['similarity'] >= 90:
            # 将高相似度技能归为一组
            found = False
            for group in high_similarity_groups.values():
                if pair['skill1'] in group or pair['skill2'] in group:
                    group.add(pair['skill1'])
                    group.add(pair['skill2'])
                    found = True
                    break
            if not found:
                high_similarity_groups[pair['skill1']] = {pair['skill1'], pair['skill2']}
    
    for group_name, group_skills in high_similarity_groups.items():
        if len(group_skills) >= 2:
            recommendations.append({
                'type': 'high_similarity',
                'skills': list(group_skills),
                'suggestion': f"Merge {len(group_skills)} highly similar skills"
            })
    
    # 显示建议
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['suggestion']}")
        if rec['type'] == 'prefix_group':
            print(f"   Prefix: {rec['prefix']}")
        print(f"   Skills: {', '.join(rec['skills'][:5])}")
        if len(rec['skills']) > 5:
            print(f"   ... and {len(rec['skills']) - 5} more")
    
    # 保存报告
    report_path = "DEDUPLICATION_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Skill Deduplication Report\n\n")
        f.write(f"**Generated**: 2026-05-29\n")
        f.write(f"**Total Skills**: {len(skills)}\n")
        f.write(f"**Similar Pairs Found**: {len(similar_pairs)}\n\n")
        
        f.write("## High Similarity Pairs (>80%)\n\n")
        if similar_pairs:
            f.write("| Similarity | Skill 1 | Skill 2 | Category |\n")
            f.write("|------------|---------|---------|----------|\n")
            for pair in similar_pairs:
                f.write(f"| {pair['similarity']}% | {pair['skill1']} | {pair['skill2']} | {pair['category']} |\n")
        else:
            f.write("No high similarity pairs found.\n")
        
        f.write("\n## Prefix Groups\n\n")
        for prefix, group_skills in sorted(prefix_groups.items(), key=lambda x: -len(x[1])):
            if len(group_skills) >= 3:
                f.write(f"\n### {prefix}* ({len(group_skills)} skills)\n\n")
                for skill in sorted(group_skills):
                    f.write(f"- {skill}\n")
        
        f.write("\n## Merge Recommendations\n\n")
        for i, rec in enumerate(recommendations, 1):
            f.write(f"\n### {i}. {rec['suggestion']}\n\n")
            f.write(f"**Skills**:\n")
            for skill in rec['skills']:
                f.write(f"- {skill}\n")
            f.write(f"\n**Action**: Review and consider merging\n")
    
    print(f"\n\nReport saved: {report_path}")
    
    # 总结
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total skills analyzed: {len(skills)}")
    print(f"Similar pairs found: {len(similar_pairs)}")
    print(f"Prefix groups: {len(prefix_groups)}")
    print(f"Merge recommendations: {len(recommendations)}")

if __name__ == "__main__":
    main()
