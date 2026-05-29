#!/usr/bin/env python3
"""
为缺少 YAML frontmatter 的技能文件添加标准 frontmatter
"""

import os
import re
from pathlib import Path

def extract_info_from_content(content, skill_name):
    """从文件内容提取信息"""
    info = {
        'name': skill_name,
        'version': '1.0.0',
        'author': 'Anonymous',
        'license': 'MIT',
        'description': '',
        'keywords': [],
        'category': 'general'
    }
    
    # 尝试提取 name
    name_match = re.search(r'name:\s*(.+)', content)
    if name_match:
        info['name'] = name_match.group(1).strip()
    
    # 尝试提取 version
    version_match = re.search(r'version:\s*(.+)', content)
    if version_match:
        info['version'] = version_match.group(1).strip()
    
    # 尝试提取 author
    author_match = re.search(r'author:\s*(.+)', content)
    if author_match:
        info['author'] = author_match.group(1).strip()
    
    # 尝试提取 description
    desc_match = re.search(r'description:\s*[\|\>]?\s*\n?\s*(.+)', content, re.DOTALL)
    if desc_match:
        desc = desc_match.group(1).strip()
        # 只取第一行
        desc = desc.split('\n')[0].strip()
        info['description'] = desc[:100]  # 限制长度
    
    # 尝试提取 keywords
    keywords_match = re.search(r'keywords:\s*\[(.*?)\]', content, re.DOTALL)
    if keywords_match:
        keywords_str = keywords_match.group(1)
        keywords = [k.strip().strip('"\'') for k in keywords_str.split(',')]
        info['keywords'] = keywords[:5]  # 最多5个
    
    # 尝试提取 category
    category_match = re.search(r'category:\s*(.+)', content)
    if category_match:
        info['category'] = category_match.group(1).strip()
    
    return info

def fix_yaml_frontmatter(skill_path):
    """修复 YAML frontmatter"""
    skill_md = Path(skill_path) / "SKILL.md"
    
    if not skill_md.exists():
        return False, "SKILL.md not found"
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有正确的 YAML frontmatter
        if content.startswith('---'):
            # 检查是否有 stability
            if 'stability:' not in content:
                # 在 category 后添加 stability
                lines = content.split('\n')
                new_lines = []
                added = False
                
                for line in lines:
                    new_lines.append(line)
                    if line.startswith('category:') and not added:
                        indent = len(line) - len(line.lstrip())
                        new_lines.append(' ' * indent + 'stability: stable')
                        added = True
                
                if added:
                    with open(skill_md, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines))
                    return True, "Added stability to existing frontmatter"
            return False, "Already has proper frontmatter"
        
        # 提取信息
        skill_name = skill_path.name
        info = extract_info_from_content(content, skill_name)
        
        # 构建新的 YAML frontmatter
        yaml_content = f"""---
name: {info['name']}
version: {info['version']}
author: {info['author']}
license: {info['license']}
description: {info['description']}
keywords:
{chr(10).join('  - ' + k for k in info['keywords']) if info['keywords'] else '  - ai'}
category: {info['category']}
stability: stable
---

"""
        
        # 找到第一个标题
        lines = content.split('\n')
        title_idx = -1
        for i, line in enumerate(lines):
            if line.startswith('# ') and not line.startswith('# SKILL.md'):
                title_idx = i
                break
        
        if title_idx >= 0:
            # 在第一个标题前插入 frontmatter
            new_content = yaml_content + '\n'.join(lines[title_idx:])
        else:
            # 没有找到标题，在文件开头添加
            new_content = yaml_content + content
        
        with open(skill_md, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Added YAML frontmatter"
            
    except Exception as e:
        return False, f"Error: {e}"

def main():
    # 列出需要修复的技能
    skills_to_fix = [
        "ai-agent-operation-framework",
        "ai-brand-landing-practice",
        "ai-companion-robot-framework",
        "ai-creative-synergy-framework",
        "ai-empowered-ip-creation-pipeline",
        "ai-era-brand-growth-methodology",
        "ai-era-consumption-market-framework",
        "ai-era-industry-replacement-framework",
        "ai-marketing-efficiency-methodology",
        "ai-second-growth-curve-strategy",
        "brand-data-platform-construction",
        "digital-ip-ecosystem-methodology",
        "ip-brand-collaboration-resonance-methodology",
        "personal-ai-collaboration-ability",
        "physical-ai-landing-strategy"
    ]
    
    print("=== Fixing YAML Frontmatter ===\n")
    
    fixed_count = 0
    
    for skill_name in skills_to_fix:
        skill_path = Path("skills") / skill_name
        if skill_path.exists():
            success, msg = fix_yaml_frontmatter(skill_path)
            if success:
                print(f"[FIXED] {skill_name}: {msg}")
                fixed_count += 1
            else:
                print(f"[WARN] {skill_name}: {msg}")
        else:
            print(f"[SKIP] {skill_name}: Directory not found")
    
    # 单独处理 content-topic-evaluator
    skill_path = Path("skills") / "content-topic-evaluator"
    if skill_path.exists():
        success, msg = fix_yaml_frontmatter(skill_path)
        if success:
            print(f"[FIXED] content-topic-evaluator: {msg}")
            fixed_count += 1
        else:
            print(f"[WARN] content-topic-evaluator: {msg}")
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {fixed_count}/{len(skills_to_fix) + 1}")

if __name__ == "__main__":
    main()
