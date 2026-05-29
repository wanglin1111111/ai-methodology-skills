@echo off
echo === Merging ai-startup-* skills ===
cd /d %~dp0

set target=skills\ai-startup-foundation

echo [1/5] Creating new skill directory...
if not exist "%target%" mkdir "%target%"

echo [2/5] Creating merged SKILL.md...
(
echo ---
echo name: ai-startup-foundation
echo version: 1.0.0
echo author: Anonymous Startup Mentor
echo license: MIT
echo description: |
echo   AI创业基础框架，整合创业动机、常见挑战与风险管理。
echo   为AI时代创业者提供从心理准备到风险控制的完整入门指南。
echo   
echo   触发场景：
echo   - 考虑AI创业但不确定是否适合
echo   - 需要了解AI创业的常见挑战
echo   - 想要建立风险管理意识
echo   - 寻求创业动机与持续动力
echo   
echo   触发词：AI创业、创业准备、风险管理、创业动机、创业挑战
echo keywords:
echo   - ai-startup
echo   - startup-foundation
echo   - entrepreneurship
echo   - risk-management
echo   - startup-motivation
echo   - startup-challenges
echo category: startup
echo ---
echo.
echo # AI Startup Foundation
echo.
echo ^> AI创业基础框架 - 从动机到风险管理的完整指南
echo.
echo ## 模块一：创业动机与心理准备
echo.
echo ### 1.1 为什么创业
echo.
echo **核心问题**：你为什么要创业？
echo.
echo | 动机类型 | 健康度 | 建议 |
echo |---------|--------|------|
echo | 解决问题 | 高 | 最佳动机，持续驱动力 |
echo | 追求自由 | 中 | 需了解创业的真实约束 |
echo | 赚钱致富 | 低 | 失败率高，难以持续 |
echo | 跟风趋势 | 低 | 缺乏核心竞争力 |
echo.
echo ### 1.2 创业者心理特质
echo.
echo **必备特质**：
echo - 抗压能力：能承受不确定性和失败
echo - 学习能力：快速适应市场变化
echo - 执行力：将想法转化为行动
echo - 韧性：从失败中快速恢复
echo.
echo ## 模块二：AI创业常见挑战
echo.
echo ### 2.1 技术挑战
echo.
echo | 挑战 | 描述 | 应对策略 |
echo |------|------|---------|
echo | 技术迭代快 | AI技术更新迅速 | 建立持续学习机制 |
echo | 算力成本高 | 模型训练需要大量资源 | 优先使用API，后期自建 |
echo | 人才稀缺 | AI人才供不应求 | 远程协作，培养内部人才 |
echo.
echo ### 2.2 市场挑战
echo.
echo - **用户教育成本**：AI产品需要更多用户教育
echo - **信任建立**：用户对AI的接受度需要时间
echo - **竞争加剧**：大公司和创业公司同台竞争
echo.
echo ### 2.3 资源挑战
echo.
echo ```
echo 资金：AI创业通常需要更多前期投入
echo 时间：产品迭代周期可能更长
echo 团队：需要跨学科人才（技术+产品+领域）
echo ```
echo.
echo ## 模块三：风险管理框架
echo.
echo ### 3.1 风险识别
echo.
echo **常见风险类型**：
echo 1. **技术风险**：模型效果不达预期
echo 2. **市场风险**：需求验证失败
echo 3. **团队风险**：核心人员流失
echo 4. **资金风险**：现金流断裂
echo 5. **合规风险**：AI监管政策变化
echo.
echo ### 3.2 风险评估矩阵
echo.
echo | 风险 | 概率 | 影响 | 优先级 |
echo |------|------|------|--------|
echo | 技术失败 | 中 | 高 | P1 |
echo | 市场不接受 | 高 | 高 | P1 |
echo | 资金耗尽 | 中 | 高 | P1 |
echo | 团队分裂 | 低 | 高 | P2 |
echo | 政策变化 | 低 | 中 | P3 |
echo.
echo ### 3.3 风险缓解策略
echo.
echo **技术风险**：
echo - MVP验证：快速验证核心假设
echo - 技术储备：保持技术多样性
echo - 外部合作：与研究机构合作
echo.
echo **市场风险**：
echo - 早期用户：找到愿意尝试的早期用户
echo - 快速迭代：根据反馈快速调整
echo - 细分市场：从细分市场切入
echo.
echo **资金风险**：
echo - 精益创业：最小化前期投入
echo - 多元收入：不要依赖单一收入来源
echo - 融资准备：保持融资能力和备选方案
echo.
echo ## 快速启动清单
echo.
echo ### 创业前自检
echo - [ ] 明确创业动机（非跟风）
echo - [ ] 评估个人心理特质
echo - [ ] 识别并评估主要风险
echo - [ ] 准备风险缓解方案
echo - [ ] 确保6个月生活费用储备
echo - [ ] 找到至少一个早期用户
echo - [ ] 完成MVP设计
echo.
echo ### 第一个月行动计划
echo - [ ] 深入访谈10个目标用户
echo - [ ] 验证核心假设
echo - [ ] 构建MVP
echo - [ ] 获取首批反馈
echo - [ ] 调整方向或坚持
echo.
echo ## 相关技能
echo.
echo - [ai-era-career-transition](ai-era-career-transition) - 职业转型指南
echo - [one-person-team-with-ai](one-person-team-with-ai) - 一人团队方法论
echo - [vertical-ai-startup-guide](vertical-ai-startup-guide) - 垂直领域AI创业
echo - [founder-action-guide](founder-action-guide) - 创始人行动指南
echo.
echo ---
echo *本技能整合了 ai-startup-motivation, ai-startup-challenges, ai-startup-risk-management 的内容*
) > "%target%\SKILL.md"

echo [3/5] Creating metadata.json...
(
echo {
echo   "name": "ai-startup-foundation",
echo   "version": "1.0.0",
echo   "author": "Anonymous Startup Mentor",
echo   "license": "MIT",
echo   "description": "AI创业基础框架，整合创业动机、常见挑战与风险管理",
echo   "keywords": ["ai-startup", "startup-foundation", "entrepreneurship", "risk-management"],
echo   "category": "startup",
echo   "merged_from": [
echo     "ai-startup-motivation",
echo     "ai-startup-challenges", 
echo     "ai-startup-risk-management"
echo   ],
echo   "merge_date": "2026-05-29"
echo }
) > "%target%\metadata.json"

echo [4/5] Creating test and example directories...
mkdir "%target%\test" 2>nul
mkdir "%target%\example" 2>nul

echo [5/5] Marking old skills as merged...
(
echo # 已合并到 ai-startup-foundation
echo.
echo 本技能内容已整合到新的综合技能：**ai-startup-foundation**
echo.
echo 请访问新技能获取完整内容：
echo - [SKILL.md](../ai-startup-foundation/SKILL.md)
echo - [metadata.json](../ai-startup-foundation/metadata.json)
echo.
echo 合并日期：2026-05-29
echo.
echo 保留此文件用于向后兼容，6个月后将归档。
) > skills\ai-startup-motivation\MERGED.md

copy skills\ai-startup-motivation\MERGED.md skills\ai-startup-challenges\MERGED.md >nul
copy skills\ai-startup-motivation\MERGED.md skills\ai-startup-risk-management\MERGED.md >nul

echo.
echo === Merge Complete ===
echo Created: %target%
echo Merged: ai-startup-motivation, ai-startup-challenges, ai-startup-risk-management
echo.
pause
