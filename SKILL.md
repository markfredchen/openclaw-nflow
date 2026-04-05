---
name: nflow
description: NFlow - Custom Development Workflow combining BMad Method + Superpowers. Use when initializing projects, defining requirements, designing systems, planning sprints, or developing software with TDD and multi-agent collaboration.
---

# NFlow - Custom Development Workflow

**Version:** 1.0.0
**融合：** BMad Method + Superpowers
**适用平台：** OpenClaw / Claude Code / Gemini / Codex

---

## Overview

NFlow is a structured development workflow that combines the best practices from BMad Method and Superpowers:
- **BMad Method:** Multi-Agent collaboration, Scale-Adaptive Intelligence
- **Superpowers:** Mandatory brainstorming, TDD, Change Control Gate

---

## Commands

| Command | Phase | Description |
|---------|-------|-------------|
| `/nflow-init` | Phase 0 | 项目初始化，复杂度判定 |
| `/nflow-requirements` | Phase 1 | 市场调研 → PRD → 架构设计 |
| `/nflow-design` | Phase 2-3 | 设计系统 + 线框图 |
| `/nflow-prototype` | Phase 4-5 | 人工审核 + HTML 原型 |
| `/nflow-plan` | Phase 6-7 | Backlog 生成 + Sprint 规划 |
| `/nflow-dev` | Phase 8 | 开发循环（精简入口）|
| `/nflow-resume` | Phase 8 | 恢复中断的开发循环 |
| `/nflow-story` | Phase 8 | 实现单个 User Story |
| `/nflow-review` | Phase 9 | 最终 Code Review |
| `/nflow-new-spec` | CHANGE | 新需求/Bug 录入和处理 |
| `/nflow-hotfix-planning` | HOTFIX | 紧急修复 Sprint 规划 |

---

## Quick Start

```
1. /nflow-init                    # 初始化项目
2. /nflow-requirements           # 需求定义
3. /nflow-design                 # 设计系统 + 线框图
4. /nflow-prototype              # 原型 + 审核
5. /nflow-plan                   # Backlog + Sprint
6. /nflow-dev                    # 开始开发循环
7. /nflow-review                 # 最终评审
```

---

## Workflow Overview

```
Phase 0: INIT
         ↓
Phase 1: REQUIREMENTS
    RESEARCH → PRD → ARCHITECTURE
         ↓
Phase 2-3: DESIGN
    DESIGN SYSTEM → WIREFRAMES
         ↓
Phase 4-5: PROTOTYPE
    APPROVAL GATE → UI PROTOTYPE
         ↓
Phase 6-7: PLAN
    BACKLOG → SPRINT PLANNING
         ↓
Phase 8: IMPLEMENT (循环)
    Story → E2E → TDD → Review → Merge → Repeat
         ↓
Phase 9: REVIEW
```

---

## Key Features

- **Dual-track Complexity:** L1 Quick → L4 Enterprise
- **Human Approval Gates:** Phase 4 & Phase 5 require human sign-off
- **TDD Required:** RED → GREEN → REFACTOR
- **Git Worktree Isolation:** Each Story in isolated worktree
- **Change Control:** Any change must go through Change Control Gate
- **Single Sprint Planning:** Only plan one Sprint at a time

---

## Platform Compatibility

This skill works with:
- ✅ **OpenClaw:** Native skill support
- ✅ **Claude Code:** Via `/nflow-*` commands
- ✅ **Gemini:** Via instructions
- ✅ **Codex:** Via `@nflow` reference

---

## Agent Activation

See `AGENTS.md` for agent activation mechanisms.

### Quick Reference

```
@nflow-init      → 激活 Lead Agent
@nflow-req       → 激活 PM + Architect Agent
@nflow-design    → 激活 UI/UX Designer Agent
@nflow-dev       → 激活 Developer + QA + Code Reviewer Agent
```

### Agent Activation Methods

**方式 1：** 直接引用
```
@Lead Agent
@PM Agent
```

**方式 2：** 读取文件
```
读取 agents/01-lead-agent.md → 激活 Lead Agent
```

## Installation

See `scripts/install-*.sh` for platform-specific installation.

### OpenClaw Mode Selection

安装时可选择 Agent 运行模式：

| 模式 | 命令 | 说明 |
|------|------|------|
| Agent 模式 | `--mode agent` | 每个 Agent 是独立进程，拥有独立 workspace，适用于复杂项目 |
| Subagent 模式 | `--mode subagent` | 使用 spawn 方式启动 Agent，轻量级协作，共享上下文 |

```bash
# Agent 模式（默认）
./scripts/install-openclaw.sh --mode agent

# Subagent 模式
./scripts/install-openclaw.sh --mode subagent
```

### Utility Scripts (Python)

**推荐使用 Python 脚本进行状态扫描和记忆管理，避免 LLM token 消耗**

#### 状态扫描命令
```bash
# Sprint 状态扫描
python3 scripts/nflow_tools.py scan-sprints

# 获取下一个待处理的 Story
python3 scripts/nflow_tools.py get-next-story

# 获取指定 Story 详情
python3 scripts/nflow_tools.py get-story STORY-001

# 检查被阻塞的 Stories
python3 scripts/nflow_tools.py check-blocked

# 检查 3 次失败规则
python3 scripts/nflow_tools.py check-3-strikes STORY-001

# 列出 Git worktree 状态
python3 scripts/nflow_tools.py list-worktrees

# 🚨 NFlow 合规检查（每次开发前必须运行）
python3 scripts/check_compliance.py [项目目录]
```

#### Story 操作命令
```bash
# 更新 Story 状态
python3 scripts/nflow_tools.py update-state STORY-001 TESTING

# 测试失败次数 +1
python3 scripts/nflow_tools.py increment-test-fail STORY-001

# 审查失败次数 +1
python3 scripts/nflow_tools.py increment-review-fail STORY-001
```

#### 记忆管理命令
```bash
# 初始化项目记忆文件
python3 scripts/nflow_tools.py init-memory "项目名称" L2 "OpenClaw"

# 更新项目记忆
python3 scripts/nflow_tools.py update-memory sprint_progress=sprint-01

# 记录决策
python3 scripts/nflow_tools.py log-decision ARCH "选择微服务" "团队规模大" "单体的替代方案"

# 生成外部 Agent 上下文（JSON）
python3 scripts/nflow_tools.py generate-context STORY-001

# 生成外部 Agent 上下文（文本）
python3 scripts/nflow_tools.py get-context STORY-001
```

#### Sprint Review 命令
```bash
# 生成 Sprint 回顾文档
python3 scripts/nflow_tools.py generate-review sprint-01

# 更新项目记忆（包含回顾数据）
python3 scripts/nflow_tools.py update-retrospective sprint-01 '{"went_well": ["TDD流程"], "improve": ["预估误差"], "lessons": ["教训"]}'
```

#### HTML 报告生成
```bash
# 生成 E2E 验收报告
python3 scripts/generate_html_report.py \\
    --template templates/acceptance-report-template.html \\
    --data /tmp/report-data.json \\
    --output sprints/sprint-01/acceptance-report-001.html

# 生成 Sprint Review 报告
python3 scripts/generate_html_report.py \\
    --template templates/sprint-review-report-template.html \\
    --data /tmp/sprint-review-data.json \\
    --output sprints/sprint-01/review-report.html
```

#### 外部 Agent 启动
```bash
# 启动外部开发 Agent（ACP 协议，自动加载项目上下文）
python3 scripts/spawn-dev-agent.py --agent claude-code --task dev --story-id STORY-001 --project /path/to/project

# 仅打印 JSON，不执行
python3 scripts/spawn-dev-agent.py --agent claude-code --task dev --story-id STORY-001 --print-only

# 不加载项目上下文
python3 scripts/spawn-dev-agent.py --agent claude-code --task dev --story-id STORY-001 --no-context
```

### Legacy Shell Scripts

```bash
./scripts/scan-sprint-status.sh [sprints目录]   # 扫描 Sprint 状态
```

---

## ENFORCEMENT - 强制执行机制

**⚠️ 重要：此 section 定义了如何确保 NFlow 流程被严格遵守，而不是被绕过。**

### 问题：为什么流程会被绕过？

传统 skill 是**被动**的 —— 等待命令才执行。如果用户说"继续开发"，Agent 可能直接写代码，跳过：
- E2E 测试用例编写（Phase 7.4）
- TDD 循环（RED → GREEN → REFACTOR）
- Code Review（Phase 9）

### 解决方案：项目标记 + 强制检查

#### 1. 项目标记文件 `.nflow-phase`

每个使用 NFlow 的项目必须在根目录创建 `.nflow-phase` 文件：

```bash
# 项目根目录
touch .nflow-phase
```

文件内容示例：
```
PHASE=8
COMPLEXITY=L2
WORKFLOW=nflow
SPRINT=sprint-02
LAST_COMMAND=/nflow-dev
LAST_UPDATE=2026-04-05
```

#### 2. Agent 进入项目时的强制检查

**规则（适用于所有 Agent）：**

```
当进入一个目录时：
1. 检查是否存在 .nflow-phase 文件
2. 如果存在：
   a. 读取 PHASE 和 CURRENT_SPRINT
   b. 确认当前工作在正确的 Phase
   c. 如果用户说"继续开发"但 PHASE ≠ 8，报错并提示正确命令
3. 如果不存在：
   a. 可以跳过 NFlow 流程
   b. 但仍然遵循基本的开发规范
```

#### 3. 命令执行前置检查

**所有 `/nflow-*` 命令在执行前必须：**

```
1. 验证 .nflow-phase 存在
2. 验证 PHASE 正确（不能跳 Phase，除非走 CHANGE 流程）
3. 验证 CURRENT_SPRINT 存在且在正确状态
4. 如果检查失败，输出错误并拒绝执行
```

#### 4. 开发循环的前置条件

**执行 `/nflow-dev` 前必须满足：**

| 前置条件 | 检查方式 | 如果失败 |
|----------|----------|----------|
| Sprint plan 存在 | `sprints/sprint-XX/plan.md` 存在 | 要求先运行 `/nflow-plan` |
| Backlog 已创建 | `sprints/backlog/stories.md` 存在 | 要求先运行 `/nflow-plan` |
| E2E 测试框架已设置 | `e2e/` 目录或测试配置存在 | 警告但不阻塞 |

**Sprint 结束的前置条件：**

| 前置条件 | 检查方式 | 如果失败 |
|----------|----------|----------|
| 所有 Stories 完成 | Sprint tracker 100% | 不允许开始新 Sprint |
| E2E 测试已执行 | 测试报告存在 | 警告但不阻塞 |
| Sprint Review 已生成 | `sprints/sprint-XX/review.md` 存在 | 警告但不阻塞 |

#### 5. 自动检查脚本

```bash
# 检查项目是否符合 NFlow 规范
python3 scripts/nflow_tools.py check-compliance

# 输出示例：
# ✅ .nflow-phase 存在
# ✅ PHASE=8 (正确)
# ✅ Sprint plan 存在
# ⚠️ E2E 测试框架未设置
# ❌ Sprint-01 review.md 缺失
# 
# 必须修复后才能继续
```

#### 6. 强制执行流程图

```
用户说"继续开发"
        ↓
检查 .nflow-phase 是否存在
        ↓
    不存在 → ⚠️ 警告：此项目未使用 NFlow
    存在 → 读取 PHASE
        ↓
    PHASE ≠ 8? → ❌ 错误：当前 Phase 是 X，请先执行 /nflow-xxx
    PHASE = 8 → 继续
        ↓
    检查 Sprint plan 存在
        ↓
    不存在 → ❌ 错误：Sprint plan 缺失，请先 /nflow-plan
    存在 → 检查 Stories 状态
        ↓
    有 Story 在 TODO? → 执行下一个 TODO Story
    所有完成 → ❌ 错误：Sprint 已完成，请先 /nflow-review
```

### 违反规则的后果

| 违规行为 | 后果 |
|----------|------|
| 在 PHASE ≠ 8 时执行 `/nflow-dev` | 命令拒绝执行，提示当前 Phase |
| 跳过 E2E 测试直接 commit | 下次 `/nflow-dev` 检测到并报警 |
| Sprint 未完成就开新 Sprint | 拒绝创建，强制先做 Review |
| 跳过 Code Review 直接合并 | Git pre-commit hook 阻止 |

### 在 AGENTS.md 中的应用

在 AGENTS.md 中添加规则：

```markdown
## 项目进入规则

当你进入一个目录时：

1. 检查是否存在 `.nflow-phase` 文件
2. 如果存在：
   - 读取文件了解当前 Phase 和 Sprint
   - 确保当前操作符合 Phase 定义
   - 如果不符合，拒绝执行并提示正确命令
3. 如果不存在：
   - 标记为"非 NFlow 项目"
   - 使用简化流程（但仍保持基本规范）
```

### 初始化新项目的正确流程

```bash
# 1. 创建项目目录
mkdir my-project && cd my-project

# 2. 初始化 NFlow
/nflow-init

# 3. NFlow 会自动创建：
#    - .nflow-phase
#    - sprints/backlog/
#    - docs/
#    - workflow-design/

# 4. 设置复杂度
#    - 根据问题判断 L1-L4
#    - 更新 .nflow-phase

# 5. 开始开发
/nflow-dev
```
