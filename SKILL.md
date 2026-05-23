# Object Capability (OCaps) Security Model Skill

## 技能概述

本技能专注于对象能力模型在AI Agent安全设计中的应用，解决传统权限管理的"混淆代理"问题，通过最小权限原则构建安全的AI系统。

**核心领域**：
- 混淆代理问题与安全风险
- 传统ACL权限模型的局限
- 最小权限原则（Principle of Least Privilege）
- 对象能力（Object Capability）模型
- AI Agent安全架构设计

---

## 1. AI Agent安全风险分析

### 1.1 混淆代理问题（Confused Deputy）

**问题定义**：
程序被授权执行某项任务，却拥有访问其他资源的权限，从而带来安全隐患。

**AI Agent场景**：
```yaml
典型场景:
  用户请求: "处理project-A目录下的文件"
  
  传统设计:
    Agent继承用户全部权限
    → 可访问整个主目录
    → 可访问所有凭证、密钥、配置文件
    → 可访问网络、摄像头、麦克风
    → 意外删除project-B的数据
  
  风险:
    - 权限过度授予（Over-privileged）
    - 意外访问敏感资源
    - 错误操作影响其他项目
    - 被攻击后影响整个系统
```

**实际案例**：
```yaml
案例1: 文件删除事故
  任务: 清理project-A的临时文件
  错误: Agent删除了project-B的重要文件
  原因: Agent继承了用户对所有文件的删除权限
  
案例2: 凭证泄露
  任务: 读取配置文件
  错误: Agent意外读取并发送了AWS密钥
  原因: Agent可访问整个~/.aws/目录
  
案例3: 横向移动攻击
  任务: 执行用户命令
  攻击: 恶意提示词诱导Agent访问网络
  原因: Agent继承了用户的网络访问权限
```

### 1.2 传统权限模型的局限

#### 1.2.1 ACL（访问控制列表）模型

**设计原理**：
```yaml
ACL模型:
  基于用户角色设定权限
  - 读权限（Read）
  - 写权限（Write）
  - 执行权限（Execute）
  
  权限检查流程:
    1. 用户发起请求
    2. 系统检查用户角色
    3. 根据角色判断是否有权限
    4. 允许或拒绝访问
```

**局限性**：
```yaml
问题1: 权限继承
  程序运行 → 继承用户全部权限
  无法区分"用户操作"和"程序操作"
  
问题2: 权限扩散
  用户可委托权限给程序
  程序可再委托给子程序
  权限链条无法控制
  
问题3: 粒度过粗
  权限基于"用户-资源"二元关系
  无法表达"仅对此特定文件"的权限
  
问题4: 时间无限制
  权限一旦授予，持续有效
  无法表达"仅在任务期间"的权限
```

**比喻说明**：
```
去医院看病:

ACL模型:
  你拿到房间钥匙 → 同时获得进入整个医院的权限
  可以进入任何房间、手术室、药房
  即使你只需要去诊室A

理想模型:
  你拿到诊室A的钥匙 → 只能进入诊室A
  无法进入其他房间
  离开医院后钥匙失效
```

---

## 2. 最小权限原则（Principle of Least Privilege）

### 2.1 原则定义

**提出时间**：1975年  
**核心思想**：每个程序应仅拥有完成其任务所需的最小权限集合

```yaml
最小权限原则:
  定义: 权限(程序) = 必需权限(任务)
  
  对比:
    传统设计: 权限(程序) = 权限(用户)
    最小权限: 权限(程序) ⊂ 权限(用户)
  
  效果:
    - 限制损害范围
    - 防止权限滥用
    - 减少攻击面
    - 提高系统韧性
```

### 2.2 安全效益

**损害限制**：
```yaml
场景: Agent被恶意提示词攻击

传统设计:
  攻击者获得用户全部权限
  → 可访问所有文件
  → 可访问网络
  → 可执行任意命令
  损害范围: 整个系统

最小权限:
  攻击者仅获得Agent的有限权限
  → 只能访问project-A目录
  → 无法访问网络
  → 无法访问其他项目
  损害范围: 仅project-A
```

**错误隔离**：
```yaml
场景: Agent代码存在Bug

传统设计:
  Bug可能导致:
  - 删除错误文件
  - 发送错误邮件
  - 访问错误API
  影响范围: 不可预测

最小权限:
  Bug仅能影响:
  - 授权范围内的文件
  - 授权范围内的API
  影响范围: 可预测、可控
```

---

## 3. 实现最小权限的三个维度

### 3.1 资源范围（Resource Scope）

**定义**：仅传递特定资源的引用，而非整个系统权限

```yaml
传统方式:
  授予: 整个主目录访问权
  风险: 可访问所有文件、子目录

最小权限:
  授予: 单个文件或目录的引用
  限制: 仅能访问该特定资源
  
示例:
  任务: 编辑 /project-A/config.yaml
  
  传统:
    权限: fs.access('/'), fs.read(), fs.write()
    可访问: 任何文件
  
  最小权限:
    权限: file.handle('/project-A/config.yaml')
    可访问: 仅config.yaml
```

**实现方式**：
```yaml
方式1: 文件句柄传递
  不传递路径字符串
  传递已打开的文件句柄
  Agent只能操作该句柄
  
方式2: 目录句柄传递
  传递目录的引用
  Agent只能访问该目录及其子目录
  
方式3: 对象引用传递
  传递对象的引用
  Agent只能调用该对象的方法
```

### 3.2 时间范围（Time Scope）

**定义**：仅在进程运行期间授予访问权限，任务结束后权限即刻失效

```yaml
传统方式:
  权限授予: 持续有效
  权限撤销: 需显式操作
  风险: 权限泄露、长期有效

最小权限:
  权限授予: 任务开始时
  权限撤销: 任务结束时自动失效
  优势: 无需手动撤销
  
实现:
  能力对象生命周期:
    创建: 任务启动
    有效: 任务执行期间
    销毁: 任务完成或失败
```

**实现示例**：
```python
# 传统方式（权限持续有效）
agent = Agent(user_permissions)
agent.execute(task)
# agent仍保留所有权限

# 最小权限方式（权限自动失效）
with capability_scope(resource='/project-A') as cap:
    agent = Agent(cap)
    agent.execute(task)
# 退出with块后，cap自动失效
```

### 3.3 传播范围（Propagation Scope）

**定义**：限制权限的扩散，防止权限蔓延至系统其他部分

```yaml
传统方式:
  组件A获得权限
  → 可委托给组件B
  → 组件B可委托给组件C
  → 权限链条无法控制
  风险: 权限扩散、横向移动

最小权限:
  组件A获得权限
  → 可委托权限的子集给组件B
  → 组件B无法获得超出A的权限
  → 权限单调递减
  优势: 权限链条可控
```

**权限衰减规则**：
```yaml
规则1: 权限子集传递
  组件A权限: {file1, file2, network}
  可传递给B: {file1} ⊂ {file1, file2, network}
  不可传递: {file3} ∉ {file1, file2, network}

规则2: 权限不可增强
  组件B的权限 ⊆ 组件A的权限
  组件B无法获得超出A的权限

规则3: 权限不可伪造
  无法凭空创建新权限
  权限必须从现有权限派生
```

---

## 4. 对象能力（Object Capability, OCaps）模型

### 4.1 模型定义

**核心概念**：
"持有对象的引用" = "拥有访问能力" = "拥有操作权限"

```yaml
OCaps模型:
  基本原理:
    - 对象 = 资源 + 操作
    - 引用 = 访问能力
    - 持有引用 = 拥有权限
  
  权限传递:
    通过引用传递进行权限委托
    无法通过其他方式获得权限
  
  权限限制:
    只能对持有引用的对象操作
    无法越权访问其他对象
```

**对比传统模型**：
```yaml
ACL模型:
  权限检查: 用户角色 + 资源ACL
  权限来源: 系统配置
  权限控制: 基于身份
  
OCaps模型:
  权限检查: 是否持有对象引用
  权限来源: 引用传递
  权限控制: 基于能力
```

### 4.2 OCaps三大原则

#### 原则1: 仅通过引用访问

```yaml
规则:
  访问对象的唯一方式 = 持有对象引用
  
  禁止:
    - 通过名字访问（如路径字符串）
    - 通过全局变量访问
    - 通过系统调用访问
  
  允许:
    - 通过引用调用对象方法
    - 通过引用读取对象属性
```

**示例**：
```python
# ❌ 错误：通过路径访问（ACL风格）
def process_file(path):
    with open(path) as f:  # 通过路径字符串访问
        return f.read()

# ✅ 正确：通过引用访问（OCaps风格）
def process_file(file_handle):
    return file_handle.read()  # 通过文件句柄访问
```

#### 原则2: 引用不可伪造

```yaml
规则:
  无法凭空创建对象引用
  引用必须通过合法途径获得
  
  合法途径:
    - 创建新对象（获得其引用）
    - 接收他人传递的引用
    - 从父对象派生子对象引用
  
  非法途径（禁止）:
    - 猜测或构造引用值
    - 从全局变量获取引用
    - 通过类型转换获得引用
```

**示例**：
```python
# ❌ 错误：伪造引用
fake_handle = FileHandle("/etc/passwd")  # 凭空创建引用

# ✅ 正确：合法获得引用
with open("/project-A/file.txt") as handle:  # 创建对象获得引用
    agent.process(handle)  # 传递引用
```

#### 原则3: 权限单调递减

```yaml
规则:
  权限传递过程中，权限只能减少或保持，不能增加
  
  数学表达:
    权限(B) ⊆ 权限(A)
    其中B从A获得权限
  
  效果:
    - 防止权限提升攻击
    - 限制权限扩散
    - 保证权限链条安全
```

**示例**：
```python
# 权限单调递减示例
root_cap = Capability(['/project-A', '/project-B'])  # 权限: A + B

# 传递子集权限
child_cap = root_cap.restrict(['/project-A'])  # 权限: A
# child_cap ⊂ root_cap ✓

# 无法增强权限
# child_cap无法获得'/project-C'的权限
# 因为root_cap本身没有该权限
```

### 4.3 OCaps实现机制

#### 4.3.1 能力对象设计

```yaml
能力对象结构:
  引用ID: 唯一标识符
  资源引用: 指向实际资源
  权限集合: 允许的操作
  生命周期: 创建时间、过期时间
  
示例:
  Capability:
    id: "cap-12345"
    resource: FileHandle("/project-A/config.yaml")
    permissions: [READ, WRITE]
    created_at: 2026-05-23T20:00:00
    expires_at: 2026-05-23T20:30:00
```

#### 4.3.2 能力传递机制

```yaml
传递流程:
  1. 创建者创建能力对象
  2. 创建者持有能力引用
  3. 创建者将引用传递给Agent
  4. Agent使用引用访问资源
  5. 任务完成后引用失效
  
传递方式:
  - 函数参数传递
  - 对象属性传递
  - 消息传递（分布式系统）
```

#### 4.3.3 能力撤销机制

```yaml
撤销方式:
  方式1: 时间过期
    能力对象设置过期时间
    到期自动失效
  
  方式2: 显式撤销
    创建者主动撤销能力
    所有派生能力同时失效
  
  方式3: 资源销毁
    资源被销毁时
    所有相关能力失效
```

---

## 5. AI Agent安全架构设计

### 5.1 基于OCaps的Agent设计

```yaml
Agent架构:
  能力管理器:
    - 创建能力对象
    - 管理能力生命周期
    - 撤销过期能力
  
  能力存储:
    - 存储Agent持有的能力
    - 防止能力伪造
    - 跟踪能力来源
  
  能力检查:
    - 检查Agent是否持有能力
    - 验证能力有效性
    - 记录能力使用
```

### 5.2 任务执行流程

```yaml
标准流程:
  1. 用户发起任务请求
     请求: "编辑/project-A/config.yaml"
  
  2. 系统创建最小权限能力
     cap = Capability(
       resource='/project-A/config.yaml',
       permissions=[READ, WRITE],
       expires=now + 30min
     )
  
  3. 将能力传递给Agent
     agent = Agent(capabilities=[cap])
  
  4. Agent执行任务
     agent.execute(task)
     # Agent只能访问config.yaml
     # 无法访问其他文件
  
  5. 任务完成，能力失效
     cap.revoke()
     # Agent失去所有权限
```

### 5.3 多Agent协作

```yaml
协作场景:
  主Agent需要委托子任务给子Agent
  
传统方式:
  主Agent传递用户权限给子Agent
  子Agent继承用户全部权限
  风险: 权限扩散

OCaps方式:
  主Agent创建子集能力
  sub_cap = main_cap.restrict(['/project-A/subdir'])
  子Agent获得受限能力
  优势: 权限单调递减
```

---

## 6. 实践应用指南

### 6.1 设计Checklist

```yaml
OCaps设计清单:
  资源访问:
    - [ ] 所有资源访问通过能力引用
    - [ ] 禁止通过路径字符串访问
    - [ ] 禁止通过全局变量访问
  
  能力传递:
    - [ ] 能力通过参数传递
    - [ ] 能力不可伪造
    - [ ] 能力单调递减
  
  生命周期:
    - [ ] 能力有明确过期时间
    - [ ] 任务完成自动撤销
    - [ ] 支持显式撤销
  
  审计日志:
    - [ ] 记录能力创建
    - [ ] 记录能力传递
    - [ ] 记录能力使用
    - [ ] 记录能力撤销
```

### 6.2 代码示例

#### Python实现示例

```python
from dataclasses import dataclass
from typing import Set, Optional
from datetime import datetime, timedelta
from enum import Enum

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"

@dataclass
class Capability:
    """对象能力"""
    id: str
    resource: str  # 资源路径或引用
    permissions: Set[Permission]
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    def is_valid(self) -> bool:
        """检查能力是否有效"""
        if self.expires_at and datetime.now() > self.expires_at:
            return False
        return True
    
    def has_permission(self, perm: Permission) -> bool:
        """检查是否有指定权限"""
        return self.is_valid() and perm in self.permissions
    
    def restrict(self, permissions: Set[Permission]) -> 'Capability':
        """创建权限子集（权限单调递减）"""
        new_perms = self.permissions & permissions
        if not new_perms:
            raise ValueError("Cannot restrict to empty permissions")
        return Capability(
            id=f"{self.id}-restricted",
            resource=self.resource,
            permissions=new_perms,
            created_at=datetime.now(),
            expires_at=self.expires_at
        )

class OCapsAgent:
    """基于OCaps的Agent"""
    
    def __init__(self):
        self.capabilities: Set[Capability] = set()
    
    def grant(self, cap: Capability):
        """授予能力"""
        if not cap.is_valid():
            raise ValueError("Cannot grant invalid capability")
        self.capabilities.add(cap)
    
    def revoke(self, cap_id: str):
        """撤销能力"""
        self.capabilities = {
            cap for cap in self.capabilities if cap.id != cap_id
        }
    
    def can_access(self, resource: str, perm: Permission) -> bool:
        """检查是否有访问权限"""
        for cap in self.capabilities:
            if cap.resource == resource and cap.has_permission(perm):
                return True
        return False
    
    def read_file(self, file_cap: Capability) -> str:
        """读取文件（通过能力引用）"""
        if not file_cap.has_permission(Permission.READ):
            raise PermissionError("No READ permission")
        # 实际读取文件
        return f"Content of {file_cap.resource}"

# 使用示例
def example_usage():
    # 创建能力（最小权限）
    cap = Capability(
        id="cap-001",
        resource="/project-A/config.yaml",
        permissions={Permission.READ, Permission.WRITE},
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(minutes=30)
    )
    
    # 创建Agent并授予能力
    agent = OCapsAgent()
    agent.grant(cap)
    
    # Agent执行任务
    content = agent.read_file(cap)
    
    # 任务完成，撤销能力
    agent.revoke("cap-001")
```

---

## 7. 与其他安全模型的对比

| 维度 | ACL模型 | RBAC模型 | OCaps模型 |
|------|---------|----------|-----------|
| **权限粒度** | 用户-资源 | 角色-资源 | 对象引用 |
| **权限传递** | 难以控制 | 基于角色 | 严格受控 |
| **最小权限** | 难以实现 | 部分支持 | 天然支持 |
| **混淆代理** | 易受攻击 | 部分缓解 | 完全解决 |
| **权限撤销** | 需显式操作 | 需显式操作 | 自动失效 |
| **审计追踪** | 基于用户 | 基于角色 | 基于能力 |

---

## 8. 使用本技能的场景

**触发条件**（当以下情况时使用此技能）：

1. 设计AI Agent权限系统
2. 解决混淆代理安全问题
3. 实现最小权限原则
4. 构建对象能力模型
5. 设计安全的Agent架构
6. 用户提到"对象能力"、"OCaps"、"最小权限"、"混淆代理"

**典型任务**：
- 分析Agent安全风险
- 设计OCaps权限系统
- 实现能力传递机制
- 评估权限模型优劣
- 编写安全代码示例

---

## 9. 技能输出格式

### 9.1 安全风险评估模板

```markdown
# AI Agent安全风险评估报告

## 1. 混淆代理风险分析
- 当前权限模型: [ACL/RBAC/OCaps]
- 权限继承方式: [用户权限/角色权限/能力引用]
- 风险等级: [高/中/低]

## 2. 最小权限实现评估
| 维度 | 当前状态 | 风险 | 建议 |
|------|---------|------|------|
| 资源范围 | [评估] | [风险] | [建议] |
| 时间范围 | [评估] | [风险] | [建议] |
| 传播范围 | [评估] | [风险] | [建议] |

## 3. OCaps迁移建议
- [ ] 实现能力对象
- [ ] 替换路径访问为引用访问
- [ ] 添加能力生命周期管理
- [ ] 实现权限单调递减检查
```

---

## 10. 技能维护与更新

**更新频率**：每月评审最新研究进展

**维护清单**：
- [ ] 同步OCaps最新论文
- [ ] 更新代码示例（多语言）
- [ ] 优化安全评估模板
- [ ] 追踪实际案例

**版本记录**：
- v1.0.0 (2026-05-23): 初始版本，基于对象能力模型研究创建