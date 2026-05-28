#!/usr/bin/env python3
"""
整合版技能验证脚本
结合agent-scripts的validate-skills和现有验证逻辑
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional

# 尝试导入yaml，如果没有则使用简单解析
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("警告: 未安装PyYAML，使用简化YAML解析")

class SkillValidator:
    """技能验证器 - 整合版"""
    
    def __init__(self, skills_dir: str = "references"):
        self.skills_dir = Path(skills_dir)
        self.errors: List[Tuple[str, str]] = []
        self.warnings: List[Tuple[str, str]] = []
        self.names: Dict[str, str] = {}
        self.stats = {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "warnings": 0
        }
    
    def load_front_matter(self, path: Path, content: str) -> Tuple[Optional[Dict], Optional[str]]:
        """加载YAML front matter"""
        # 检查front matter格式
        match = re.match(r'^---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\z)', content, re.DOTALL)
        if not match:
            return None, "front matter必须从第一行开始并以---结束"
        
        yaml_text = match.group(1)
        
        if HAS_YAML:
            try:
                data = yaml.safe_load(yaml_text)
            except Exception as e:
                return None, f"YAML语法错误: {e}"
        else:
            # 简化解析：提取key: value对
            data = {}
            for line in yaml_text.split('\n'):
                line = line.strip()
                if ':' in line and not line.startswith('#'):
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    if value:
                        data[key] = value
        
        if not isinstance(data, dict):
            return None, "front matter必须是YAML映射（键值对）"
        
        return data, None
    
    def validate_required_fields(self, path: Path, data: Dict) -> bool:
        """验证必需字段"""
        required_fields = ['name', 'description', 'version']
        valid = True
        
        for field in required_fields:
            value = data.get(field)
            if not isinstance(value, str) or not value.strip():
                self.errors.append((str(path), f"缺少非空字符串字段: {field}"))
                valid = False
        
        return valid
    
    def validate_optional_fields(self, path: Path, data: Dict) -> None:
        """验证可选字段"""
        # 检查stability
        stability = data.get('stability')
        if stability and stability not in ['stable', 'experimental', 'deprecated']:
            self.warnings.append((str(path), f"stability建议使用: stable/experimental/deprecated"))
        
        # 检查aliases
        aliases = data.get('aliases')
        if aliases and not isinstance(aliases, list):
            self.warnings.append((str(path), "aliases应该是字符串数组"))
        
        # 检查last_updated
        last_updated = data.get('last_updated')
        if last_updated and not re.match(r'^\d{4}-\d{2}-\d{2}$', str(last_updated)):
            self.warnings.append((str(path), "last_updated建议使用YYYY-MM-DD格式"))
    
    def check_duplicate_names(self, path: Path, data: Dict) -> bool:
        """检查重复名称"""
        name = data.get('name', '').strip()
        if not name:
            return True
        
        if name in self.names:
            self.errors.append((
                str(path),
                f"重复的技能名称 '{name}'，也用于 {self.names[name]}"
            ))
            return False
        
        self.names[name] = str(path)
        return True
    
    def validate_content_structure(self, path: Path, content: str) -> None:
        """验证内容结构"""
        # 检查是否有二级标题
        if not re.search(r'^## ', content, re.MULTILINE):
            self.warnings.append((str(path), "建议添加二级标题(##)组织内容"))
        
        # 检查代码示例
        code_blocks = len(re.findall(r'```[\w]*\n', content))
        if code_blocks == 0:
            self.warnings.append((str(path), "建议添加代码示例"))
        
        # 检查表格
        tables = len(re.findall(r'\|.*\|.*\|', content))
        if tables == 0:
            self.warnings.append((str(path), "建议添加表格增强可读性"))
    
    def validate_skill(self, path: Path) -> bool:
        """验证单个技能"""
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append((str(path), f"无法读取文件: {e}"))
            return False
        
        # 加载front matter
        data, error = self.load_front_matter(path, content)
        if error:
            self.errors.append((str(path), error))
            return False
        
        # 验证必需字段
        if not self.validate_required_fields(path, data):
            return False
        
        # 验证可选字段
        self.validate_optional_fields(path, data)
        
        # 检查重复名称
        if not self.check_duplicate_names(path, data):
            return False
        
        # 验证内容结构
        self.validate_content_structure(path, content)
        
        return True
    
    def validate_all(self) -> bool:
        """验证所有技能"""
        # 查找所有.md文件（您的技能库结构）
        skill_files = list(self.skills_dir.rglob("*.md"))
        # 排除README和索引文件
        skill_files = [f for f in skill_files if f.name not in ['README.md', 'SKILL.md', 'quality_report.md', 'USER_GUIDE.md', 'QUICK_START.md', 'EXAMPLES.md', 'ADVANCED_FEATURES.md']]
        skill_files.sort()
        
        if not skill_files:
            print(f"警告: 在 {self.skills_dir} 中未找到技能文件")
            return True
        
        self.stats["total"] = len(skill_files)
        
        for path in skill_files:
            if self.validate_skill(path):
                self.stats["valid"] += 1
            else:
                self.stats["invalid"] += 1
        
        self.stats["warnings"] = len(self.warnings)
        
        return self.stats["invalid"] == 0
    
    def print_report(self) -> None:
        """打印验证报告"""
        print("=" * 70)
        print("技能验证报告")
        print("=" * 70)
        
        # 统计信息
        print(f"\n统计:")
        print(f"  总技能数: {self.stats['total']}")
        print(f"  有效: {self.stats['valid']} [OK]")
        print(f"  无效: {self.stats['invalid']} [FAIL]")
        print(f"  警告: {self.stats['warnings']} [WARN]")
        
        # 错误详情
        if self.errors:
            print(f"\n错误 ({len(self.errors)}):")
            for path, error in self.errors:
                print(f"  [FAIL] {path}")
                print(f"     -> {error}")
        
        # 警告详情
        if self.warnings:
            print(f"\n警告 ({len(self.warnings)}):")
            for path, warning in self.warnings[:20]:  # 最多显示20个
                print(f"  [WARN] {path}")
                print(f"     -> {warning}")
            if len(self.warnings) > 20:
                print(f"  ... 还有 {len(self.warnings) - 20} 个警告")
        
        # 总结
        print("\n" + "=" * 70)
        if self.stats["invalid"] == 0:
            print("[OK] 所有技能验证通过！")
            if self.warnings:
                print(f"[WARN] 但有 {len(self.warnings)} 个警告需要关注")
        else:
            print(f"[FAIL] 验证失败: {self.stats['invalid']} 个技能存在问题")
        print("=" * 70)

def main():
    """主函数"""
    # 支持命令行参数指定目录
    skills_dir = sys.argv[1] if len(sys.argv) > 1 else "references"
    
    validator = SkillValidator(skills_dir)
    success = validator.validate_all()
    validator.print_report()
    
    # 返回退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
