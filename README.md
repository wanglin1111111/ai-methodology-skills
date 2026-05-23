# 灵光AI产品策略 (Lingguang AI Product Strategy)

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange)]()

> 灵光AI产品策略知识库，记录AI产品从0到1的核心策略决策。

## 项目简介

本知识库记录灵光AI产品的核心策略，包括：
- 传播策略与获客路径
- 产品定位与场景选择
- 硬件产品规划
- 工作流引擎设计
- Agent个性化策略
- 关键决策追踪
- 竞争优势分析
- 待验证假设

## 核心内容

### 📢 传播策略
- **自有阵地核心**：官网、公众号、视频号
- **多渠道引流**：抖音、快手、小红书、知乎
- **私域沉淀**：微信生态、社群运营

### 🎯 产品定位
- **4.0交互时代**：AI驱动的自然交互
- **办公场景**：会议、文档、协作
- **支付宝接入**：支付+AI服务融合

### 🔧 硬件产品
- **AI语音设备**：智能音箱、会议助手
- **功能规格**：语音识别、自然语言处理
- **改进方向**：音质、响应速度、多轮对话

### ⚙️ 工作流引擎
- **交付为本**：结果导向，效率优先
- **开源策略**：核心开源，商业版增值
- **本地部署**：数据安全，隐私保护

### 🤖 Agent个性化
- **专属代理**：个人AI助手定制
- **社交替代**：部分社交场景AI化
- **数据驱动**：行为分析，智能推荐

### 🎯 关键决策
- **支付渠道**：支付宝深度合作
- **开源方式**：Apache 2.0协议
- **本地部署**：支持私有化部署

### 🏆 竞争优势
1. 技术领先：自研大模型
2. 场景深耕：办公场景专业化
3. 生态整合：支付宝生态接入
4. 开源开放：社区驱动创新
5. 本地部署：数据安全可控

### ❓ 待验证假设
1. 用户愿意为AI办公付费
2. 企业接受本地部署模式
3. 开源能吸引开发者生态
4. 支付宝渠道转化率高
5. 硬件+软件组合有市场

## 技能功能

### query_strategy
查询灵光AI产品策略

```json
{
  "topic": "spread",
  "detail": true
}
```

### track_decision
追踪关键决策执行进度

```json
{
  "decision_id": "payment-channel",
  "status": "implementing",
  "notes": "支付宝SDK集成中"
}
```

### validate_hypothesis
标记假设验证进度

```json
{
  "hypothesis_id": "h1",
  "result": "validated",
  "evidence": "付费转化率15%"
}
```

### analyze_competition
分析竞争优势和竞品对比

```json
{
  "competitor": "通义千问",
  "dimension": "overall"
}
```

## 使用示例

### 查询传播策略
```
查询灵光AI的传播策略是什么？
```

### 追踪决策
```
追踪支付渠道决策的执行进度
```

### 验证假设
```
标记"用户愿意为AI办公付费"假设的验证结果
```

### 竞争分析
```
分析与通义千问的竞争优劣势
```

## 文件结构

```
lingguang-strategy/
├── README.md          # 项目说明
├── SKILL.md           # 技能定义
├── IDENTITY.md        # 代理身份
├── AGENTS.md          # 工作区配置
└── knowledge-base/
    └── lingguang-ai-product-strategy.md
```

## 安装

### 方式1: 直接复制
```bash
# 复制到OpenClaw skills目录
cp -r lingguang-strategy ~/.stepclaw/skills/
```

### 方式2: Git克隆
```bash
git clone https://github.com/wanglin1111111/lingguang-strategy.git
cd lingguang-strategy
# 复制到skills目录
```

## 使用

在OpenClaw中激活技能：
```
查询灵光AI的产品定位策略
```

或追踪决策：
```
追踪开源策略决策的最新进展
```

## 更新日志

### v1.0.0 (2026-05-23)
- 初始版本发布
- 包含8大核心策略模块
- 提供4个查询追踪工具

## 贡献

欢迎提交Issue和PR！

## 许可证

MIT License

## 联系方式

- GitHub: https://github.com/wanglin1111111/lingguang-strategy

---

**注意**: 本知识库包含商业策略信息，仅供内部使用。
