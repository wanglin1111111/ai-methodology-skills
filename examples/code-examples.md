# Object Capability Code Examples - OCaps代码示例库

## 概述
本示例库提供对象能力模型的多语言实现示例，涵盖能力创建、传递、验证、撤销等核心操作。

---

## 示例1：Python实现 - 基础能力管理

### 1.1 能力对象实现

```python
from dataclasses import dataclass
from typing import Set, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid

class Permission(Enum):
    """权限类型"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"

@dataclass
class Capability:
    """对象能力"""
    id: str
    resource: str  # 资源标识符
    permissions: Set[Permission]
    created_at: datetime
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
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
            id=f"{self.id}-restricted-{uuid.uuid4().hex[:8]}",
            resource=self.resource,
            permissions=new_perms,
            created_at=datetime.now(),
            expires_at=self.expires_at,
            metadata=self.metadata
        )
    
    def extend_expiry(self, duration: timedelta) -> 'Capability':
        """延长过期时间"""
        if not self.expires_at:
            return self
        new_expiry = min(self.expires_at + duration, datetime.now() + timedelta(hours=24))
        return Capability(
            id=self.id,
            resource=self.resource,
            permissions=self.permissions,
            created_at=self.created_at,
            expires_at=new_expiry,
            metadata=self.metadata
        )
```

### 1.2 Agent实现

```python
class OCapsAgent:
    """基于OCaps的Agent"""
    
    def __init__(self, name: str):
        self.name = name
        self.capabilities: Dict[str, Capability] = {}
    
    def grant(self, cap: Capability):
        """授予能力"""
        if not cap.is_valid():
            raise ValueError("Cannot grant invalid capability")
        self.capabilities[cap.id] = cap
    
    def revoke(self, cap_id: str):
        """撤销能力"""
        if cap_id in self.capabilities:
            del self.capabilities[cap_id]
    
    def revoke_all(self):
        """撤销所有能力"""
        self.capabilities.clear()
    
    def can_access(self, resource: str, perm: Permission) -> bool:
        """检查是否有访问权限"""
        for cap in self.capabilities.values():
            if cap.resource == resource and cap.has_permission(perm):
                return True
        return False
    
    def delegate(self, cap_id: str, target_agent: 'OCapsAgent', 
                 permissions: Set[Permission]) -> str:
        """委托能力给其他Agent"""
        if cap_id not in self.capabilities:
            raise ValueError(f"Capability {cap_id} not found")
        
        original_cap = self.capabilities[cap_id]
        
        # 创建权限子集（权限单调递减）
        restricted_cap = original_cap.restrict(permissions)
        
        # 授予目标Agent
        target_agent.grant(restricted_cap)
        
        return restricted_cap.id
    
    def execute_task(self, task: callable, cap_id: str):
        """执行任务（使用能力）"""
        if cap_id not in self.capabilities:
            raise ValueError(f"Capability {cap_id} not found")
        
        cap = self.capabilities[cap_id]
        if not cap.is_valid():
            raise ValueError("Capability has expired")
        
        # 执行任务
        return task(cap)
```

### 1.3 使用示例

```python
# 创建能力管理器
class CapabilityManager:
    """能力管理器"""
    
    def __init__(self):
        self.capabilities: Dict[str, Capability] = {}
        self.audit_log: List[Dict] = []
    
    def create_capability(self, resource: str, permissions: Set[Permission],
                          duration: timedelta = timedelta(minutes=30)) -> Capability:
        """创建新能力"""
        cap = Capability(
            id=f"cap-{uuid.uuid4().hex[:12]}",
            resource=resource,
            permissions=permissions,
            created_at=datetime.now(),
            expires_at=datetime.now() + duration
        )
        self.capabilities[cap.id] = cap
        self._log("create", cap.id, resource, permissions)
        return cap
    
    def revoke_capability(self, cap_id: str):
        """撤销能力"""
        if cap_id in self.capabilities:
            cap = self.capabilities[cap_id]
            del self.capabilities[cap_id]
            self._log("revoke", cap_id, cap.resource, cap.permissions)
    
    def _log(self, action: str, cap_id: str, resource: str, 
             permissions: Set[Permission]):
        """记录审计日志"""
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "capability_id": cap_id,
            "resource": resource,
            "permissions": [p.value for p in permissions]
        })

# 实际使用示例
def example_usage():
    # 1. 创建能力管理器
    cap_manager = CapabilityManager()
    
    # 2. 创建能力（最小权限）
    cap = cap_manager.create_capability(
        resource="/project-A/config.yaml",
        permissions={Permission.READ, Permission.WRITE},
        duration=timedelta(minutes=30)
    )
    
    # 3. 创建Agent并授予能力
    agent = OCapsAgent(name="ConfigAgent")
    agent.grant(cap)
    
    # 4. Agent执行任务
    def read_config(cap: Capability) -> str:
        print(f"Reading {cap.resource} with permissions: {cap.permissions}")
        return f"Content of {cap.resource}"
    
    result = agent.execute_task(read_config, cap.id)
    
    # 5. 委托能力给子Agent
    sub_agent = OCapsAgent(name="SubAgent")
    sub_cap_id = agent.delegate(cap.id, sub_agent, {Permission.READ})
    
    # 6. 验证权限单调递减
    sub_cap = sub_agent.capabilities[sub_cap_id]
    print(f"Original permissions: {cap.permissions}")  # {READ, WRITE}
    print(f"Delegated permissions: {sub_cap.permissions}")  # {READ}
    
    # 7. 任务完成，撤销能力
    cap_manager.revoke_capability(cap.id)
    
    return result

# 运行示例
if __name__ == "__main__":
    example_usage()
```

---

## 示例2：JavaScript/TypeScript实现

### 2.1 能力对象实现

```typescript
// capability.ts
import { v4 as uuidv4 } from 'uuid';

export enum Permission {
  READ = 'read',
  WRITE = 'write',
  EXECUTE = 'execute',
  DELETE = 'delete'
}

export interface CapabilityConfig {
  resource: string;
  permissions: Set<Permission>;
  durationMs?: number;
  metadata?: Record<string, any>;
}

export class Capability {
  readonly id: string;
  readonly resource: string;
  readonly permissions: Set<Permission>;
  readonly createdAt: Date;
  readonly expiresAt: Date | null;
  readonly metadata: Record<string, any>;

  constructor(config: CapabilityConfig) {
    this.id = `cap-${uuidv4().split('-')[0]}`;
    this.resource = config.resource;
    this.permissions = config.permissions;
    this.createdAt = new Date();
    this.expiresAt = config.durationMs 
      ? new Date(Date.now() + config.durationMs)
      : null;
    this.metadata = config.metadata || {};
  }

  isValid(): boolean {
    if (this.expiresAt && new Date() > this.expiresAt) {
      return false;
    }
    return true;
  }

  hasPermission(perm: Permission): boolean {
    return this.isValid() && this.permissions.has(perm);
  }

  restrict(permissions: Set<Permission>): Capability {
    const newPerms = new Set(
      [...this.permissions].filter(p => permissions.has(p))
    );
    
    if (newPerms.size === 0) {
      throw new Error('Cannot restrict to empty permissions');
    }

    return new Capability({
      resource: this.resource,
      permissions: newPerms,
      durationMs: this.expiresAt 
        ? this.expiresAt.getTime() - Date.now()
        : undefined,
      metadata: this.metadata
    });
  }
}
```

### 2.2 Agent实现

```typescript
// agent.ts
import { Capability, Permission } from './capability';

export class OCapsAgent {
  readonly name: string;
  private capabilities: Map<string, Capability> = new Map();

  constructor(name: string) {
    this.name = name;
  }

  grant(cap: Capability): void {
    if (!cap.isValid()) {
      throw new Error('Cannot grant invalid capability');
    }
    this.capabilities.set(cap.id, cap);
  }

  revoke(capId: string): void {
    this.capabilities.delete(capId);
  }

  revokeAll(): void {
    this.capabilities.clear();
  }

  canAccess(resource: string, perm: Permission): boolean {
    for (const cap of this.capabilities.values()) {
      if (cap.resource === resource && cap.hasPermission(perm)) {
        return true;
      }
    }
    return false;
  }

  delegate(capId: string, targetAgent: OCapsAgent, 
           permissions: Set<Permission>): string {
    const originalCap = this.capabilities.get(capId);
    if (!originalCap) {
      throw new Error(`Capability ${capId} not found`);
    }

    // 创建权限子集（权限单调递减）
    const restrictedCap = originalCap.restrict(permissions);
    
    // 授予目标Agent
    targetAgent.grant(restrictedCap);
    
    return restrictedCap.id;
  }

  async executeTask<T>(
    task: (cap: Capability) => Promise<T>, 
    capId: string
  ): Promise<T> {
    const cap = this.capabilities.get(capId);
    if (!cap) {
      throw new Error(`Capability ${capId} not found`);
    }

    if (!cap.isValid()) {
      throw new Error('Capability has expired');
    }

    return await task(cap);
  }
}
```

### 2.3 使用示例

```typescript
// example.ts
import { Capability, Permission } from './capability';
import { OCapsAgent } from './agent';

async function exampleUsage() {
  // 1. 创建能力（最小权限）
  const cap = new Capability({
    resource: '/project-A/config.yaml',
    permissions: new Set([Permission.READ, Permission.WRITE]),
    durationMs: 30 * 60 * 1000 // 30分钟
  });

  // 2. 创建Agent并授予能力
  const agent = new OCapsAgent('ConfigAgent');
  agent.grant(cap);

  // 3. Agent执行任务
  const result = await agent.executeTask(async (cap) => {
    console.log(`Reading ${cap.resource}`);
    console.log(`Permissions: ${[...cap.permissions].join(', ')}`);
    return `Content of ${cap.resource}`;
  }, cap.id);

  console.log(result);

  // 4. 委托能力给子Agent
  const subAgent = new OCapsAgent('SubAgent');
  const subCapId = agent.delegate(
    cap.id, 
    subAgent, 
    new Set([Permission.READ])
  );

  // 5. 验证权限单调递减
  const subCap = subAgent['capabilities'].get(subCapId);
  console.log('Original permissions:', [...cap.permissions]); // [READ, WRITE]
  console.log('Delegated permissions:', [...subCap.permissions]); // [READ]
}

exampleUsage();
```

---

## 示例3：Rust实现（高性能场景）

### 3.1 能力对象实现

```rust
// capability.rs
use std::collections::HashSet;
use std::time::{Duration, Instant};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Permission {
    Read,
    Write,
    Execute,
    Delete,
}

#[derive(Debug)]
pub struct Capability {
    pub id: String,
    pub resource: String,
    pub permissions: HashSet<Permission>,
    pub created_at: Instant,
    pub expires_at: Option<Instant>,
}

impl Capability {
    pub fn new(
        resource: String,
        permissions: HashSet<Permission>,
        duration: Option<Duration>,
    ) -> Self {
        let id = format!("cap-{}", uuid::Uuid::new_v4());
        let created_at = Instant::now();
        let expires_at = duration.map(|d| created_at + d);

        Capability {
            id,
            resource,
            permissions,
            created_at,
            expires_at,
        }
    }

    pub fn is_valid(&self) -> bool {
        if let Some(expires_at) = self.expires_at {
            Instant::now() < expires_at
        } else {
            true
        }
    }

    pub fn has_permission(&self, perm: Permission) -> bool {
        self.is_valid() && self.permissions.contains(&perm)
    }

    pub fn restrict(&self, permissions: HashSet<Permission>) -> Result<Self, String> {
        let new_perms: HashSet<Permission> = self.permissions
            .intersection(&permissions)
            .cloned()
            .collect();

        if new_perms.is_empty() {
            return Err("Cannot restrict to empty permissions".to_string());
        }

        let duration = self.expires_at.map(|exp| {
            exp.duration_since(Instant::now())
                .unwrap_or(Duration::from_secs(0))
        });

        Ok(Capability::new(self.resource.clone(), new_perms, duration))
    }
}
```

### 3.2 Agent实现

```rust
// agent.rs
use std::collections::HashMap;
use crate::capability::{Capability, Permission};

pub struct OCapsAgent {
    name: String,
    capabilities: HashMap<String, Capability>,
}

impl OCapsAgent {
    pub fn new(name: String) -> Self {
        OCapsAgent {
            name,
            capabilities: HashMap::new(),
        }
    }

    pub fn grant(&mut self, cap: Capability) -> Result<(), String> {
        if !cap.is_valid() {
            return Err("Cannot grant invalid capability".to_string());
        }
        self.capabilities.insert(cap.id.clone(), cap);
        Ok(())
    }

    pub fn revoke(&mut self, cap_id: &str) {
        self.capabilities.remove(cap_id);
    }

    pub fn can_access(&self, resource: &str, perm: Permission) -> bool {
        self.capabilities.values().any(|cap| {
            cap.resource == resource && cap.has_permission(perm)
        })
    }

    pub fn delegate(
        &self,
        cap_id: &str,
        target: &mut OCapsAgent,
        permissions: HashSet<Permission>,
    ) -> Result<String, String> {
        let original_cap = self.capabilities.get(cap_id)
            .ok_or_else(|| format!("Capability {} not found", cap_id))?;

        let restricted_cap = original_cap.restrict(permissions)?;
        let new_id = restricted_cap.id.clone();

        target.grant(restricted_cap)?;

        Ok(new_id)
    }
}
```

---

## 示例4：文件系统访问控制

### 4.1 传统方式 vs OCaps方式

```python
# ❌ 传统方式：通过路径访问（ACL风格）
def traditional_file_access():
    # Agent继承用户全部权限
    def agent_read_file(path: str) -> str:
        with open(path, 'r') as f:
            return f.read()
    
    # Agent可以读取任何文件
    content = agent_read_file('/etc/passwd')  # 危险！
    content = agent_read_file('/project-B/secret.yaml')  # 越权！

# ✅ OCaps方式：通过能力引用访问
def ocaps_file_access():
    # 创建能力（最小权限）
    cap = Capability(
        id="cap-001",
        resource="/project-A/config.yaml",
        permissions={Permission.READ},
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(minutes=30)
    )
    
    # Agent只能访问授权的文件
    def agent_read_file(file_cap: Capability) -> str:
        if not file_cap.has_permission(Permission.READ):
            raise PermissionError("No READ permission")
        with open(file_cap.resource, 'r') as f:
            return f.read()
    
    # 安全访问
    content = agent_read_file(cap)  # 仅能访问config.yaml
    
    # 无法访问其他文件
    # agent_read_file('/etc/passwd')  # 编译错误：需要Capability类型
```

---

## 示例5：多Agent协作场景

### 5.1 主Agent委托子任务

```python
def multi_agent_collaboration():
    # 1. 创建主Agent和子Agent
    main_agent = OCapsAgent(name="MainAgent")
    sub_agent1 = OCapsAgent(name="SubAgent1")
    sub_agent2 = OCapsAgent(name="SubAgent2")
    
    # 2. 创建主能力（权限：读/写）
    main_cap = Capability(
        id="cap-main",
        resource="/project-A",
        permissions={Permission.READ, Permission.WRITE},
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(hours=2)
    )
    
    main_agent.grant(main_cap)
    
    # 3. 委托权限给子Agent（权限单调递减）
    # SubAgent1获得读权限
    sub_cap1_id = main_agent.delegate(
        main_cap.id, 
        sub_agent1, 
        {Permission.READ}
    )
    
    # SubAgent2获得读权限
    sub_cap2_id = main_agent.delegate(
        main_cap.id,
        sub_agent2,
        {Permission.READ}
    )
    
    # 4. 子Agent无法委托写权限（因为它们没有写权限）
    try:
        sub_agent1.delegate(sub_cap1_id, sub_agent2, {Permission.WRITE})
    except ValueError as e:
        print(f"权限委托失败: {e}")  # 正确！无法增强权限
    
    # 5. 主Agent撤销能力
    main_agent.revoke(main_cap.id)
    # 所有子Agent的能力也失效（传播范围控制）
```

---

## 使用指南

### 如何选择实现语言

| 语言 | 适用场景 | 性能 | 生态 |
|------|---------|------|------|
| **Python** | 快速原型、研究验证 | 中等 | 丰富 |
| **TypeScript** | Web应用、Node.js后端 | 良好 | 完善 |
| **Rust** | 高性能系统、安全关键场景 | 极高 | 成长中 |

### 最佳实践

```yaml
设计原则:
  1. 最小权限: 仅授予任务所需的权限
  2. 能力短生命周期: 设置合理的过期时间
  3. 权限单调递减: 委托时只能减少权限
  4. 审计日志: 记录所有能力操作
  5. 自动撤销: 任务完成后自动撤销能力

实施步骤:
  1. 识别Agent需要访问的资源
  2. 定义所需的最小权限集合
  3. 创建能力并授予Agent
  4. Agent通过能力引用访问资源
  5. 任务完成后撤销能力
```

---

**版本**: v1.0.0  
**最后更新**: 2026-05-23