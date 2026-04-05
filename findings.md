# 调研发现 - BMad + Superpowers 融合分析

---

## BMad Method 核心提炼

### 两种路径

**Quick Flow（3步）：**
```
/quick-spec → /dev-story → /code-review
```
适用：bug fix、明确范围的小功能（1-15 stories）、无需架构决策

**Full Planning（完整规划）：**
```
PRD → Architecture → Epics & Stories → Sprint Planning → Dev-Story Loop
```
适用：新产品、主要功能、10-50+ stories、需要架构决策

### Scale-Domain-Adaptive Intelligence

| 复杂度 | 流程 |
|--------|------|
| Bug fix | Quick Flow，3命令搞定 |
| 简单功能 | Tech-spec → 实现，30分钟 |
| SaaS 平台 | 完整 PRD + 架构 + Epic + Sprint |
| 企业系统 | + 安全评审 + 合规检查 + DevOps |

### 12种专业化 Agent

PM / Architect / Developer / Scrum Master / Analyst / UX Designer / QA (Quinn) / DevOps / Security / Tech Lead / Docs Writer / Data Analyst

---

## Superpowers 核心提炼

### 强制多阶段工作流

```
brainstorming → spec-writing → implementation-planning → coding → debugging
```

**不可跳过任何阶段，必须按顺序执行。**

### brainstorming 阶段（Socratic 方法）

- 问澄清性问题
- 探索替代方案
- 展示设计分段给用户确认
- 输出保存的设计文档（design.md）
- **核心：确保 AI 和用户对需求理解一致后再动手**

### TDD 测试驱动

- 先写测试
- 再写实现
- 用测试验证实现

### Change Control（需求变更控制）

Superpowers 流程内置变更门控：
- 任何需求变更必须重新进入 brainstorming
- 评估影响范围
- 更新 spec
- 影响实现计划

---

## 两者共同点

1. **渐进式复杂度**：小任务简单流程，大任务完整流程
2. **文档驱动**：规格说明书是核心
3. **AI 作为协作者**：不是替代思考，是增强思考
4. **阶段性门控**：不跳步，每阶段有明确输入输出

---

## 两者差异

| 维度 | BMad | Superpowers |
|------|------|-------------|
| 团队/个人 | 面向团队，有多 Agent 协作 | 面向个人/小团队，sub-agent 并行 |
| 需求澄清 | 可选（/bmad-brainstorming） | 强制（brainstorming 阶段） |
| 测试 | QA Agent 负责 | TDD 内置，强制先写测试 |
| 变更控制 | Scrum Master 把控 | 内置 Change Control Gate |
| 规划粒度 | Epic → Story → Sprint | Spec → Implementation Plan |

---

## 老大的特殊要求：需求变更可控

Superpowers 的 Change Control Gate 是亮点：
- 变更不是随意的
- 变更需要评估影响
- 变更需要更新文档
- 变更需要重新确认

**需要设计一个明确的变更控制机制。**
