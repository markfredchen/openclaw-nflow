# NFlow Agent Personas

NFlow 工作流中的 Agent 角色定义。全部遵循 agency-agents 格式。

---

## 角色总览

| Agent | Emoji | Color | 核心职责 |
|-------|-------|-------|----------|
| [Lead Agent](./01-lead-agent.md) | 🎯 | 🟣 purple | 项目总负责，复杂度判定 |
| [Trend Researcher Agent](./00-trend-researcher-agent.md) | 🔍 | 🟣 violet | 市场调研，竞品分析 |
| [PM Agent](./02-pm-agent.md) | 📋 | 🔵 blue | 需求管理，PRD |
| [UI Designer Agent](./00-ui-designer-agent.md) | 🎨 | 🩻 magenta | 设计系统，风格规范 |
| [UX Designer Agent](./00-ux-designer-agent.md) | 🎨 | 🟣 purple | 线框图设计，交互设计 |
| [Architect Agent](./03-architect-agent.md) | 🏗️ | 🟠 orange | 技术设计，架构决策 |
| [Frontend Developer Agent](./00-frontend-developer-agent.md) | 🖥️ | 🩵 cyan | 前端开发，React/Vue/Angular |
| [Backend Developer Agent](./00-backend-developer-agent.md) | 🏗️ | 🔵 blue | 后端开发，API/数据库 |
| [Mobile App Builder Agent](./00-mobile-app-builder-agent.md) | 📲 | 🟣 purple | 移动端开发，iOS/Android |
| [Git Workflow Master Agent](./00-git-workflow-master-agent.md) | 🌿 | 🟠 orange | Git worktree，分支管理 |
| [Code Reviewer Agent](./00-code-reviewer-agent.md) | 👁️ | 🟣 purple | 代码审查，质量把关 |
| [Tech Lead Agent](./05-techlead-agent.md) | 🔧 | 🟡 yellow | 代码质量，技术指导 |
| [QA Agent](./06-qa-agent.md) | 🎯 | 🔴 red | 测试策略，质量保障 |
| [Scrum Master Agent](./07-scrummaster-agent.md) | ⚡ | 🩵 cyan | Sprint 管理，流程把控 |
| [Sprint Prioritizer Agent](./00-sprint-planner-agent.md) | 📊 | 🩵 teal | Sprint 规划，优先级排序 |
| [Analyst Agent](./08-analyst-agent.md) | 📊 | 🩷 pink | 调研分析，风险评估 |

---

## 流程中的 Agent 参与矩阵

| 阶段 | Lead | Trend | PM | UI | UX | Arch | Frontend | Backend | Mobile | Git | CodeReview | TechLead | QA | Scrum | SprintPri | Analyst |
|------|------|-------|----|----|----|-----|----------|---------|--------|----|-----------|----------|----|----|----------|---------|
| 项目初始化 | ✅ | | | | | | | | | | | | | | | |
| Phase 1.1 市场调研 | | ✅ | | | | | | | | | | | | | | |
| Phase 1.2 需求文档 | | | ✅ | | | | | | | | | | | | | |
| Phase 1.3 架构设计 | | | | | | ✅ | | | | | | | | | | |
| Phase 2 设计系统 | | | | ✅ | | | | | | | | | | | | |
| Phase 3 UX 设计 | | | | | ✅ | | | | | | | | | | | |
| Phase 4 人工审核 | 🤖 | 🤖 | 🤖 | 🤖 | 🤖 | 🤖 | | | | | | | | | 🤖 | |
| Phase 4.5 UI Prototype | | | | | | ✅ UI Designer | | | | | | | | | | |
| Phase 5 Backlog | | | **PM** | | | **Architect** | | | | | | | | | | |
| Phase 6 Sprint | | | | | | | | | | | | | | ✅ | **✅** | |
| **Phase 7 开发** | | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | | | | | |
| Phase 8 Review | | | | | | | | | | | | ✅ | ✅ | | | |
| CHANGE | ✅ | | ✅ | | | ✅ | | | | | | | | ✅ | | |

---

## Phase 7 开发 Agent 角色

| Agent | 职责 |
|-------|------|
| **Git Workflow Master** | 创建 worktree、合并到 main |
| **Frontend Developer** | 前端 UI 实现（TDD）|
| **Backend Developer** | 后端 API 实现（TDD）|
| **Mobile App Builder** | 移动端实现（React Native/Flutter）|
| **Code Reviewer** | 代码审查（安全性/可维护性/性能）|

---

## 激活 Agent

在 OpenClaw / Claude Code 中，通过读取对应 agent 文件激活对应 persona：

```
读取 agents/01-lead-agent.md → 激活 Lead Agent
读取 agents/00-frontend-developer-agent.md → 激活 Frontend Developer
...
```

每个 Agent 文件包含：
- **Identity** — name / description / color / emoji / vibe
- **Personality** — Role / Personality / Memory / Experience
- **Technical Focus** — 技能重点
- **Workflow** — 核心工作流程
- **Success Metrics** — 成功标准
- **实用模板** — 代码示例/规范
