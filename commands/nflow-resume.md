# /nflow-resume

## 恢复执行

**执行时机:** `/nflow-dev` 执行中断后

---

## 确定执行哪个 Sprint

**规则：** 只执行**最新一个有未完成 Stories 的 Sprint**

```
1. 读取 sprints/user-stories-tracker.md

2. 检查所有 Sprint 状态：
   
   Sprint 01: ✅ DONE (所有 Stories 完成)
   Sprint 02: 🔄 3/5 Stories 完成
   Sprint 03: ⏳ 0/4 Stories 开始
   
   → 恢复 Sprint 02（最新一个有未完成的）

3. 如果所有 Sprint 都完成 → 无需恢复

4. 如果没有可用 Sprint → 提示执行 /nflow-plan
```

---

## 执行步骤

### 1. 检查 Sprint 状态

读取 `sprints/user-stories-tracker.md`，查看所有 Stories 的状态：

```markdown
| Story ID | 名称 | 状态 |
|----------|------|------|
| STORY-001 | 用户注册 | ✅ DONE |
| STORY-002 | 用户登录 | 🔄 IN_PROGRESS |
| STORY-003 | 用户登出 | ⏳ TODO |
```

### 2. 根据状态判断恢复点

| 状态 | 含义 | 恢复动作 |
|------|------|----------|
| ✅ DONE | 已完成 | 跳过，选择下一个 TODO Story |
| 🔄 IN_PROGRESS | 开发中 | 检查 worktree，继续开发 |
| 🔍 CODE_REVIEW | 审查中 | 获取审查反馈，继续审查 |
| 🧪 TESTING | 测试中 | 继续测试 |
| ⏳ TODO | 未开始 | 正常开始 |

### 3. 检查 Git Worktree 状态

```bash
# 查看所有 worktrees
git worktree list

# 示例输出：
# /path/main         (bare repository, main)
# /path/worktrees/story-002-user-login HEAD detached at feat/story-002

# 查看分支状态
git branch -a

# 如果有 IN_PROGRESS 的 worktree，进入检查
cd ../worktrees/story-002-user-login
git status
git log --oneline -3
```

### 4. 恢复执行

**如果 Story 状态是 🔄 IN_PROGRESS：**
```
1. 检查 worktree 是否存在
2. 进入 worktree 检查代码状态
3. 查看是否有未提交的更改
4. 根据情况继续：
   - 有未完成代码 → 继续 TDD 开发
   - 代码完成待审查 → 执行 Code Review
   - 审查反馈待修复 → 修复问题
```

**如果 Story 状态是 🔍 CODE_REVIEW：**
```
1. 确认是否有审查反馈
2. 检查测试失败次数（在 tracker 中）
3. 如果测试失败次数 ≥ 3 → 🤖 人工干预！
4. 否则 → 修复 🔴 Blocker
5. 重新提交审查
```

**3 次规则：** 测试失败 3 次后，必须人工干预。

**如果 Story 状态是 🧪 TESTING：**
```
1. 继续执行测试
2. 查看测试报告
3. 如果失败 → 回退到代码编写修复
4. 重新测试
```
**注意：** 测试失败需要回到 TDD 代码编写阶段修复，不只是修复测试。

### 5. 清理无效 Worktree

如果 worktree 存在但 Story 已完成或状态异常：

```bash
# 删除已完成的 worktree
git worktree remove ../worktrees/story-{id}-{name}

# 删除孤立分支
git branch -D feat/story-{id}
```

---

## 恢复检查清单

```
□ 读取 user-stories-tracker.md
□ 识别中断的 Story
□ 检查 Git worktree 状态
□ 判断恢复点
□ 继续执行中断的步骤
□ 更新 tracker（如有状态变化）
```

---

## 示例场景

### 场景 1：会话中断，Story 还在开发中

**状态：** STORY-002 状态为 🔄 IN_PROGRESS

**恢复：**
```
1. git worktree list → 确认 worktree 存在
2. cd worktrees/story-002-user-login
3. git status → 有未提交代码
4. 继续开发 → 完成代码
5. 提交 → 执行 Code Review
```

### 场景 2：Code Review 被要求修改

**状态：** STORY-002 状态为 🔍 CODE_REVIEW，有 🔴 Blocker

**恢复：**
```
1. 查看审查反馈
2. 修复 Blockers
3. 提交代码
4. 重新发起 Code Review
```

### 场景 3：Story 完全未开始

**状态：** STORY-003 状态为 ⏳ TODO

**恢复：**
```
1. 正常开始 STORY-003
2. 执行完整流程：8.3 → 8.4 → 8.5 → ...
```

---

## 继续开发循环

恢复后，继续 `/nflow-dev` 的循环执行，直到所有 Stories 完成。

---

## 下一步

当所有 Stories 完成：

```
/nflow-review
```
