#!/usr/bin/env python3
"""
修复缺少 category 字段的技能
"""

from pathlib import Path

def fix_skill(skill_name, default_category='general'):
    """修复单个技能"""
    skill_md = Path('skills') / skill_name / 'SKILL.md'
    
    if not skill_md.exists():
        print(f"[SKIP] {skill_name}: SKILL.md not found")
        return False
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有 category
        if 'category:' in content:
            print(f"[OK] {skill_name}: Already has category")
            return False
        
        # 在 YAML frontmatter 中添加 category
        lines = content.split('\n')
        new_lines = []
        added = False
        in_yaml = False
        
        for line in lines:
            new_lines.append(line)
            
            # 检测 YAML frontmatter 开始
            if line.strip() == '---' and not in_yaml:
                in_yaml = True
                continue
            
            # 在 keywords 后添加 category
            if in_yaml and line.strip().startswith('keywords:') and not added:
                # 找到 keywords 结束位置
                continue
            
            # 在 keywords 列表结束后添加 category
            if in_yaml and not added:
                # 检测是否在 keywords 列表中
                if line.strip().startswith('- ') and 'keywords:' in '\n'.join(new_lines[-5:]):
                    continue
                elif line.strip().startswith('keywords:'):
                    continue
                elif 'keywords:' in '\n'.join(new_lines[-10:]) and line.strip() and not line.strip().startswith('-') and not line.strip().startswith('keywords:'):
                    # 在 keywords 后添加 category
                    new_lines.append(f'category: {default_category}')
                    added = True
        
        if not added:
            # 备用方案：在 stability 前添加
            new_lines = []
            for line in lines:
                if line.strip().startswith('stability:') and not added:
                    new_lines.append(f'category: {default_category}')
                    added = True
                new_lines.append(line)
        
        if added:
            with open(skill_md, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            print(f"[FIXED] {skill_name}: Added category: {default_category}")
            return True
        else:
            print(f"[WARN] {skill_name}: Could not find insertion point")
            return False
            
    except Exception as e:
        print(f"[ERROR] {skill_name}: {e}")
        return False

def main():
    # 需要修复的技能
    skills_to_fix = [
        ('ai-application-creator', 'productivity'),
        ('ai-hardware-design', 'technology'),
        ('ai-monetization-strategist', 'business'),
        ('ai-workflow-automation', 'productivity'),
        ('edge-ai-agent', 'technology'),
        ('solo-entrepreneur-growth', 'business'),
        ('xiaohongshu-content-creator', 'content')
    ]
    
    print("=== Fixing Missing Category Fields ===\n")
    
    fixed_count = 0
    
    for skill_name, category in skills_to_fix:
        if fix_skill(skill_name, category):
            fixed_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {fixed_count}/{len(skills_to_fix)}")

if __name__ == "__main__":
    main()
