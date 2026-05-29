#!/usr/bin/env python3
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
