#!/usr/bin/env python3
"""
AI技能库案例定制化脚本
为每个类别生成特定的案例内容
"""

import os
import re
from pathlib import Path
from datetime import datetime

class CaseCustomizer:
    def __init__(self, references_dir="references"):
        self.references_dir = Path(references_dir)
        
        # 类别特定的案例模板
        self.category_cases = {
            "category-01-human-value": {
                "case1": {
                    "title": "从执行者到需求表达者的转型",
                    "background": "小李是一名5年经验的设计师，AI绘图工具的出现让他感到焦虑，担心自己的技能被替代。",
                    "process": "通过'AI时代人类价值'技能的学习，他意识到自己从'会设计'转向'知道自己想要什么设计'。开始练习向AI提出精确的设计需求，并加入个人独特审美判断。",
                    "result": "3个月后，他成为团队中最会用AI工具的人，效率提升5倍，薪资上涨30%。",
                    "insight": "AI替代的是执行，但无法替代人的审美判断和需求表达能力。"
                },
                "case2": {
                    "title": "构建个人独特世界",
                    "background": "小王是一名内容创作者，感到自己的内容同质化严重，缺乏独特性。",
                    "process": "运用'个人独特性构建'技能，他开始系统记录自己的生活经历、独特观点和情感体验，形成独特的'内在世界'。",
                    "result": "6个月后，他的内容辨识度大幅提升，粉丝增长300%，接到品牌合作邀约。",
                    "insight": "独特性来自真实的生活体验和深度的自我认知，而非技巧堆砌。"
                }
            },
            "category-02-career-transition": {
                "case1": {
                    "title": "AI替代焦虑的化解",
                    "background": "小张是一名文案策划，看到AI写作工具后担心被裁员，陷入焦虑。",
                    "process": "通过'AI替代边界'技能分析，他认识到AI擅长套路化写作，但不擅长创意策略和情感共鸣。他转向更高端的品牌策略工作。",
                    "result": "成功转型为品牌策略师，薪资提升40%，工作更有创造性。",
                    "insight": "与其对抗AI，不如找到AI无法替代的高价值工作。"
                },
                "case2": {
                    "title": "人机协作效率提升",
                    "background": "某市场团队10人，每天处理大量数据分析报告，工作繁重。",
                    "process": "引入AI工具后，通过'AI工具人机共生'技能指导，重新设计工作流程：AI处理数据，人做洞察分析。",
                    "result": "报告产出时间从3天缩短到4小时，团队可以专注于策略建议，客户满意度提升50%。",
                    "insight": "人机协作的关键是明确分工：AI做计算，人做判断。"
                }
            },
            "category-03-professional-redefinition": {
                "case1": {
                    "title": "从专家到AI协作专家",
                    "background": "老刘是资深财务分析师，专业技能强但学习新工具慢。",
                    "process": "运用'AI时代专业重定义'技能，他将专业知识与AI工具结合，成为'AI财务分析专家'。",
                    "result": "分析效率提升10倍，能处理更复杂的预测模型，成为公司不可或缺的专家。",
                    "insight": "专业价值不在于会多少工具，而在于如何用工具解决复杂问题。"
                },
                "case2": {
                    "title": "一人团队创业成功",
                    "background": "小陈想创业但资金有限，无法组建团队。",
                    "process": "通过'AI一人团队'技能，他用AI工具替代设计师、文案、客服等角色，自己专注产品和策略。",
                    "result": "3个月内产品上线，首月营收5万，成本仅为传统创业的10%。",
                    "insight": "AI让个人创业门槛大幅降低，一人可以抵过去一个团队。"
                }
            },
            "category-04-brand-growth": {
                "case1": {
                    "title": "AI赋能品牌内容矩阵",
                    "background": "某新消费品牌内容团队3人，需覆盖5个平台，产能严重不足。",
                    "process": "运用'AI创意协同框架'，建立AI内容工厂：AI生成初稿，人工优化调性，批量生产适配各平台的内容。",
                    "result": "内容产量提升10倍，覆盖平台从5个扩展到12个，粉丝增长200%。",
                    "insight": "AI不是替代创意，而是放大创意产能。"
                },
                "case2": {
                    "title": "数据驱动的精准营销",
                    "background": "某品牌广告投放ROI持续下降，获客成本越来越高。",
                    "process": "通过'品牌数据平台建设'，整合用户数据，用AI分析高价值用户特征，精准定向投放。",
                    "result": "获客成本降低60%，转化率提升3倍，ROI从1:2提升到1:5。",
                    "insight": "数据+AI让营销从'广撒网'变成'精准狙击'。"
                }
            },
            "category-05-consumption-market": {
                "case1": {
                    "title": "AI Agent客服升级",
                    "background": "某电商客服团队20人，每天处理5000+咨询，响应慢、满意度低。",
                    "process": "部署AI Agent客服，通过'AI Agent运营框架'设计多轮对话流程，处理80%常见问题。",
                    "result": "响应时间从5分钟缩短到10秒，满意度从70%提升到92%，人工客服专注处理复杂问题。",
                    "insight": "AI Agent不是替代人工，而是让人做更有价值的服务。"
                },
                "case2": {
                    "title": "物理AI产品落地",
                    "background": "某智能家居公司开发AI助手，但用户接受度低。",
                    "process": "运用'物理AI落地策略'，重新设计产品：从'功能导向'转向'场景导向'，聚焦3个高频场景做透。",
                    "result": "用户日活提升5倍，NPS评分从30提升到65，成为品类爆款。",
                    "insight": "物理AI成功的关键是找到真实场景，而非堆砌功能。"
                }
            },
            "category-06-ai-companion": {
                "case1": {
                    "title": "情感陪伴机器人设计",
                    "background": "某团队开发AI陪伴机器人，但用户留存率仅10%。",
                    "process": "运用'AI陪伴机器人框架'，重新设计：增加情感记忆、个性化成长、主动关怀机制。",
                    "result": "留存率提升到65%，用户平均使用时长从5分钟提升到45分钟。",
                    "insight": "陪伴不只是对话，而是建立情感连接和记忆。"
                },
                "case2": {
                    "title": "第二增长曲线探索",
                    "background": "某硬件公司主营业务增长停滞，寻找新增长点。",
                    "process": "通过'AI第二增长曲线策略'，分析核心能力（硬件+渠道），切入AI陪伴硬件赛道。",
                    "result": "新产品线6个月营收破亿，成为公司增长引擎。",
                    "insight": "第二曲线应基于核心能力，而非盲目追风口。"
                }
            },
            "category-07-digital-ip": {
                "case1": {
                    "title": "AI辅助IP创作流水线",
                    "background": "某IP创作者每月产出2个作品，产能受限，难以规模化。",
                    "process": "建立'AI赋能IP创作流水线'：AI辅助概念设计、初稿生成，人做创意把控和精修。",
                    "result": "月产出提升到15个作品，IP授权收入增长5倍。",
                    "insight": "AI让IP创作从'手工作坊'变成'内容工厂'。"
                },
                "case2": {
                    "title": "IP品牌协同共振",
                    "background": "某IP有粉丝但变现困难，品牌合作效果差。",
                    "process": "运用'IP品牌协同共振方法论'，筛选与IP调性匹配的品牌，设计深度联名而非简单贴牌。",
                    "result": "品牌合作满意度提升，单次合作收入从10万提升到100万，粉丝不反感。",
                    "insight": "IP变现的关键是'调性匹配'，而非流量堆砌。"
                }
            },
            "category-08-industry-competition": {
                "case1": {
                    "title": "机会窗口精准把握",
                    "background": "某公司看到AI风口想入局，但不知从何切入。",
                    "process": "运用'机会窗口策略'，分析技术成熟度、市场需求、竞争格局，选择'AI+教育'细分赛道。",
                    "result": "提前6个月进入市场，成为细分赛道头部，占据40%市场份额。",
                    "insight": "机会窗口的判断需要数据支撑，而非凭感觉。"
                },
                "case2": {
                    "title": "全栈竞争壁垒构建",
                    "background": "某AI创业公司技术强但易被模仿，竞争压力大。",
                    "process": "通过'全栈竞争框架'，构建'技术+数据+场景+服务'全栈能力，形成复合壁垒。",
                    "result": "竞争对手难以复制，客户粘性高，续约率95%，估值提升3倍。",
                    "insight": "单点优势易被模仿，全栈能力才是护城河。"
                }
            },
            "category-09-embodied-ai": {
                "case1": {
                    "title": "端到端服务设计优化",
                    "background": "某机器人公司产品销售好但口碑差，用户不会用、售后问题多。",
                    "process": "运用'端到端服务设计'，重新设计全流程：售前咨询、安装指导、使用培训、售后支持。",
                    "result": "NPS从20提升到60，复购率提升3倍，客服工单减少70%。",
                    "insight": "硬件产品竞争的是全链路体验，而非单一功能。"
                },
                "case2": {
                    "title": "技术商业化时机把握",
                    "background": "某团队有领先技术，但过早商业化失败，过晚又错失机会。",
                    "process": "通过'技术商业化时机'分析，等待技术成熟度达到'可用'标准，同时储备渠道资源。",
                    "result": "在最佳时机入场，产品一推出即成为品类标杆。",
                    "insight": "技术商业化需要'技术成熟度'和'市场准备度'双匹配。"
                }
            },
            "category-10-llm-tech": {
                "case1": {
                    "title": "模型评估体系建立",
                    "background": "某公司选型大模型，被厂商宣传迷惑，不知如何选择。",
                    "process": "建立'AI模型评估系统'，从准确性、速度、成本、安全等维度实测对比。",
                    "result": "选择最适合业务场景的模型，成本降低50%，效果提升30%。",
                    "insight": "模型选择应基于实测数据，而非厂商宣传。"
                },
                "case2": {
                    "title": "强化学习应用落地",
                    "background": "某团队尝试RLHF训练模型，但效果不佳，投入产出比低。",
                    "process": "运用'强化学习应用'技能，优化奖励函数设计，引入人类反馈闭环。",
                    "result": "模型对齐度提升，用户满意度从60%提升到85%，训练成本降低40%。",
                    "insight": "强化学习成功的关键是奖励函数设计和反馈质量。"
                }
            },
            "category-11-startup": {
                "case1": {
                    "title": "创业动机深度检验",
                    "background": "某创业者因'不想上班'创业，6个月后失败，负债20万。",
                    "process": "回顾'AI创业动机'技能，认识到自己是'逃避型动机'，未做好充分准备。",
                    "result": "第二次创业前充分准备，明确使命型动机，目前公司估值过亿。",
                    "insight": "错误的动机是创业失败的最大原因。"
                },
                "case2": {
                    "title": "规模化能力建设",
                    "background": "某创业公司产品好但扩张慢，每次扩团队就出问题。",
                    "process": "运用'规模化能力建设'，建立标准化流程、人才培养体系、文化沉淀机制。",
                    "result": "团队从20人扩展到200人，效率不降反升，成功完成B轮融资。",
                    "insight": "规模化需要系统能力，而非简单堆人。"
                }
            },
            "category-12-core-methodology": {
                "case1": {
                    "title": "PBL学习方法实践",
                    "background": "某员工学习AI工具，看了一堆教程还是不会用。",
                    "process": "运用'PBL AI学习'方法，以实际项目驱动学习，边做边学，遇到问题再查资料。",
                    "result": "2周内独立完成3个AI辅助项目，学习效率提升5倍。",
                    "insight": "项目驱动学习比被动听课效率高得多。"
                },
                "case2": {
                    "title": "成功发布方法论",
                    "background": "某产品功能完善但发布后市场反响平平。",
                    "process": "运用'成功发布方法'，提前3个月预热，找种子用户验证，分阶段 rollout。",
                    "result": "发布首周用户破万，媒体报道30+篇，成为行业热点。",
                    "insight": "产品发布是系统工程，不只是上线那一刻。"
                }
            },
            "category-13-app-design": {
                "case1": {
                    "title": "教育AI产品设计",
                    "background": "某教育AI产品功能强大但学生不爱用，完课率低。",
                    "process": "运用'教育AI设计'原则，增加游戏化元素、社交互动、个性化路径。",
                    "result": "完课率从30%提升到75%，用户好评率90%+。",
                    "insight": "教育产品要'有效'更要'有趣'，学习动力是关键。"
                },
                "case2": {
                    "title": "情感AI陪伴设计",
                    "background": "某情感AI助手用户觉得'假'，不愿深度交流。",
                    "process": "运用'情感AI陪伴'设计，增加记忆连续性、情感共鸣、适度脆弱性。",
                    "result": "用户平均对话轮数从5轮提升到25轮，愿意分享真实情感。",
                    "insight": "情感AI需要'真实感'而非'完美感'。"
                }
            },
            "category-14-community": {
                "case1": {
                    "title": "AI社区建设",
                    "background": "某AI工具用户分散，缺乏交流，活跃度低。",
                    "process": "运用'AI社区建设者'技能，建立分层社区：新手区、进阶区、专家区，设计贡献激励机制。",
                    "result": "社区活跃度提升10倍，用户自发产生内容占比60%，获客成本降低70%。",
                    "insight": "社区是产品的护城河，用户是最好的布道者。"
                },
                "case2": {
                    "title": "青年AI创作者培养",
                    "background": "某平台想培养年轻AI创作者，但缺乏系统方法。",
                    "process": "运用'青年AI创作者指南'，设计学习路径、项目实战、导师对接、作品展示全链路。",
                    "result": "3个月培养100+优质创作者，平台内容产量提升3倍。",
                    "insight": "创作者培养需要'技能+项目+反馈'闭环。"
                }
            },
            "category-15-industry-analysis": {
                "case1": {
                    "title": "AI赛道精准选择",
                    "background": "某基金想投AI但不知哪个细分赛道有机会。",
                    "process": "运用'AI赛道选择'框架，分析技术成熟度、市场规模、竞争格局、团队能力匹配度。",
                    "result": "成功投资3个细分赛道头部项目，IRR达到80%。",
                    "insight": "赛道选择需要多维分析，而非追热点。"
                },
                "case2": {
                    "title": "泡沫判断与退出",
                    "background": "某公司估值暴涨，创始人犹豫是否该融资或退出。",
                    "process": "运用'泡沫判断框架'，分析估值合理性、收入质量、竞争态势，判断处于泡沫期。",
                    "result": "在高点完成融资，18个月后市场回调，公司有足够资金过冬。",
                    "insight": "泡沫期是融资窗口，但要有过冬准备。"
                }
            }
        }
        
    def customize_all(self):
        """批量定制所有技能案例"""
        print("=" * 60)
        print("AI技能库案例定制化")
        print("=" * 60)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # 按类别处理
        for category_dir in sorted(self.references_dir.glob("category-*")):
            if category_dir.is_dir():
                self.customize_category(category_dir)
        
        print("\n" + "=" * 60)
        print("案例定制化完成")
        print("=" * 60)
        
    def customize_category(self, category_dir):
        """定制单个类别的案例"""
        category_name = category_dir.name
        
        if category_name not in self.category_cases:
            print(f"跳过: {category_name} (无定制模板)")
            return
            
        cases = self.category_cases[category_name]
        print(f"\n处理: {category_name}")
        
        # 处理该类别下的所有技能
        for skill_file in sorted(category_dir.glob("*.md")):
            self.customize_skill(skill_file, cases)
            
    def customize_skill(self, skill_file, cases):
        """定制单个技能的案例"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  ERR: {skill_file.name} - 读取失败")
            return
        
        # 替换通用案例为定制案例
        customized = self.replace_cases(content, cases)
        
        # 写回文件
        try:
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(customized)
            print(f"  OK: {skill_file.name}")
        except Exception as e:
            print(f"  ERR: {skill_file.name} - 写入失败")
            
    def replace_cases(self, content, cases):
        """替换案例内容"""
        # 替换案例一
        content = re.sub(
            r'### 案例一：.*?\n\*\*背景\*\*: .*?\n\*\*过程\*\*: .*?\n\*\*结果\*\*: .*?\n\*\*启示\*\*: .*?(?=\n\n### 案例二|$)',
            f"### 案例一：{cases['case1']['title']}\n"
            f"**背景**: {cases['case1']['background']}\n"
            f"**过程**: {cases['case1']['process']}\n"
            f"**结果**: {cases['case1']['result']}\n"
            f"**启示**: {cases['case1']['insight']}\n",
            content,
            flags=re.DOTALL
        )
        
        # 替换案例二
        content = re.sub(
            r'### 案例二：.*?\n\*\*背景\*\*: .*?\n\*\*过程\*\*: .*?\n\*\*结果\*\*: .*?\n\*\*启示\*\*: .*?(?=\n\n---|$)',
            f"### 案例二：{cases['case2']['title']}\n"
            f"**背景**: {cases['case2']['background']}\n"
            f"**过程**: {cases['case2']['process']}\n"
            f"**结果**: {cases['case2']['result']}\n"
            f"**启示**: {cases['case2']['insight']}\n",
            content,
            flags=re.DOTALL
        )
        
        return content

def main():
    customizer = CaseCustomizer()
    customizer.customize_all()

if __name__ == "__main__":
    main()
