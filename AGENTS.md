# NFlow Agents

## Agent 激活方式

### 方式 1：直接引用

在对话中使用 `@Agent名称`：

```
@Lead Agent
@PM Agent
@Architect Agent
@Developer Agent
```

### 方式 2：读取文件激活

读取对应 Agent 的 persona 文件即可激活：

```
读取 agents/01-lead-agent.md → 激活 Lead Agent
读取 agents/02-pm-agent.md → 激活 PM Agent
读取 agents/03-architect-agent.md → 激活 Architect Agent
读取 agents/00-frontend-developer-agent.md → 激活 Frontend Developer
读取 agents/00-backend-developer-agent.md → 激活 Backend Developer
读取 agents/00-mobile-app-builder-agent.md → 激活 Mobile App Builder
读取 agents/00-git-workflow-master-agent.md → 激活 Git Workflow Master
读取 agents/00-code-reviewer-agent.md → 激活 Code Reviewer
读取 agents/06-qa-agent.md → 激活 QA Agent
```

---

## Agent 快速索引

| Agent | 文件 | 用途 |
|-------|------|------|
| Lead Agent | `agents/01-lead-agent.md` | 项目总负责，复杂度判定 |
| Trend Researcher Agent | `agents/00-trend-researcher-agent.md` | 市场调研，竞品分析 |
| PM Agent | `agents/02-pm-agent.md` | 需求管理，PRD |
| UI Designer Agent | `agents/00-ui-designer-agent.md` | 设计系统，风格规范 |
| UX Designer Agent | `agents/00-ux-designer-agent.md` | 线框图设计，交互设计 |
| Architect Agent | `agents/03-architect-agent.md` | 技术架构，API 设计 |
| Frontend Developer | `agents/00-frontend-developer-agent.md` | React/Vue/Angular |
| Backend Developer | `agents/00-backend-developer-agent.md` | Python + NestJS |
| Mobile App Builder | `agents/00-mobile-app-builder-agent.md` | iOS/Android |
| Git Workflow Master | `agents/00-git-workflow-master-agent.md` | Git worktree/commit |
| Code Reviewer | `agents/00-code-reviewer-agent.md` | 代码审查 |
| QA Agent | `agents/06-qa-agent.md` | 测试策略，E2E |
| Tech Lead Agent | `agents/05-techlead-agent.md` | 技术指导 |
| Scrum Master Agent | `agents/07-scrummaster-agent.md` | Sprint 管理 |
| Sprint Prioritizer Agent | `agents/00-sprint-planner-agent.md` | 优先级排序 |
| Analyst Agent | `agents/08-analyst-agent.md` | 风险评估 |

---

## 在 NFlow 命令中的使用

每个 NFlow 命令执行时会自动指定对应的 Agent。例如：

### `/nflow-init`
```
激活: Lead Agent
```

### `/nflow-requirements`
```
激活: Trend Researcher Agent → PM Agent → Architect Agent
```

### `/nflow-design`
```
激活: UI Designer Agent → UX Designer Agent
```

### `/nflow-dev`
```
激活: Git Workflow Master Agent + Developer Agent(s) + QA Agent + Code Reviewer Agent
```

---

## Agent 切换

如果需要切换当前 Agent，直接读取新的 agent 文件即可：

```
读取 agents/02-pm-agent.md
→ PM Agent 激活

读取 agents/03-architect-agent.md  
→ Architect Agent 激活
```

---

## 记忆保持

每次切换 Agent 时，新的 Agent 会继承：
- 项目上下文
- 当前 Phase 进度
- 之前的决策和输出

不需要重复说明背景，直接执行新 Agent 的职责即可。
