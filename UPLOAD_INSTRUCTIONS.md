# Git Upload Instructions for Ziba Skill

由于当前环境网络连接不稳定，请按以下步骤手动上传：

## 方式1：GitHub网页端上传（推荐）

### 步骤1：访问仓库
打开：https://github.com/wanglin1111111/-

### 步骤2：创建目录
在仓库中创建以下目录结构：
```
ziba-ai-game-strategy/
├── knowledge-base/
```

### 步骤3：上传文件

#### 文件1：技能配置
- 路径：`ziba-ai-game-strategy/SKILL.md`
- 本地文件：`C:\Users\22812\.openclaw-autoclaw\ziba-skill-upload\SKILL.md`
- 大小：6,292 bytes

#### 文件2：使用说明
- 路径：`ziba-ai-game-strategy/README.md`
- 本地文件：`C:\Users\22812\.openclaw-autoclaw\ziba-skill-upload\README.md`
- 大小：4,310 bytes

#### 文件3：知识库
- 路径：`ziba-ai-game-strategy/knowledge-base/ziba-brand-strategy-ai-game-workshop.md`
- 本地文件：`C:\Users\22812\.openclaw-autoclaw\ziba-skill-upload\knowledge-base\ziba-brand-strategy-ai-game-workshop.md`
- 大小：13,784 bytes

### 步骤4：提交更改
提交信息：
```
Add Ziba Brand Strategy & AI Game Workshop Skill v1.1.0

- Ziba品牌全球化战略与AI游戏工作坊知识管理技能
- 新增Coze平台API集成方案
- 新增Live a Life案例追踪系统
- 新增工作坊V3.0迭代方案
- 新增20%销售增长数据验证
- 包含隐私保护声明
- MIT许可证
```

---

## 方式2：Git命令上传（如有网络）

```bash
# 进入上传目录
cd C:\Users\22812\.openclaw-autoclaw\ziba-skill-upload

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Add Ziba Brand Strategy & AI Game Workshop Skill v1.1.0"

# 添加远程仓库
git remote add origin https://github.com/wanglin1111111/-.git

# 拉取最新代码（避免冲突）
git pull origin main --allow-unrelated-histories

# 解决冲突后推送
git push -u origin main
```

---

## 文件清单

| 文件名 | 路径 | 大小 | 状态 |
|--------|------|------|------|
| SKILL.md | ziba-ai-game-strategy/ | 6,292 bytes | ✅ 已准备 |
| README.md | ziba-ai-game-strategy/ | 4,310 bytes | ✅ 已准备 |
| ziba-brand-strategy-ai-game-workshop.md | ziba-ai-game-strategy/knowledge-base/ | 13,784 bytes | ✅ 已准备 |

**总大小**：24,386 bytes

---

## 验证清单

上传前请确认：
- [ ] SKILL.md 包含完整元数据（v1.1.0）
- [ ] README.md 包含优化亮点说明
- [ ] 知识库包含4个优化模块
- [ ] 所有文件都有隐私保护声明
- [ ] MIT许可证已添加

---

## 技能信息

- **名称**：ziba-ai-game-strategy
- **版本**：v1.1.0
- **作者**：AutoClaw User
- **许可证**：MIT
- **创建时间**：2026-05-23
- **更新时间**：2026-05-23 15:50

---

**文件位置**：
```
C:\Users\22812\.openclaw-autoclaw\ziba-skill-upload\
```

**创建时间**：2026-05-23 15:55  
**状态**：文件已准备，等待上传