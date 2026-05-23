# Object Capability (OCaps) Security Model Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/object-capability-security)

> 对象能力模型在AI Agent安全设计中的应用 - 解决"混淆代理"问题，实现最小权限原则

---

## 📖 概述

对象能力模型是一种强大的安全架构，通过"持有对象的引用即拥有访问权限"的设计，从根本上解决传统权限管理的"混淆代理"问题。

**核心问题**：
- ❌ AI Agent继承用户全部权限
- ❌ 权限远超任务所需
- ❌ 意外访问其他资源
- ❌ 被攻击后影响整个系统

**OCaps解决方案**：
- ✅ 最小权限原则（Principle of Least Privilege）
- ✅ 权限严格受控传递
- ✅ 自动过期和撤销
- ✅ 损害范围限制

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/object-capability-security.git

# 复制到OpenClaw技能目录
cp -r object-capability-security ~/.openclaw-autoclaw/skills/
```

### Python快速示例

```python
from capability import Capability, Permission
from agent import OCapsAgent
from datetime import timedelta

# 1. 创建能力（最小权限）
cap = Capability(
    resource="/project-A/config.yaml",
    permissions={Permission.READ, Permission.WRITE},
    duration=timedelta(minutes=30)
)

# 2. 创建Agent并授予能力
agent = OCapsAgent(name="ConfigAgent")
agent.grant(cap)

# 3. Agent执行任务（只能访问授权的文件）
content = agent.read_file(cap)  # ✅ 可以访问

# 4. Agent无法访问其他文件
# agent.read_file("/etc/passwd")  # ❌ 无能力引用

# 5. 任务完成，能力自动失效
```

---

## 📁 文件结构

```
object-capability-security/
├── SKILL.md                          # 主文档（理论框架）
├── README.md                         # 使用指南（本文件）
├── LICENSE                           # MIT开源协议
├── examples/
│   └── code-examples.md              # 多语言代码示例
└── templates/
    └── security-assessment.md        # 安全风险评估模板
```

---

## 🎯 核心概念

### 1. 混淆代理问题（Confused Deputy）

```yaml
问题场景:
  用户请求: "处理project-A目录"
  传统设计: Agent继承用户全部权限
  实际访问: 可访问整个主目录
  风险: 意外删除project-B的文件

OCaps解决:
  能力引用: 仅传递/project-A的引用
  权限限制: 只能访问project-A
  效果: 无法访问其他项目
```

### 2. 最小权限三维度

| 维度 | 传统方式 | OCaps方式 | 效果 |
|------|---------|-----------|------|
| **资源范围** | 整个主目录 | 特定文件/目录 | 限制访问范围 |
| **时间范围** | 持续有效 | 任务期间有效 | 自动过期 |
| **传播范围** | 可自由委托 | 权限单调递减 | 防止扩散 |

### 3. OCaps三大原则

```yaml
原则1: 仅通过引用访问
  禁止: 通过路径字符串访问
  允许: 通过能力引用访问
  
原则2: 引用不可伪造
  禁止: 凭空创建能力
  允许: 从现有能力派生
  
原则3: 权限单调递减
  规则: 权限(B) ⊆ 权限(A)
  效果: 防止权限提升攻击
```

---

## 🔬 使用场景

### 场景1：文件访问控制

```python
# ❌ 传统方式（危险）
def agent_read_file(path):
    with open(path) as f:  # 可访问任何文件
        return f.read()

# ✅ OCaps方式（安全）
def agent_read_file(file_cap):
    if not file_cap.has_permission(Permission.READ):
        raise PermissionError()
    with open(file_cap.resource) as f:  # 仅能访问授权文件
        return f.read()
```

### 场景2：多Agent协作

```python
# 主Agent委托子任务
main_agent = OCapsAgent("MainAgent")
sub_agent = OCapsAgent("SubAgent")

# 主Agent拥有读写权限
main_cap = Capability("/project-A", {READ, WRITE})
main_agent.grant(main_cap)

# 委托只读权限给子Agent（权限单调递减）
sub_cap_id = main_agent.delegate(main_cap.id, sub_agent, {READ})
# sub_agent只能读取，无法写入
```

### 场景3：时间限制

```python
# 能力30分钟后自动失效
cap = Capability(
    resource="/project-A/config.yaml",
    permissions={READ},
    duration=timedelta(minutes=30)
)

# 30分钟后
assert not cap.is_valid()  # 能力已过期
```

---

## 📊 对比传统模型

| 维度 | ACL模型 | OCaps模型 |
|------|---------|-----------|
| **权限粒度** | 用户-资源 | 对象引用 |
| **权限传递** | 难以控制 | 严格受控 |
| **最小权限** | 难以实现 | 天然支持 |
| **混淆代理** | 易受攻击 | 完全解决 |
| **权限撤销** | 需显式操作 | 自动失效 |

---

## 🛡️ 安全效益

### 损害限制

```yaml
传统设计（无OCaps）:
  攻击者控制Agent
  → 获得用户全部权限
  → 可访问所有文件
  → 可访问网络
  损害范围: 整个系统 🔴

OCaps设计:
  攻击者控制Agent
  → 仅获得受限能力
  → 只能访问project-A
  → 无网络权限
  损害范围: 仅project-A ✅
```

### 错误隔离

```yaml
传统设计:
  Agent代码Bug
  → 可能删除错误文件
  → 可能访问错误API
  影响范围: 不可预测 🔴

OCaps设计:
  Agent代码Bug
  → 只能操作授权资源
  → 无法越权访问
  影响范围: 可预测、可控 ✅
```

---

## 📚 文档导航

- **[SKILL.md](./SKILL.md)** - 完整理论框架
  - 混淆代理问题分析
  - 最小权限原则详解
  - OCaps模型原理
  - Agent安全架构设计

- **[examples/code-examples.md](./examples/code-examples.md)** - 代码实现
  - Python完整实现
  - TypeScript完整实现
  - Rust高性能实现
  - 多场景应用示例

- **[templates/security-assessment.md](./templates/security-assessment.md)** - 评估模板
  - 混淆代理风险识别
  - 最小权限实现评估
  - OCaps迁移路线图
  - 安全加固建议

---

## 🔧 实施指南

### 设计Checklist

```yaml
✅ 资源访问:
  - [ ] 所有资源访问通过能力引用
  - [ ] 禁止通过路径字符串访问
  - [ ] 禁止通过全局变量访问

✅ 能力传递:
  - [ ] 能力通过参数传递
  - [ ] 能力不可伪造
  - [ ] 能力单调递减

✅ 生命周期:
  - [ ] 能力有明确过期时间
  - [ ] 任务完成自动撤销
  - [ ] 支持显式撤销

✅ 审计日志:
  - [ ] 记录能力创建
  - [ ] 记录能力传递
  - [ ] 记录能力使用
  - [ ] 记录能力撤销
```

---

## 🤝 贡献指南

欢迎贡献代码、文档、测试用例！

```bash
# Fork仓库
git clone https://github.com/YOUR_USERNAME/object-capability-security.git

# 创建分支
git checkout -b feature/new-feature

# 提交Pull Request
git push origin feature/new-feature
```

---

## 📖 参考文献

### 学术论文
- "Capability-Based Security" (1975)
- "The Confused Deputy Problem" (1988)
- "Object Capability Model" (2006)

### 标准规范
- NIST SP 800-53: Access Control
- ISO/IEC 27001: Information Security

---

## 📜 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

**版本**: v1.0.0  
**发布日期**: 2026-05-23  
**维护者**: Object Capability Research Community