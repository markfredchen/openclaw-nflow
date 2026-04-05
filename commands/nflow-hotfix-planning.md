# /nflow-hotfix-planning

## Hotfix Sprint 规划

**Phase:** HOTFIX

**执行时机:** 发现紧急 bug 或需要立即修复的问题

**执行 Agent:** Lead Agent + PM Agent + Scrum Master Agent

---

## 触发条件

| 情况 | 说明 |
|------|------|
| 生产环境严重 bug | 影响核心功能 |
| 安全漏洞 | 需要立即修复 |
| 数据问题 | 数据损坏或丢失 |
| 客户投诉 | 紧急客户需求 |

---

## 与普通 Sprint 的区别

| 维度 | 普通 Sprint | Hotfix Sprint |
|------|------------|---------------|
| 目标 | 完成新功能 | 修复紧急问题 |
| Sprint 长度 | 1-4 周 | 通常 1-7 天 |
| 团队 | 全员 | 必要时最小团队 |
| 审查 | 标准 Code Review | 快速 Code Review |
| 测试 | 完整测试 | 聚焦回归测试 |
| 部署 | 按计划 | 修复即部署 |

---

## 执行步骤

### 1. 收集 Hotfix Stories

**收集所有紧急修复需求：**

```bash
# 扫描所有标记为紧急的 Stories
python3 scripts/nflow_tools.py scan-sprints
```

**来源：**
- `/nflow-review` 发现的紧急问题
- `/nflow-new-spec` 录入的紧急 bug
- 用户报告的生产问题

**紧急程度判断：**

| 级别 | 影响 | 响应时间 |
|------|------|----------|
| 🔴 P0 - 紧急 | 核心功能不可用 | 立即处理 |
| 🟠 P1 - 高 | 主要功能受损 | 24h 内 |
| 🟡 P2 - 中 | 功能部分受影响 | 72h 内 |

### 2. 创建 Hotfix Sprint

**Sprint 命名规则：**
```
hotfix-{date}
示例: hotfix-20260405
```

**创建目录结构：**

```
sprints/
├── hotfix-20260405/
│   ├── sprint-plan.md
│   ├── user-stories-tracker.md
│   └── implementations/
├── backlog.md（已更新）
└── change-log.md（已更新）
```

### 3. 规划 Hotfix Sprint

**使用最小团队：**

| 角色 | 参与 |
|------|------|
| Lead Agent | 统筹协调 |
| PM Agent | 需求确认 |
| Developer | 1-2 人（按需）|
| QA Agent | 测试验证 |
| Git Workflow Master | 快速部署 |

**Sprint 容量：**

- 团队规模 1-3 人
- Sprint 长度 1-7 天
- 故事点上限 8-13 点（按紧急程度）

### 4. 创建 Hotfix Sprint 文件

**sprints/hotfix-YYYYMMDD/sprint-plan.md：**

```markdown
# Hotfix Sprint Plan - {date}

**Sprint:** hotfix-{date}
**日期:** {date}
**类型:** HOTFIX
**持续时间:** {n} 天
**团队:** {最小团队}

## 紧急程度

| Story ID | 问题 | 紧急程度 | 负责人 |
|----------|------|----------|--------|
| HOTFIX-001 | 登录功能崩溃 | P0 | @dev1 |
| HOTFIX-002 | 支付接口异常 | P0 | @dev2 |

## Sprint 目标

尽快修复生产环境紧急问题，恢复核心功能。

## 部署计划

| 时间 | 行动 |
|------|------|
| Day 1 | HOTFIX-001 修复 + 测试 |
| Day 1 | HOTFIX-001 部署 |
| Day 2 | HOTFIX-002 修复 + 测试 |
| Day 2 | HOTFIX-002 部署 |

## 风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 修复引入新问题 | 高 | 完整回归测试 |
| 测试时间不足 | 中 | 聚焦核心功能测试 |
```

**sprints/hotfix-YYYYMMDD/user-stories-tracker.md：**

```markdown
# User Stories Tracker - Hotfix Sprint {date}

| Story ID | 名称 | 紧急程度 | 故事点 | 状态 | 负责人 | 备注 |
|----------|------|----------|--------|------|--------|------|
| HOTFIX-001 | 登录崩溃修复 | P0 | 3 | 🔄 IN_PROGRESS | @dev1 | |
| HOTFIX-002 | 支付接口修复 | P0 | 5 | ⏳ TODO | @dev2 | |
```

### 5. 更新相关文件

**更新 backlog.md：**

```markdown
## Hotfix Stories

### HOTFIX-001: 登录功能崩溃修复

**来源:** 生产环境发现
**紧急程度:** P0
**故事点:** 3

**问题描述:**
用户无法登录，错误率 100%

**Acceptance Criteria:**
- [ ] 修复登录接口
- [ ] 验证修复有效
- [ ] 部署到生产
```

**更新 change-log.md：**

```markdown
| CR-HOTFIX-001 | {date} | BUG_FIX | 登录崩溃 | HOTFIX-001 | APPROVED | HOTFIX |
| CR-HOTFIX-002 | {date} | BUG_FIX | 支付异常 | HOTFIX-002 | APPROVED | HOTFIX |
```

### 6. 执行 Hotfix 开发

```bash
# 开始 Hotfix 开发
/nflow-dev --sprint hotfix-20260405
```

**流程简化：**

```
Hotfix 开发流程：
1. 快速 TDD 开发
2. 快速 Code Review（30min 内）
3. 回归测试
4. 立即部署
```

---

## 输出文件

| 文件 | 路径 | Agent |
|------|------|-------|
| Hotfix Sprint Plan | `sprints/hotfix-YYYYMMDD/sprint-plan.md` | Scrum Master |
| Hotfix Tracker | `sprints/hotfix-YYYYMMDD/user-stories-tracker.md` | Scrum Master |
| Backlog 更新 | `sprints/backlog.md` | PM Agent |
| Change Log 更新 | `change-log.md` | PM Agent |

---

## Hotfix 完成后的动作

1. **立即部署**到生产环境
2. **通知**相关人员
3. **记录**修复内容
4. **合并**到主分支
5. **更新**项目记忆

---

## 与 /nflow-new-spec 的区别

| 命令 | 场景 | Sprint 类型 |
|------|------|-------------|
| `/nflow-new-spec` | 新需求/Bug（普通） | 普通 Sprint |
| `/nflow-hotfix-planning` | 紧急修复 | Hotfix Sprint |
