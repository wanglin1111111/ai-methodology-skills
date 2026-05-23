---
summary: "灵光AI产品策略知识库"
autoclaw.schema: "skill/v1"
skill.name: "lingguang-strategy"
skill.version: "1.0.0"
skill.author: "wanglin1111111"
skill.tags: ["AI", "product-strategy", "knowledge-base", "lingguang"]
---

# 灵光AI产品策略

## 描述
灵光AI产品策略知识库，记录传播策略、产品定位、硬件规划、工作流引擎、Agent个性化等核心策略决策。

## 核心内容

### 1. 传播策略
- **自有阵地核心**：官网、公众号、视频号
- **多渠道引流**：抖音、快手、小红书、知乎
- **私域沉淀**：微信生态、社群运营

### 2. 产品定位
- **4.0交互时代**：AI驱动的自然交互
- **办公场景**：会议、文档、协作
- **支付宝接入**：支付+AI服务融合

### 3. 硬件产品
- **AI语音设备**：智能音箱、会议助手
- **功能规格**：语音识别、自然语言处理
- **改进方向**：音质、响应速度、多轮对话

### 4. 工作流引擎
- **交付为本**：结果导向，效率优先
- **开源策略**：核心开源，商业版增值
- **本地部署**：数据安全，隐私保护

### 5. Agent个性化
- **专属代理**：个人AI助手定制
- **社交替代**：部分社交场景AI化
- **数据驱动**：行为分析，智能推荐

### 6. 关键决策
- **支付渠道**：支付宝深度合作
- **开源方式**：Apache 2.0协议
- **本地部署**：支持私有化部署

### 7. 竞争优势
1. 技术领先：自研大模型
2. 场景深耕：办公场景专业化
3. 生态整合：支付宝生态接入
4. 开源开放：社区驱动创新
5. 本地部署：数据安全可控

### 8. 待验证假设
1. 用户愿意为AI办公付费
2. 企业接受本地部署模式
3. 开源能吸引开发者生态
4. 支付宝渠道转化率高
5. 硬件+软件组合有市场

## 工具

### query_strategy
查询灵光AI产品策略。

**参数：**
- topic (enum, required): 查询主题
  - `spread`: 传播策略
  - `positioning`: 产品定位
  - `hardware`: 硬件产品
  - `workflow`: 工作流引擎
  - `agent`: Agent个性化
  - `decision`: 关键决策
  - `advantage`: 竞争优势
  - `hypothesis`: 待验证假设
- detail (boolean, optional): 是否返回详细内容，默认true

**返回：**
- topic (string): 主题名称
- content (string): 策略内容
- key_points (array): 关键要点
- related_topics (array): 相关主题

**示例：**
```json
{
  "topic": "spread",
  "detail": true
}
```

### track_decision
追踪关键决策执行进度。

**参数：**
- decision_id (string, required): 决策ID
- status (enum, required): 当前状态
  - `proposed`: 已提出
  - `evaluating`: 评估中
  - `approved`: 已批准
  - `implementing`: 执行中
  - `completed`: 已完成
  - `cancelled`: 已取消
- notes (string, optional): 备注说明

**返回：**
- decision_id (string): 决策ID
- status (string): 更新后状态
- history (array): 状态变更历史

### validate_hypothesis
标记假设验证进度。

**参数：**
- hypothesis_id (string, required): 假设ID
- result (enum, required): 验证结果
  - `validated`: 已验证成立
  - `invalidated`: 已证伪
  - `pending`: 待验证
  - `in_progress`: 验证中
- evidence (string, optional): 验证证据

**返回：**
- hypothesis_id (string): 假设ID
- result (string): 验证结果
- confidence (number): 置信度

### analyze_competition
分析竞争优势和竞品对比。

**参数：**
- competitor (string, optional): 竞品名称
- dimension (enum, optional): 分析维度
  - `technology`: 技术能力
  - `product`: 产品功能
  - `market`: 市场覆盖
  - `ecosystem`: 生态系统
  - `overall`: 综合对比

**返回：**
- advantages (array): 优势列表
- disadvantages (array): 劣势列表
- opportunities (array): 机会点
- threats (array): 威胁点

## 示例

### 示例1: 查询传播策略
```
查询灵光AI的传播策略
```

### 示例2: 追踪决策
```
追踪支付渠道决策的执行进度
```

### 示例3: 验证假设
```
标记"用户愿意为AI办公付费"假设的验证结果
```

### 示例4: 竞争分析
```
分析与通义千问的竞争优劣势
```

## 注意事项

- 知识库为活文档，持续更新
- 关键决策需定期回顾
- 假设验证需数据支撑
- 竞争分析需客观公正

## 更新日志

### v1.0.0 (2026-05-23)
- 初始版本发布
- 包含8大核心策略模块
- 提供4个查询追踪工具

---

**版本**: 1.0.0  
**更新日期**: 2026-05-23  
**适用框架**: OpenClaw Agent System
