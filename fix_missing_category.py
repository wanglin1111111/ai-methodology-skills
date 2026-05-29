#!/usr/bin/env python3
"""
为缺少 category 字段的技能文件添加该字段
同时修复 YAML frontmatter 位置问题
"""

import os
from pathlib import Path

def fix_skill_file(skill_path):
    """修复单个技能文件"""
    skill_md = Path(skill_path) / "SKILL.md"
    
    if not skill_md.exists():
        return False, "SKILL.md not found"
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有 category 字段
        if 'category:' in content:
            return False, "Already has category"
        
        # 尝试在 YAML frontmatter 中添加 category
        # 查找 keywords: 行，在其后添加 category
        if 'keywords:' in content:
            lines = content.split('\n')
            new_lines = []
            added = False
            in_yaml = False
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                # 检测 YAML frontmatter 开始
                if line.strip() == '---' and not in_yaml:
                    in_yaml = True
                    continue
                
                # 在 keywords 行后添加 category
                if in_yaml and line.strip().startswith('keywords:') and not added:
                    # 找到 keywords 的缩进
                    base_indent = "  "
                    new_lines.append(f"{base_indent}category: general")
                    added = True
                
                # 检测 YAML frontmatter 结束
                if in_yaml and line.strip() == '---' and i > 0:
                    in_yaml = False
            
            if added:
                with open(skill_md, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                return True, "Added category field"
        
        # 如果没有 keywords，尝试在 description 后添加
        if 'description:' in content:
            lines = content.split('\n')
            new_lines = []
            added = False
            in_yaml = False
            yaml_started = False
            
            for i, line in enumerate(lines):
                # 检测 YAML frontmatter 开始
                if line.strip() == '---':
                    if not yaml_started:
                        yaml_started = True
                        in_yaml = True
                    else:
                        in_yaml = False
                
                new_lines.append(line)
                
                # 在 description 段落结束后添加 category
                if in_yaml and not added:
                    # 简单检测：如果当前行是 description 相关，且下一行不是缩进
                    if line.strip().startswith('description:') or (
                        i > 0 and 
                        lines[i-1].strip().startswith('description:') and
                        not line.strip().startswith(' ') and
                        line.strip() and
                        not line.strip().startswith('description:')
                    ):
                        new_lines.append('category: general')
                        added = True
            
            if added:
                with open(skill_md, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                return True, "Added category field after description"
        
        return False, "Could not find suitable location for category"
            
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
        "content-topic-evaluator",
        "digital-ip-ecosystem-methodology",
        "ip-brand-collaboration-resonance-methodology",
        "personal-ai-collaboration-ability",
        "physical-ai-landing-strategy"
    ]
    
    print("=== Fixing Missing Category Fields ===\n")
    
    fixed_count = 0
    
    for skill_name in skills_to_fix:
        skill_path = Path("skills") / skill_name
        if skill_path.exists():
            success, msg = fix_skill_file(skill_path)
            if success:
                print(f"[FIXED] {skill_name}: {msg}")
                fixed_count += 1
            else:
                print(f"[WARN] {skill_name}: {msg}")
        else:
            print(f"[SKIP] {skill_name}: Directory not found")
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {fixed_count}/{len(skills_to_fix)}")

if __name__ == "__main__":
    main()
