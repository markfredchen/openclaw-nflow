# /nflow-review

## Sprint 回顾 + 最终 Code Review

**Phase:** Phase 9

**执行时机:** Sprint 中所有 Stories 完成后

**执行 Agent:** Tech Lead Agent + QA Agent + Scrum Master Agent

---

## 执行步骤

### 1. Sprint 状态检查

**使用脚本检查（避免 LLM 消耗 token）：**

```bash
python3 scripts/nflow_tools.py scan-sprints
```

**检查项:**
- [ ] 所有 Stories 是否都是 `✅ DONE`？
- [ ] 所有 Stories 是否都有 `test-report-{id}.md`？
- [ ] Sprint 容量利用率如何？
- [ ] 有哪些遗留问题？

---

### 2. Sprint 回顾（Sprint Retrospective）

**生成 Sprint 回顾文档：**

```bash
# 使用模板生成 sprints/sprint-XX/review.md
# 模板: templates/sprint-review.md
```

**Sprint 回顾内容：**

#### 做得好的
- TDD 流程执行顺利
- Code Review 及时
- Git Worktree 隔离有效

#### 需要改进
- 外部依赖评估不足
- 预估误差较大
- 审查反馈循环太慢

#### 下个 Sprint 关注点
- 第三方 API 提前确认
- 增加预估 buffer
- 缩短审查反馈周期

---

### 3. 更新项目记忆（必须）

**使用脚本更新记忆：**

```bash
# 更新 Sprint 状态
python3 scripts/nflow_tools.py update-memory sprint_progress=sprint-XX,done=5,total=5,status=DONE

# 记录决策（如果有新决策）
python3 scripts/nflow_tools.py log-decision ARCH "决策内容" "原因"
```

**更新 `docs/project-memory.md`：**

```markdown
## Sprint 回顾

### Sprint XX (YYYY-MM-DD)

**完成情况:**
- 计划故事点: {n}
- 完成故事点: {n}
- 完成率: {n}%

**做得好的:**
- {point}

**需要改进:**
- {point}

**教训:**
- {lesson}
```

**更新 `sprints/decision-log.md`：**

如果有架构或技术决策变更，记录到决策日志。

---

### 4. 完整性检查

**Tech Lead Agent 检查:**
- [ ] 代码符合 Architecture
- [ ] 无安全漏洞
- [ ] 测试覆盖率达标
- [ ] 文档已更新

**QA Agent 检查:**
- [ ] 单元测试 > 80%
- [ ] 集成测试 > 60%
- [ ] E2E 测试覆盖核心流程
- [ ] 无高/中风险 bug 未解决

---

### 5. 生成 Review Report

**输出:** `sprints/sprint-XX/review.md`

**模板:** `templates/sprint-review.md`

### 6. 生成 Sprint Review HTML 报告

**使用脚本生成（推荐）：**

1. LLM 返回 JSON 数据
2. 脚本处理模板生成 HTML

**JSON 数据格式：**

```json
{
  "sprint_number": "01",
  "date": "2026-04-05",
  "team": "Team A",
  "completed_stories": 5,
  "total_stories": 6,
  "completion_rate": 83,
  "planned_points": 21,
  "completed_points": 18,
  "stories": [
    {"id": "STORY-001", "name": "用户注册", "points": 3, "status": "DONE"}
  ],
  "went_well": ["TDD 流程顺利", "Code Review 及时"],
  "improve": ["预估误差大", "外部依赖需确认"],
  "next_sprint": ["提前确认第三方 API"]
}
```

**生成命令：**

```bash
python3 scripts/generate_html_report.py \\
    --template templates/sprint-review-report-template.html \\
    --data /tmp/sprint-review-data.json \\
    --output sprints/sprint-01/review-report.html
```

**模板:** `templates/sprint-review-report-template.html`

**输出:** `sprints/sprint-XX/review-report.html`

### 7. 完整性验证

```markdown
# Sprint {n} Review

**Sprint:** sprint-{n}
**日期:** YYYY-MM-DD
**团队:** {team}

---

## 执行摘要

| 指标 | 值 |
|------|-----|
| 计划故事点 | {planned} |
| 完成故事点 | {completed} |
| 完成率 | {rate}% |
| Stories 完成 | {done}/{total} |
| 阻塞时间 | {hours}h |

---

## 完成 Stories

| Story ID | 名称 | 故事点 | 状态 |
|----------|------|--------|------|
| STORY-001 | {名称} | {n} | ✅ DONE |

---

## 未完成 Stories

| Story ID | 名称 | 故事点 | 原因 |
|----------|------|--------|------|
| STORY-002 | {名称} | {n} | {原因} |

---

## 做得好的

- {point 1}
- {point 2}

---

## 需要改进

- {point 1}
- {point 2}

---

## 下个 Sprint 关注点

- {point 1}
- {point 2}

---

## 人工干预记录

| 日期 | Story | 问题 | 解决方案 |
|------|-------|------|----------|
| YYYY-MM-DD | STORY-001 | {问题} | {方案} |

---

## 代码质量报告

| 检查项 | 状态 | 备注 |
|--------|------|------|
| Architecture 合规 | ✅ | 无偏离 |
| 安全扫描 | ✅ | 0 高/中风险 |
| 测试覆盖率 | ✅ | {n}% |
| 文档更新 | ⚠️ | {备注} |

---

## 遗留问题

| ID | 问题描述 | 影响 | 解决方案 |
|----|----------|------|----------|
| ISSUE-001 | ... | ... | ... |

---

## 下一步建议

- ISSUE-001 需要在 Sprint {n+1} 优先处理
- 建议增加 API 文档自动生成
```

---

### 7. 完整性验证

```bash
# 验证所有必需文件存在
python3 scripts/nflow_tools.py scan-sprints
```

---

### 8. 自动创建新 Stories（处理潜在问题）

**如果发现潜在问题或 Bug，需要自动创建新 User Story：**

**触发条件：**
- 代码审查中发现但未修复的问题
- 测试中发现但未解决的问题
- 用户反馈的问题
- 技术债务

**创建流程：**

```
发现问题
    ↓
评估影响（高/中/低）
    ↓
确定优先级
    ├── 高 → 当前 Sprint 紧急修复
    ├── 中 → 下个 Sprint 处理
    └── 低 → Backlog
    ↓
创建新 Story
    ↓
更新 backlog.md
    ↓
如果是紧急 → 更新当前 Sprint 计划
```

**新 Story 模板：**

```markdown
### STORY-XXN: {问题简述}

**Epic:** EPIC-XX
**优先级:** P0 / P1 / P2
**故事点:** {估算}
**来源:** Sprint {n} Review 发现

**AS A** {用户角色}
**I WANT** {功能描述}
**SO THAT** {价值}

**问题描述:**
{详细描述发现的问题}

**Acceptance Criteria:**
- [ ] {标准1}
- [ ] {标准2}

**相关文件:**
- {相关文件路径}
```

**使用脚本创建：**

```bash
# 如果有自动化脚本
python3 scripts/nflow_tools.py create-story-from-issue \
    --sprint sprint-XX \
    --title "问题标题" \
    --priority P1 \
    --points 3 \
    --description "问题描述" \
    --source "Sprint Review"
```

**更新 backlog.md：**

在 `sprints/backlog.md` 中添加新 Story，并更新 Epic 关联。

**更新 change-log.md：**

```markdown
| CR-XXX | YYYY-MM-DD | BUG_FIX | {问题} | 新增 STORY-XXN | APPROVED | EPIC-XX |
```

---

## 输出文件

| 文件 | 路径 | Agent |
|------|------|-------|
| Sprint 回顾 | `sprints/sprint-XX/review.md` | Scrum Master |
| Sprint Review HTML | `sprints/sprint-XX/review-report.html` | Scrum Master |
| 项目记忆更新 | `docs/project-memory.md` | Lead Agent |
| 决策日志更新 | `sprints/decision-log.md` | Lead Agent |
| Review Report | `sprints/sprint-XX/review.md` | Tech Lead + QA |
| 新增 Stories | `sprints/backlog.md`（已更新）| PM Agent |
| 变更记录 | `change-log.md`（已更新）| PM Agent |

---

## 记忆更新清单

**Phase 9 完成后必须更新：**

- [ ] `docs/project-memory.md` - 更新 Sprint 进度
- [ ] `docs/project-memory.md` - 记录做得好的/需要改进的
- [ ] `docs/project-memory.md` - 更新已知问题
- [ ] `sprints/decision-log.md` - 记录任何新决策
- [ ] `sprints/sprint-XX/review.md` - Sprint 回顾文档
- [ ] `sprints/backlog.md` - 添加新发现的 Stories
- [ ] `change-log.md` - 记录新 Story 创建

---

## 工作流完成

Phase 9 完成 = 当前 Sprint 完成

**后续步骤:**
- 如果还有下一个 Sprint → 重新 `/nflow-plan`
- 如果所有 Sprint 完成 → 项目完成 ✅
