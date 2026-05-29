#!/usr/bin/env python3
"""
批量添加 stability 字段到所有 SKILL.md 文件
在 category 行后添加 stability: stable
"""

import os
import re
from pathlib import Path

def fix_skill_file(skill_path):
    """修复单个技能文件的 stability 字段"""
    skill_md = Path(skill_path) / "SKILL.md"
    
    if not skill_md.exists():
        print(f"[SKIP] {skill_path.name}: SKILL.md not found")
        return False
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有 stability 字段
        if 'stability:' in content:
            print(f"[OK] {skill_path.name}: Already has stability")
            return False
        
        # 在 category 行后添加 stability
        lines = content.split('\n')
        new_lines = []
        added = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            # 在 category 行后添加 stability
            if line.startswith('category:') and not added:
                # 计算缩进
                indent = len(line) - len(line.lstrip())
                new_lines.append(' ' * indent + 'stability: stable')
                added = True
        
        if added:
            with open(skill_md, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            print(f"[FIXED] {skill_path.name}: Added stability field")
            return True
        else:
            print(f"[WARN] {skill_path.name}: Could not find category field")
            return False
            
    except Exception as e:
        print(f"[ERROR] {skill_path.name}: {e}")
        return False

def main():
    skills_dir = Path("skills")
    
    if not skills_dir.exists():
        print("Error: skills/ directory not found")
        return
    
    print("=== Fixing Stability Fields ===\n")
    
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir():
            result = fix_skill_file(skill_dir)
            if result:
                fixed_count += 1
            else:
                skipped_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {fixed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total: {fixed_count + skipped_count}")

if __name__ == "__main__":
    main()
