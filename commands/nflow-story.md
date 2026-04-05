# /nflow-story

## 实现单个 User Story

**Phase:** Phase 8（单 Story 执行）

**执行时机:** 执行 `/nflow-dev` 过程中，或者单独实现某个 Story

**执行 Agent:** 对应 Developer Agent

---

## 执行步骤

### 1. 选择 Story

从 `user-stories-tracker.md` 的 TODO Stories 中选择一个。

### 2. 收集需求

**必须收集:**
1. Story Acceptance Criteria（来自 `stories.md`）
2. API 契约（来自 `architecture.md`）
3. 数据模型（来自 `architecture.md`）
4. Wireframe（来自 `wireframes/*.md`）
5. 设计规范（来自 `design-pattern.json`）

### 3. 创建实现计划

**输出:** `story-implementation-plan-{id}.md`

```markdown
# Story 实现计划: STORY-001

## 需求收集
- **Story:** 用户注册
- **Acceptance Criteria:** [列表]
- **API:** POST /api/auth/register
- **Wireframe:** wireframes/page-001-login.md

## 任务拆分
| 任务 | 类型 | 预估时间 |
|------|------|----------|
| 创建数据库迁移 | DB | 1h |
| 实现 send-code API | Backend | 2h |
| 实现 register API | Backend | 3h |
| 编写单元测试 | Test | 2h |
| 前端注册表单 | Frontend | 3h |
| E2E 测试 | Test | 2h |
```

### 4. TDD 开发循环

```
RED（写测试）→ GREEN（写实现）→ REFACTOR（重构）
```

### 5. 代码审查

**输出:** Review 反馈

| 结果 | 含义 | 动作 |
|------|------|------|
| ✅ APPROVED | 通过 | 继续 |
| 🔴 REQUEST_CHANGES | 需要修改 | 修复后重新审查 |

### 6. 执行测试

- 单元测试
- 集成测试
- E2E 测试（如需要）

### 7. 代码合并

**Git Workflow Master Agent 执行:**
```bash
git checkout main
git merge --no-ff feat/story-{id}
git branch -d feat/story-{id}
git worktree remove ../worktrees/story-{id}
```

### 8. 更新 Tracker

在 `user-stories-tracker.md` 中更新 Story 状态为 `✅ DONE`。

---

## 输出文件

| 文件 | Agent |
|------|-------|
| `story-implementation-plan-{id}.md` | Developer |
| `test-report-{id}.md` | QA Agent |

---

## 下一步

完成当前 Story 后：
- 返回 `/nflow-dev` 继续下一个 Story
- 或使用 `/nflow-story` 继续实现
