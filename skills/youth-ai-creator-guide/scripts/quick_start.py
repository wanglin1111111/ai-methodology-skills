#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import datetime
import json


def display_banner():
    print("="*60)
    print("青少年AI创作指南 - 快速开始")
    print("="*60)


def show_intro():
    print("\n欢迎来到AI创作的世界！")
    print("在这里，你将学习如何用AI工具创造有趣的作品。\n")
    print("你将学习到：")
    print("  - AI是什么以及如何工作")
    print("  - 如何创建你的第一个AI作品")
    print("  - 如何不断改进你的作品")
    print("  - 如何分享和展示你的创作\n")


def show_learning_path():
    print("="*60)
    print("学习路径")
    print("="*60 + "\n")
    
    stages = [
        ("启蒙期", "0-100小时", "了解AI，创建第一个作品"),
        ("成长期", "100-500小时", "掌握更多工具，创作更复杂作品"),
        ("突破期", "500-1000小时", "产出有影响力的作品"),
        ("成熟期", "1000+小时", "成为AI创作领域的专家"),
    ]
    
    for i, (stage, hours, goal) in enumerate(stages, 1):
        print(f"{i}. {stage} ({hours})")
        print(f"   目标: {goal}\n")


def show_quick_start():
    print("="*60)
    print("快速开始：创建你的第一个AI作品")
    print("="*60 + "\n")
    
    steps = [
        ("选择平台", "选择一个AI创作平台开始"),
        ("选择模板", "选择一个简单的模板开始"),
        ("修改定制", "修改模板让它变成'你的'"),
        ("测试作品", "测试你的作品是否正常工作"),
        ("分享作品", "分享给朋友或家人"),
    ]
    
    for i, (title, desc) in enumerate(steps, 1):
        print(f"  {i}. {title}")
        print(f"     -> {desc}\n")


def show_motivation():
    print("="*60)
    print("记住：每个大师都曾是新手")
    print("="*60 + "\n")
    
    tips = [
        "不要害怕犯错，错误是学习的一部分",
        "遇到困难时，分解问题，一步一步解决",
        "保持好奇心，享受创作的过程",
        "和他人分享你的作品，获得反馈和鼓励",
        "最重要的是：开始行动！",
    ]
    
    for tip in tips:
        print(f"  - {tip}")
    
    print()


def create_project_template():
    template = {
        "project_name": "我的第一个AI作品",
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "goals": "描述你的创作目标",
        "problems_solved": "这个作品解决了什么问题",
        "features": ["功能1", "功能2", "功能3"],
        "learning_points": "学习到的技能和知识",
        "next_steps": "下一步要做什么",
        "difficulties": "遇到的困难",
        "solutions": "如何解决的",
    }
    
    print("创建项目记录模板...")
    print(json.dumps(template, ensure_ascii=False, indent=2))
    
    return template


def main():
    display_banner()
    show_intro()
    show_learning_path()
    show_quick_start()
    show_motivation()
    create_project_template()
    
    print("\n" + "="*60)
    print("准备开始你的AI创作之旅！")
    print("="*60 + "\n")
    print("提示：查看SKILL.md获取完整的学习指南\n")


if __name__ == "__main__":
    main()
