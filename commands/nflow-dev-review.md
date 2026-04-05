# /nflow-dev-review

## 代码审查流程

**Phase:** Phase 8.6

**执行 Agent:** Code Reviewer Agent

---

## 通知机制

代码审查完成后发送通知：
- 审查通过
- 审查有问题（Blocker/Suggestion）
- 审查失败达到 3 次（人工干预）

---

## 代码审查标准

### 🔴 Blocker（必须修复）

- 安全漏洞
- 逻辑错误
- 严重性能问题
- 破坏性变更

### 🟡 Suggestion（建议修复）

- 代码可读性问题
- 潜在性能优化
- 缺少注释

### 💭 Nit（可选小问题）

- 命名规范
- 格式问题
- 微不足道的改进

---

## 代码审查流程

```
1. 读取代码变更
       ↓
2. 检查基本正确性
       ↓
3. 发现 Blocker?
    ├── 是 → 记录并要求修复
    │    ↓
    │   审查失败次数 +1
    │    ↓
    │   发送审查失败通知
    └── 否 → 继续审查
       ↓
4. 发现 Suggestion?
    ├── 是 → 记录建议
    │    ↓
    │   发送审查建议通知
    └── 否 → 继续
       ↓
5. 完成审查报告
       ↓
6. 发送审查完成通知
```

### 审查完成通知

```bash
# 审查通过
python3 scripts/nflow_notify.py \
    --node "代码审查" \
    --status success \
    --message "审查通过：0 个 Blocker，0 个 Suggestion" \
    --story-id STORY-001 \
    --sprint sprint-01

# 有 Blocker 需要修复
python3 scripts/nflow_notify.py \
    --node "代码审查" \
    --status warning \
    --message "发现 1 个 🔴 Blocker（SQL注入风险）和 2 个 🟡 Suggestion，请修复" \
    --screenshot "sprints/sprint-01/reviews/review-001.png" \
    --story-id STORY-001 \
    --sprint sprint-01

# 有 Blocker 但未达到3次阈值
python3 scripts/nflow_notify.py \
    --node "代码审查" \
    --status warning \
    --message "审查失败 2 次，请修复 Blockers 后重新提交审查" \
    --story-id STORY-001
```

### 人工干预通知（3次失败）

```bash
python3 scripts/nflow_notify.py \
    --node "代码审查-人工干预" \
    --status failure \
    --message "⚠️ 审查失败 3 次！需要 Tech Lead 人工介入审查 STORY-001" \
    --story-id STORY-001 \
    --sprint sprint-01
```

---

## 审查反馈格式

```markdown
## Code Review Feedback

**Story:** {story_id}
**Reviewer:** {name}
**Date:** {date}

### 🔴 Blockers

| # | 文件 | 问题 | 建议 |
|---|------|------|------|
| 1 | src/user.py | SQL 注入风险 | 使用参数化查询 |

### 🟡 Suggestions

| # | 文件 | 问题 | 建议 |
|---|------|------|------|
| 1 | src/utils.js | 缺少注释 | 添加函数说明 |

### 💭 Nits

- 变量命名不一致
```

---

## 审查失败规则

**审查失败次数跟踪：**
- 每次审查被要求修复 Blockers，审查失败次数 +1
- 记录在 `user-stories-tracker.md`

**tracker 记录格式：**
```markdown
| STORY-001 | 用户注册 | P0 | 3 | Sprint 01 | 🔍 CODE_REVIEW | @dev1 | 审查第 2 次 |
```

**3 次规则：**
- 第 1 次失败 → 修复 → 重新审查
- 第 2 次失败 → 修复 → 重新审查
- **第 3 次失败 → 🤖 人工干预！**

---

## 人工干预处理

当审查失败 3 次时：

1. **Tech Lead Agent 介入**
2. **分析问题根源**
   - 需求不清？
   - 技术方案问题？
   - 沟通问题？
3. **根据原因处理**
   - 需求问题 → 触发 Change Control Gate
   - 技术问题 → Architect Agent 重新评估方案
4. **直接修复问题**
5. **继续流程**

**人工干预完成通知：**
```bash
python3 scripts/nflow_notify.py \
    --node "人工干预完成" \
    --status success \
    --message "Tech Lead 已完成 STORY-001 的问题修复，审查通过" \
    --story-id STORY-001 \
    --sprint sprint-01
```

---

## 代码审查检查清单

| 检查项 | 说明 |
|--------|------|
| 功能正确性 | 代码是否实现了需求 |
| 安全性 | 是否有安全漏洞 |
| 性能 | 是否有性能问题 |
| 可读性 | 代码是否易读 |
| 测试覆盖 | 是否有足够的测试 |
| 文档 | 是否更新了必要文档 |

---

## 输出文件

| 文件 | 说明 |
|------|------|
| Code Review 反馈 | 记录在 Story 备注中 |
| 审查报告 | `sprints/sprint-XX/code-review-{id}.md` |

---

## 相关脚本

- `scripts/nflow_notify.py` - Telegram 通知脚本
- `scripts/nflow_tools.py` - 审查失败次数跟踪
