# /nflow-dev

## 开发循环

**Phase:** Phase 8

**执行时机:** 完成 `/nflow-plan` 后

**执行 Agent:** Git Workflow Master / Developer / QA Agent / Code Reviewer

**循环执行:** 直到 Sprint 计划中的所有 User Stories 全部完成。

---

## 通知机制

每个节点完成后自动发送 Telegram 通知给老大，包含：
- 节点执行状态（成功/失败）
- 任务详情
- 截图（如有）

**详细说明:** 参考 `references/notifications.md`

---

## 执行概览

```
1. 确定 Sprint（Hotfix 优先）
       ↓
2. 选择下一个 Story
       ↓
3. 创建 Git Worktree
       ↓
4. TDD 开发 + E2E 用例编写（并行）
       ↓
5. 代码审查
       ↓
6. 执行测试
       ↓
7. E2E 测试 + 生成报告
       ↓
8. 代码合并
       ↓
9. 更新 Tracker
       ↓
   循环直到所有 Stories 完成
```

---

## 确定执行哪个 Sprint

**使用脚本（推荐）：**

```bash
python3 scripts/nflow_tools.py scan-sprints --include-hotfix
```

**优先级：**
| 优先级 | 情况 | 选择 |
|--------|------|------|
| P0 | 有 Hotfix Sprint | Hotfix Sprint |
| P1 | 最新有未完成的 Sprint | Sprint 02 > Sprint 01 |

---

## 选择下一个 Story

从 `user-stories-tracker.md` 中选择状态为 `⏳ TODO` 的 Story，按：
1. 优先级（P0 > P1 > P2）
2. 依赖关系（被依赖的先做）

**选择完成后发送通知：**
```bash
python3 scripts/nflow_notify.py \
    --node "Story选择" \
    --status success \
    --message "已选择 STORY-001: xxx功能" \
    --story-id STORY-001 \
    --sprint sprint-01
```

---

## 子流程详情

### TDD 开发

详见 `nflow-dev-tdd.md`

**节点完成通知示例：**
```bash
python3 scripts/nflow_notify.py \
    --node "TDD开发" \
    --status success \
    --message "RED→GREEN→REFACTOR 完成，覆盖率 85%" \
    --screenshot "sprints/sprint-01/coverage-report.png" \
    --story-id STORY-001 \
    --sprint sprint-01
```

### E2E 测试

详见 `nflow-dev-e2e.md`

**节点完成通知示例：**
```bash
python3 scripts/nflow_notify.py \
    --node "E2E用例编写" \
    --status success \
    --message "已完成 5 个测试用例，覆盖核心流程" \
    --screenshot "sprints/sprint-01/screenshots/us001-case001-step1.png" \
    --story-id STORY-001 \
    --sprint sprint-01
```

### 代码审查

详见 `nflow-dev-review.md`

**节点完成通知示例：**
```bash
# 审查通过
python3 scripts/nflow_notify.py \
    --node "代码审查" \
    --status success \
    --message "审查通过，0 个 Blocker" \
    --story-id STORY-001

# 审查有问题
python3 scripts/nflow_notify.py \
    --node "代码审查" \
    --status warning \
    --message "发现 2 个 🟡 Suggestion，请修复" \
    --screenshot "sprints/sprint-01/reviews/review-001.png" \
    --story-id STORY-001

# 审查失败达到3次（人工干预）
python3 scripts/nflow_notify.py \
    --node "代码审查-人工干预" \
    --status failure \
    --message "⚠️ 审查失败 3 次！需要 Tech Lead 人工介入" \
    --story-id STORY-001
```

---

## 循环终止条件

当所有 Stories 状态都是 `✅ DONE` 时，`/nflow-dev` 完成。

**最终通知：**
```bash
python3 scripts/nflow_notify.py \
    --node "Sprint完成" \
    --status success \
    --message "Sprint-01 所有 Stories 已完成！可以执行 /nflow-review 进行最终评审。" \
    --sprint sprint-01
```

---

## 下一步

```
/nflow-review
```

---

## 相关命令

| 命令 | 说明 |
|------|------|
| `/nflow-resume` | 恢复中断的开发循环 |
| `/nflow-story` | 执行单个 Story |
| `scripts/nflow_notify.py` | Telegram 通知脚本 |
| `references/notifications.md` | 通知使用参考 |
