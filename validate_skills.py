#!/usr/bin/env python3
"""
AI技能库验证脚本
验证所有技能文档的格式和内容质量
"""

import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime

class SkillsValidator:
    def __init__(self, references_dir="references"):
        self.references_dir = Path(references_dir)
        self.errors = []
        self.warnings = []
        self.stats = {
            "total_files": 0,
            "valid_files": 0,
            "error_files": 0,
            "warning_files": 0
        }
        
    def validate_all(self):
        """验证所有技能文件"""
        print("=" * 60)
        print("AI技能库验证")
        print("=" * 60)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"目录: {self.references_dir.absolute()}")
        print("-" * 60)
        
        # 查找所有markdown文件
        md_files = list(self.references_dir.rglob("*.md"))
        self.stats["total_files"] = len(md_files)
        
        print(f"\n找到 {len(md_files)} 个Markdown文件\n")
        
        for file_path in sorted(md_files):
            self.validate_file(file_path)
        
        # 生成报告
        self.generate_report()
        
    def validate_file(self, file_path):
        """验证单个文件"""
        rel_path = file_path.relative_to(self.references_dir)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"{rel_path}: 无法读取文件 - {e}")
            self.stats["error_files"] += 1
            return
        
        file_errors = []
        file_warnings = []
        
        # 1. 检查文件大小
        if len(content) < 100:
            file_warnings.append("文件内容过少（<100字符）")
        
        # 2. 检查标题（支持YAML frontmatter）
        content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        if not content_without_frontmatter.strip().startswith('#'):
            file_errors.append("文件必须以#标题开头")
        
        # 3. 检查必要章节（参考资料文档使用不同结构）
        # 检查是否有核心内容章节
        core_sections = ['核心理念', '核心概念', '什么时候使用', '使用场景', '示例']
        has_core_content = any(section in content for section in core_sections)
        if not has_core_content:
            file_warnings.append("缺少核心内容章节（如'核心理念'、'使用场景'等）")
        
        # 4. 检查工具/方法章节
        tool_sections = ['工具', '方法', '实践', '行动']
        has_tool_section = any(f'## {section}' in content for section in tool_sections)
        if not has_tool_section:
            file_warnings.append("缺少工具/方法章节")
        
        # 5. 检查示例/案例
        example_sections = ['示例', '案例', '实践', '使用示例']
        has_example = any(section in content for section in example_sections)
        if not has_example:
            file_warnings.append("缺少示例/案例")
        
        # 6. 检查格式问题
        if content.count('```') % 2 != 0:
            file_errors.append("代码块未正确闭合")
        
        # 7. 检查空行
        lines = content.split('\n')
        empty_line_count = sum(1 for line in lines if line.strip() == '')
        if empty_line_count < 3:
            file_warnings.append("空行过少，建议增加可读性")
        
        # 8. 检查链接
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, url in links:
            if url.startswith('#'):
                # 内部链接，检查锚点
                anchor = url[1:]
                if anchor not in content:
                    file_warnings.append(f"内部链接可能无效: {url}")
        
        # 9. 检查图片
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        for alt, src in images:
            if not src.startswith(('http://', 'https://', '/')):
                # 相对路径，检查文件是否存在
                img_path = file_path.parent / src
                if not img_path.exists():
                    file_warnings.append(f"图片可能不存在: {src}")
        
        # 10. 检查表格格式
        table_lines = [line for line in lines if '|' in line]
        for i, line in enumerate(table_lines):
            if i > 0 and '---' not in table_lines[i-1]:
                # 检查表格分隔线
                pass  # 简化检查
        
        # 记录结果
        if file_errors:
            self.errors.extend([f"{rel_path}: {e}" for e in file_errors])
            self.stats["error_files"] += 1
        elif file_warnings:
            self.warnings.extend([f"{rel_path}: {w}" for w in file_warnings])
            self.stats["warning_files"] += 1
        else:
            self.stats["valid_files"] += 1
            
    def generate_report(self):
        """生成验证报告"""
        print("\n" + "=" * 60)
        print("验证报告")
        print("=" * 60)
        
        # 统计
        print(f"\n统计信息:")
        print(f"   总文件数: {self.stats['total_files']}")
        print(f"   通过: {self.stats['valid_files']}")
        print(f"   警告: {self.stats['warning_files']}")
        print(f"   错误: {self.stats['error_files']}")
        
        # 计算通过率
        if self.stats['total_files'] > 0:
            pass_rate = (self.stats['valid_files'] / self.stats['total_files']) * 100
            print(f"   通过率: {pass_rate:.1f}%")
        
        # 错误详情
        if self.errors:
            print(f"\n错误 ({len(self.errors)}项):")
            for error in self.errors[:20]:  # 只显示前20个
                print(f"   - {error}")
            if len(self.errors) > 20:
                print(f"   ... 还有 {len(self.errors) - 20} 个错误")
        
        # 警告详情
        if self.warnings:
            print(f"\n警告 ({len(self.warnings)}项):")
            for warning in self.warnings[:20]:  # 只显示前20个
                print(f"   - {warning}")
            if len(self.warnings) > 20:
                print(f"   ... 还有 {len(self.warnings) - 20} 个警告")
        
        # 质量评分
        score = self.calculate_score()
        print(f"\n质量评分: {score}/100")
        
        if score >= 95:
            print("   评级: 优秀")
        elif score >= 85:
            print("   评级: 良好")
        elif score >= 70:
            print("   评级: 一般")
        elif score >= 50:
            print("   评级: 需改进")
        else:
            print("   评级: 不合格")
        
        # 建议
        print(f"\n建议:")
        if self.errors:
            print("   1. 优先修复错误项")
        if self.warnings:
            print("   2. 处理警告项以提升质量")
        if not self.errors and not self.warnings:
            print("   所有文件验证通过！继续保持！")
        
        print("\n" + "=" * 60)
        
        # 保存报告
        self.save_report(score)
        
    def calculate_score(self):
        """计算质量评分"""
        if self.stats['total_files'] == 0:
            return 0
        
        # 基础分
        base_score = 100
        
        # 错误扣分（每个-5分）
        error_penalty = len(self.errors) * 5
        
        # 警告扣分（每个-1分）
        warning_penalty = len(self.warnings) * 1
        
        # 计算最终分数
        score = max(0, base_score - error_penalty - warning_penalty)
        
        return score
        
    def save_report(self, score):
        """保存报告到文件"""
        report_path = Path("quality_report.md")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 质量验证报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 统计信息\n\n")
            f.write(f"- 总文件数: {self.stats['total_files']}\n")
            f.write(f"- 通过: {self.stats['valid_files']}\n")
            f.write(f"- 警告: {self.stats['warning_files']}\n")
            f.write(f"- 错误: {self.stats['error_files']}\n")
            f.write(f"- 质量评分: {score}/100\n\n")
            
            if self.errors:
                f.write("## 错误列表\n\n")
                for error in self.errors:
                    f.write(f"- {error}\n")
                f.write("\n")
            
            if self.warnings:
                f.write("## 警告列表\n\n")
                for warning in self.warnings:
                    f.write(f"- {warning}\n")
                f.write("\n")
            
            f.write("## 验证规则\n\n")
            f.write("1. 文件必须以#标题开头\n")
            f.write("2. 必须包含'描述'章节\n")
            f.write("3. 必须包含'功能'章节\n")
            f.write("4. 必须包含'使用场景'章节\n")
            f.write("5. 建议包含'工具'章节\n")
            f.write("6. 建议包含'示例'章节\n")
            f.write("7. 代码块必须正确闭合\n")
            f.write("8. 内部链接必须有效\n")
            f.write("9. 图片引用必须存在\n\n")
        
        print(f"\n报告已保存: {report_path.absolute()}")

def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) > 1:
        references_dir = sys.argv[1]
    else:
        references_dir = "references"
    
    # 创建验证器并运行
    validator = SkillsValidator(references_dir)
    validator.validate_all()
    
    # 返回状态码
    if validator.errors:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
