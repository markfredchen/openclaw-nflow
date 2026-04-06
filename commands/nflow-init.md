# /nflow-init

## 项目初始化

**Phase:** Phase 0

**执行时机:** 开始新项目时

**执行 Agent:** Lead Agent

---

## 执行步骤

### 1. 确定项目路径（必须）

**询问用户：**
```
新项目路径是什么？
示例：/Users/name/projects/my-app
```

**验证：**
- 路径不能为空
- 如果目录不存在，询问是否创建
- 如果目录存在且有文件，询问是否继续

```
❌ 错误：项目路径不能为空

请提供项目路径，例如：
  /Users/name/projects/my-app
  ~/projects/my-app
```

---

### 2. 确定项目基本信息

询问用户：
- 项目名称（默认：取路径最后一段）
- 项目目标/愿景
- 目标用户
- 预计上线时间

---

### 3. 确定开发方式

**询问用户：**
```
开发方式：
A. OpenClaw（全权负责）- 不使用外部工具
B. 外部工具（指定用 Claude Code/Codex/Gemini 开发）
C. 混合模式（OpenClaw 协调 + 外部工具执行）
```

**开发方式说明：**

| 方式 | 说明 | 使用场景 |
|------|------|----------|
| **A. OpenClaw** | 当前会话独立完成所有开发任务 | 小型项目、快速原型 |
| **B. 外部工具** | 指定 Claude Code/Codex 等执行开发 | 需要特定工具能力 |
| **C. 混合模式** | OpenClaw 协调，外部工具执行 | 中大型项目，多 Agent 协作 |

---

### 4. 确定开发工具（可选）

**仅在选择 B 或 C 时询问：**

询问用户：**"使用哪些工具执行开发？"**

```
请选择开发工具（可多选）：
□ Claude Code  - Anthropic 开发工具
□ Codex        - OpenAI 开发工具
□ Gemini      - Google 开发工具
□ Cursor      - Cursor IDE
□ 其他：____
```

**验证已安装的工具：**

| 工具 | 验证命令 |
|------|----------|
| Claude Code | `claude --version` |
| Codex | `codex --version` |
| Gemini | `gemini --version` |
| Cursor | `cursor --version` |

**如果未安装：** 提示用户安装或选择其他已安装的工具

---

### 5. 确定技术栈

询问用户：**"请选择技术栈："**

**编程语言：**
```
A. Python
B. TypeScript
C. Go
D. Java
E. Rust
F. 其他：____
```

**前端框架：**
```
A. React
B. Vue
C. Angular
D. Next.js
E. Nuxt
F. Svelte
G. 其他：____
```

**后端框架：**
```
A. FastAPI (Python)
B. NestJS (Node.js)
C. Express (Node.js)
D. Django (Python)
E. Spring Boot (Java)
F. Gin (Go)
G. 其他：____
```

**数据库：**
```
A. PostgreSQL
B. MySQL
C. MongoDB
D. Redis
E. SQLite
F. 其他：____
```

---

### 6. 评估复杂度等级

根据以下标准判断：

| 等级 | 标准 | 流程 |
|------|------|------|
| L1 | Bug fix、明确小改动（1-3 stories） | Quick Flow |
| L2 | 单一模块功能开发（4-15 stories） | Standard Flow |
| L3 | 多模块/跨团队（16-50 stories） | Full Flow |
| L4 | 架构决策、安全合规（50+ stories） | Enterprise Flow |

---

### 7. 验证开发环境（仅外部工具模式）

**对每个选择的开发工具执行验证：**

```bash
# Claude Code
claude --version

# Codex
codex --version

# Gemini
gemini --version

# Cursor
cursor --version
```

**如果验证失败：**
```
⚠️ [工具名称] 未安装或不可用
建议：
1. 安装 [工具名称]
2. 或选择其他已安装的工具
```

---

### 8. 创建项目目录结构

```
{project-path}/
├── nflow-docs/                       # NFlow 所有文档输出
│   ├── docs/                        # 文档
│   │   ├── project-config.md        # 项目配置（Phase 0）
│   │   ├── market-research-report.md # 市场调研（Phase 1）
│   │   ├── requirements-extracted.md # 需求提取（Phase 1）
│   │   ├── brainstorming-record.md  # Brainstorming 记录（Phase 1）
│   │   ├── requirements-confirmed.md # 需求确认书（Phase 1）
│   │   ├── prd.md                  # 产品需求文档（Phase 1）
│   │   ├── architecture.md         # 架构文档（Phase 1）
│   │   └── project-memory.md        # 项目记忆
│   │
│   ├── design/                     # 设计输出
│   │   ├── design-pattern.json      # 设计系统（Phase 2）
│   │   ├── wireframes/             # 线框图（Phase 3）
│   │   │   ├── README.md
│   │   │   └── page-*.md
│   │   └── mockups/                # UI 原型（Phase 5）
│   │       ├── README.md
│   │       └── page-*.html
│   │
│   └── sprints/                    # Sprint 输出
│       ├── backlog.md              # 待办列表（Phase 6）
│       ├── decision-log.md         # 决策日志
│       ├── sprint-01/
│       │   ├── sprint-plan.md      # Sprint 计划
│       │   ├── user-stories-tracker.md # Story 追踪
│       │   ├── implementations/   # Story 实现代码
│       │   ├── test-reports/      # 测试报告
│       │   ├── screenshots/       # E2E 截图
│       │   ├── acceptance-report-*.html # 验收报告
│       │   └── review.md          # Sprint 回顾
│       └── sprint-02/
│
├── deploy/                          # 部署文档（独立）
│   ├── local/                      # 本地环境
│   ├── staging/                    # 预发布环境
│   ├── production/                 # 生产环境
│   └── migrations/                # 数据迁移
│
├── change-log.md                    # 变更记录
│
└── .claude/
    └── skills/
        └── nflow/                  # NFlow 技能

.nflow/                             # NFlow 项目配置
├── notify-config.json              # 通知渠道配置
└── project-state.json             # 项目状态
```

### 8.1 初始化记忆文件

**使用 Python 脚本（推荐）：**

```bash
# 初始化项目记忆和决策日志
python3 .claude/skills/nflow/scripts/nflow_tools.py init-memory "{project-name}" L{1-4} "{dev-mode}"
```

**手动创建：**

如果脚本不可用，手动创建以下文件：

**docs/project-memory.md:**
```markdown
# Project Memory

**项目:** {project-name}
**创建日期:** {date}
**最后更新:** {date}
**当前阶段:** Phase 0

---

## 项目信息

| 字段 | 值 |
|------|-----|
| 项目名称 | {project-name} |
| 项目路径 | {path} |
| 复杂度等级 | L{n} |

---

## 当前状态

### Sprint 进度

| Sprint | 完成 | 总计 | 状态 | 当前 Story |
|--------|------|------|------|------------|

### 关键架构决策

| ID | 决策 | 日期 |
|----|------|------|

### 已知问题

| 问题 | 影响 | 状态 |
|------|------|------|
```

**sprints/decision-log.md:**
```markdown
# Decision Log

**项目:** {project-name}
**创建日期:** {date}

---

## 架构决策

| ID | 日期 | 决策 | 原因 | 替代方案 | 状态 |
|----|------|------|------|----------|------|

---

## 技术选型

| ID | 日期 | 选择 | 原因 | 替代方案 | 状态 |
|----|------|------|------|----------|------|
```
```

**输出文件路径速查：**

| Phase | 输出文件 | 路径 |
|-------|----------|------|
| Phase 0 | project-config.md | `docs/` |
| Phase 1 | market-research-report.md | `docs/` |
| Phase 1 | prd.md | `docs/` |
| Phase 1 | architecture.md | `docs/` |
| Phase 2 | design-pattern.json | `design/` |
| Phase 3 | wireframes/ | `design/wireframes/` |
| Phase 5 | mockups/ | `design/mockups/` |
| Phase 6 | backlog.md | `sprints/` |
| Phase 7 | sprint-plan.md | `sprints/sprint-XX/` |
| Phase 7 | user-stories-tracker.md | `sprints/sprint-XX/` |
| CHANGE | change-log.md | 项目根目录 |

---

### 9. 确定通知渠道

**询问用户：**
```
通知发送到哪里？

当前已配置的渠道：
  1. Telegram (default) ✅

请选择通知渠道：
A. Telegram - 发送消息到 Telegram
B. Discord - 发送消息到 Discord
C. Slack - 发送消息到 Slack
D. 暂不启用 - 不发送通知
```

**支持的渠道：**
| 渠道 | 说明 |
|------|------|
| Telegram | 即时通讯，配置简单 |
| Discord | 适合团队协作 |
| Slack | 适合企业环境 |
| WhatsApp | 即时通讯 |
| Signal | 私密通讯 |
| iMessage | Apple 生态 |

**如果选择已配置的渠道：**
- 保存到 `.nflow/notify-config.json`
- 使用配置的默认 target

**如果选择暂不启用：**
- 设置 `enabled: false`
- 之后可通过编辑 `.nflow/notify-config.json` 启用

---

### 10. 初始化 project-config.md

```markdown
# Project Config

**项目名称:** [名称]
**创建日期:** YYYY-MM-DD
**项目路径:** [绝对路径]
**复杂度等级:** L1 / L2 / L3 / L4
**负责人:** [用户]

## 项目信息
- **目标用户:** [描述]
- **上线时间:** [日期]

## 开发方式
| 配置 | 值 |
|------|-----|
| 开发模式 | OpenClaw / 外部工具 / 混合模式 |
| 主要工具 | [如使用外部工具] |
| 备用工具 | [如使用外部工具] |

## 技术栈配置
| 类别 | 选择 | 验证状态 |
|------|------|----------|
| 编程语言 | Python | ✅ 已安装 |
| 前端框架 | React | ✅ 已安装 |
| 后端框架 | FastAPI | ✅ 已安装 |
| 数据库 | PostgreSQL | ✅ 已安装 |

## 团队配置
| Agent | 角色 |
|-------|------|
| Lead Agent | 项目总负责 |
| [其他Agents] | ... |

## 审核记录
| 阶段 | 状态 | 日期 |
|------|------|------|
| Phase 0 | ✅ 完成 | YYYY-MM-DD |
```

---

## 输出

- ✅ `project-config.md` 已创建（含开发方式和工具配置）
- ✅ 复杂度等级已确定
- ✅ 目录结构已创建
- ✅ 所有选择的工具已验证安装状态（如适用）
- ✅ `docs/project-memory.md` 已初始化
- ✅ `sprints/decision-log.md` 已初始化
- ✅ `.nflow/notify-config.json` 已创建（通知渠道配置）
- ✅ `.nflow/project-state.json` 已创建（项目状态）

---

## 下一步

```
/nflow-requirements
```

---

## 快速问答模板

```
Q1: "新项目路径是什么？"（必须）
    → 验证路径

Q2: "项目名称是什么？"（可选，有默认值）

Q3: "开发方式是什么？"
    A. OpenClaw（全权负责）
    B. 外部工具
    C. 混合模式
    → 如果 B/C，选择工具并验证

Q4: "选择什么技术栈？"
    → 编程语言、前端框架、后端框架、数据库

Q5: "预计上线时间是什么时候？"

Q6: "通知发送到哪个渠道？"
    A. Telegram（默认）
    B. Discord
    C. Slack
    D. 暂不启用
```

---

## 决策规则

| 选择 | 结果 |
|------|------|
| 不指定开发工具 | OpenClaw 独立完成所有开发 |
| 指定 Claude Code | Claude Code 执行开发，OpenClaw 协调 |
| 指定多个工具 | OpenClaw 协调，多工具协作执行 |
