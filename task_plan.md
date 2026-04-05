# 自定义开发工作流设计 - 任务计划

**目标：** 融合 BMad Method + Superpowers 的优点，设计一套适合老大自己的开发工作流
**创建日期：** 2026-04-05

---

## 阶段状态

| 阶段 | 状态 | 说明 |
|------|------|------|
| Phase 1: 调研整理 | ✅ 完成 | BMad + Superpowers 核心要素提炼 |
| Phase 2: 取舍分析 | ✅ 完成 | 确定融合策略 + Agent Persona |
| Phase 3: 工作流设计 | ✅ 完成 | 双轨制 L1-L4 + 需求变更控制 |
| Phase 4: Phase 1 结构 | ✅ 完成 | 三步流程：Trend Researcher → PM → Architect |
| Phase 5: Phase 2 设计系统 | ✅ 完成 | UI Designer Agent + design-pattern.json |
| Phase 6: Phase 3 UX | ✅ 完成 | UX Designer Agent + ASCII 线框图模板 |
| Phase 7: Phase 4 人工审核 | ✅ 完成 | Approval Gate + 审核检查清单 |
| Phase 8: Phase 5 Backlog | ✅ 完成 | Epics + User Stories 生成 |
| Phase 9: Phase 6 Sprint | ✅ 完成 | Sprint Prioritizer + 状态追踪 |
| Phase 10: Phase 7 实现 | ✅ 完成 | TDD + Git Worktree + Code Review |
| Phase 11: 收尾 | 🔄 进行中 | 模板文件整理 + 收尾 |

---

## Phase 1: 调研整理 ✅

### BMad Method 核心要素

**两种流程路径：**
- **Quick Flow（快速流程）**：3步搞定 bug/小功能 → `/quick-spec` → `/dev-story` → `/code-review`
- **Full Planning（完整规划）**：适合产品/复杂功能，有完整 PRD → 架构 → Epic → Sprint 流程

**Scale-Domain-Adaptive Intelligence（规模-领域-自适应）：**
- Bug fix → Quick Flow
- 简单功能 → Tech-spec → 实现，30分钟
- SaaS 平台 → 完整 PRD + 架构 + Epic + Sprint
- 企业系统 → + 安全评审 + 合规 + DevOps

**12+ 专业化 AI Agent 团队：**
PM / Architect / Developer / Scrum Master / Analyst / UX Designer / QA / DevOps / Security / Tech Lead / Docs Writer / Data Analyst

**核心哲学：** AI 是协作伙伴，不是替代思考的工具。结构化流程带出最佳思考。

---

### Superpowers 核心要素

**强制多阶段工作流（按顺序执行，不可跳过）：**
1. **brainstorming** — 澄清需求，问问题，展示设计供用户确认（Socratic 方法）
2. **spec-writing** — 写详细规格说明书
3. **implementation-planning** — 制定实现计划
4. **coding** — TDD 测试驱动开发
5. **debugging** — 系统性调试

**关键原则：**
- 在写任何代码之前，必须完成前面的阶段
- brainstorming 阶段必须输出保存的设计文档（design.md）
- 使用 specialized sub-agents 并行处理子任务
- TDD — 先写测试，再写实现

---

## Phase 2: 取舍分析（融合策略）

### 共同优点（两者都有，保留）：
- ✅ 强制阶段性流程（不跳步）
- ✅ 强调在写代码前先理解需求
- ✅ 文档/规格书作为持久化记忆
- ✅ 复杂度自适应（小活快办，大活细做）

### BMad 特有（值得借鉴）：
- 📦 12种专业化 Agent 分工（PM/Architect/QA...）
- 📊 Quick Flow vs Full Planning 双轨制
- 🎯 Scale-Domain-Adaptive（复杂度自动检测适配）
- 🗺️ 完整的产品路线图概念（PRD → Epic → Story → Sprint）

### Superpowers 特有（值得借鉴）：
- 🎯 **brainstorming 强制澄清需求** — 在动手前问清楚问题
- 🧪 TDD 测试驱动
- 🔒 **需求变更必须有明确控制**（内置在流程里）
- 📐 规格说明书驱动开发

### 老大特别强调：需求变更可控

这是 Superpowers 的核心优势之一：
- **Change Control Gate**：需求变更必须经过明确流程
- 不是拒绝变更，而是确保变更被正确评估和记录

---

## 下一步

继续 Phase 3：设计完整的融合工作流
