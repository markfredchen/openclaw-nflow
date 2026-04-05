# NFlow - 自定义开发工作流 🏗️

**版本：** 1.0.0  
**融合：** BMad Method + Superpowers  
**适用平台：** OpenClaw / Claude Code / Codex / Gemini

---

## 为什么选择 NFlow

- **结构化开发** — 10 个命令覆盖从需求到上线的完整流程
- **TDD 开发** — RED → GREEN → REFACTOR 强制循环
- **多 Agent 协作** — 16 个专业化 Agent 分工明确
- **变更控制** — Change Control Gate 确保需求可控
- **记忆管理** — 项目记忆跨会话持久化

---

## 适用场景

- 从零构建复杂项目
- 需要多 Agent 协作的中大型项目
- 追求 TDD 和代码质量的团队
- 需要结构化开发流程的个人开发者

---

## 命令示例

- `/nflow-init` — 初始化新项目
- `/nflow-requirements` — 定义产品需求
- `/nflow-plan` — 规划 Sprint
- `/nflow-dev` — 开始开发循环
- `/nflow-review` — Sprint 回顾

---

## 目录结构

```
nflow/
├── SKILL.md                      # Skill 入口
├── README.md                     # 英文说明
├── README_zh_cn.md             # 中文说明
├── commands/                     # 10 个命令文件
│   ├── nflow-init.md           # 项目初始化
│   ├── nflow-requirements.md   # 需求定义
│   ├── nflow-design.md         # 设计系统
│   ├── nflow-prototype.md      # 原型设计
│   ├── nflow-plan.md           # Sprint 规划
│   ├── nflow-dev.md            # 开发循环
│   ├── nflow-resume.md         # 恢复开发
│   ├── nflow-story.md          # 单个 Story
│   ├── nflow-review.md          # 最终评审
│   ├── nflow-new-spec.md       # 新需求处理
│   └── nflow-hotfix-planning.md # 紧急修复 Sprint 规划
│
├── agents/                      # 16 个 Agent persona
│   ├── 01-lead-agent.md
│   ├── 02-pm-agent.md
│   ├── 03-architect-agent.md
│   ├── 04-developer-agent.md
│   ├── 05-techlead-agent.md
│   ├── 06-qa-agent.md
│   ├── 07-scrummaster-agent.md
│   ├── 08-analyst-agent.md
│   └── 00-*-agent.md (8 个专项 Agent)
│
├── templates/                   # 模板文件
│   ├── project-memory.md        # 项目记忆
│   ├── decision-log.md          # 决策日志
│   ├── sprint-review.md         # Sprint 回顾
│   └── ...
│
└── scripts/                    # 工具脚本
    ├── install-openclaw.sh
    ├── install-claude-code.sh
    ├── install-codex.sh
    ├── nflow_tools.py          # 状态管理
    └── spawn-dev-agent.py      # 外部 Agent 启动
```

---

## 快速安装

### OpenClaw

```bash
# 全局安装
./scripts/install-openclaw.sh --mode agent

# 激活 skill
/nflow
```

### Claude Code

```bash
# 安装到项目目录
./scripts/install-claude-code.sh --local /path/to/project

# 直接使用命令
/nflow-init
```

### Codex

```bash
# 安装
./scripts/install-codex.sh --local /path/to/project
```

---

## 工作流概览

| Phase | 命令 | 说明 |
|-------|------|------|
| 0 | `/nflow-init` | 项目初始化 |
| 1 | `/nflow-requirements` | 市场调研 → PRD → 架构 |
| 2-3 | `/nflow-design` | 设计系统 + 线框图 |
| 4-5 | `/nflow-prototype` | 原型 + 人工审核 |
| 6-7 | `/nflow-plan` | Backlog + Sprint 规划 |
| 8 | `/nflow-dev` | 开发循环 |
| 9 | `/nflow-review` | 最终评审 |

---

## 核心特性

### TDD 开发循环
```
8.5 TDD 开发 ←→ 8.8 测试
          ↓
     RED → GREEN → REFACTOR
```

### 3 次失败规则
- 测试失败 3 次 → 人工干预
- 审查失败 3 次 → 人工干预

### Git Worktree 隔离
每个 Story 在独立 worktree 中开发，互不干扰。

### E2E 测试截图
- 每个测试步骤自动截图
- 文件名格式：`us{id}-case{id}-step{n}.png`
- 自动生成含截图的 HTML 验收报告

### Sprint Review HTML 报告
- 每个 Sprint 自动生成 `review-report.html`
- 包含指标、回顾、质量检查和下一步建议

### 记忆管理
- `project-memory.md` — 项目全局记忆
- `decision-log.md` — 决策审计
- `sprint-*/review.md` — Sprint 回顾

---

## 开源协议

MIT
