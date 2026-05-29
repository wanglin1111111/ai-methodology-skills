# Scripts 使用指南

本目录包含用于维护和优化技能库的脚本工具。

## 脚本列表

| 脚本 | 用途 | 执行顺序 |
|------|------|---------|
| `normalize_naming.py` | 规范化技能目录命名 | 1 |
| `quality_gate.py` | 质量门禁检查 | 2 |
| `validate_skills.py` | 验证技能结构 | 3 |
| `optimize_skills.py` | 批量优化技能 | 4 |
| `add_cross_links.py` | 添加交叉链接 | 5 |
| `create-meta.bat` | 批量创建 metadata.json | 辅助 |

## 执行顺序

```bash
# 第1步: 命名规范化
python scripts/normalize_naming.py

# 第2步: 质量检查
python scripts/quality_gate.py

# 第3步: 验证结构
python scripts/validate_skills.py

# 第4步: 批量优化
python scripts/optimize_skills.py

# 第5步: 添加交叉链接
python scripts/add_cross_links.py
```

## 快速修复

```bash
# 一键执行所有修复
python scripts/optimize_skills.py --fix-all
```

## 注意事项

- 所有脚本应在仓库根目录执行
- 执行前建议先备份
- 部分脚本会修改文件，请 review 后再提交
