#!/usr/bin/env python3
"""
AI技能库交叉引用链接生成器
为每个技能添加相关技能的超链接
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class LinkGenerator:
    def __init__(self, references_dir="references"):
        self.references_dir = Path(references_dir)
        self.skill_index = {}
        self.build_index()
        
    def build_index(self):
        """构建技能索引"""
        print("构建技能索引...")
        
        for skill_file in self.references_dir.rglob("*.md"):
            if skill_file.name == "README.md":
                continue
                
            rel_path = skill_file.relative_to(self.references_dir)
            category = rel_path.parent.name if rel_path.parent.name else "root"
            
            # 读取YAML frontmatter
            try:
                with open(skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 提取name
                name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
                if name_match:
                    name = name_match.group(1).strip()
                    self.skill_index[name] = {
                        "file": str(rel_path).replace('\\', '/'),
                        "category": category,
                        "path": skill_file
                    }
            except:
                pass
        
        print(f"索引完成: {len(self.skill_index)} 个技能")
        
    def add_links_to_all(self):
        """为所有技能添加链接"""
        print("\n" + "=" * 60)
        print("添加交叉引用链接")
        print("=" * 60)
        
        updated = 0
        
        for skill_file in self.references_dir.rglob("*.md"):
            if skill_file.name == "README.md":
                continue
                
            if self.add_links_to_skill(skill_file):
                updated += 1
                
        print(f"\n更新完成: {updated} 个技能")
        
    def add_links_to_skill(self, skill_file):
        """为单个技能添加链接"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return False
            
        # 提取相关技能
        related_match = re.search(r'^related:\s*(.+)$', content, re.MULTILINE)
        if not related_match:
            return False
            
        related_str = related_match.group(1).strip()
        related_skills = [s.strip() for s in related_str.split(',')]
        
        # 构建链接列表
        links = []
        for skill_name in related_skills:
            if skill_name in self.skill_index:
                skill_info = self.skill_index[skill_name]
                links.append(f"[{skill_name}]({skill_info['file']})")
            else:
                links.append(skill_name)
        
        if not links:
            return False
            
        # 替换相关技能行为链接
        new_related = "related: " + ", ".join(links)
        
        # 替换YAML中的related
        content_new = re.sub(
            r'^related:\s*.+$',
            new_related,
            content,
            flags=re.MULTILINE
        )
        
        # 替换快速参考卡中的相关技能
        # 查找快速参考卡表格中的相关技能行
        quick_ref_pattern = r'(\| \*\*相关技能\*\* \| )(.+?)( \|)'
        
        def replace_quick_ref(match):
            prefix = match.group(1)
            old_value = match.group(2)
            suffix = match.group(3)
            
            # 解析旧值中的技能名称
            old_skills = [s.strip() for s in old_value.split(',')]
            new_links = []
            
            for skill in old_skills:
                skill_clean = re.sub(r'\[|\]', '', skill).strip()
                if skill_clean in self.skill_index:
                    skill_info = self.skill_index[skill_clean]
                    new_links.append(f"[{skill_clean}]({skill_info['file']})")
                else:
                    new_links.append(skill_clean)
            
            return prefix + ", ".join(new_links) + suffix
        
        content_new = re.sub(quick_ref_pattern, replace_quick_ref, content_new)
        
        # 如果内容有变化，写回文件
        if content_new != content:
            try:
                with open(skill_file, 'w', encoding='utf-8') as f:
                    f.write(content_new)
                print(f"OK: {skill_file.name}")
                return True
            except:
                print(f"ERR: {skill_file.name}")
                return False
        
        return False

def main():
    generator = LinkGenerator()
    generator.add_links_to_all()

if __name__ == "__main__":
    main()
