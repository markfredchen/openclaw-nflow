# NFlow Telegram 通知参考

## 通知脚本

**位置:** `scripts/nflow_notify.py`

## 基本用法

```bash
python3 scripts/nflow_notify.py \
    --node "节点名称" \
    --status success \
    --message "详情信息" \
    --story-id STORY-001 \
    --sprint sprint-01
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--node` | 是 | 节点名称（如 TDD开发、E2E测试） |
| `--status` | 是 | success / failure / warning / pending |
| `--message` | 否 | 详细信息 |
| `--screenshot` | 否 | 截图路径（如有） |
| `--story-id` | 否 | 关联的 Story ID |
| `--sprint` | 否 | Sprint 名称 |
| `--dry-run` | 否 | 仅打印不发送（调试用） |

## 状态说明

| 状态 | Emoji | 用途 |
|------|-------|------|
| success | ✅ | 节点成功完成 |
| failure | ❌ | 节点执行失败 |
| warning | ⚠️ | 节点有警告但继续 |
| pending | ⏳ | 节点等待中 |

## 节点通知示例

### 1. Story 选择完成

```bash
python3 scripts/nflow_notify.py \
    --node "Story选择" \
    --status success \
    --message "已选择 STORY-001: 用户注册功能" \
    --story-id STORY-001 \
    --sprint sprint-01
```

### 2. Git Worktree 创建

```bash
python3 scripts/nflow_notify.py \
    --node "GitWorktree创建" \
    --status success \
    --message "分支 feature/story-001 已创建并切换" \
    --story-id STORY-001
```

### 3. E2E 用例编写完成（含截图）

```bash
python3 scripts/nflow_notify.py \
    --node "E2E用例编写" \
    --status success \
    --message "已完成 5 个测试用例，覆盖登录、注册核心流程" \
    --screenshot "sprints/sprint-01/screenshots/us001-case001-step1.png" \
    --story-id STORY-001
```

### 4. TDD 开发完成

```bash
python3 scripts/nflow_notify.py \
    --node "TDD开发" \
    --status success \
    --message "RED→GREEN→REFACTOR 完成，覆盖率 85%" \
    --screenshot "sprints/sprint-01/coverage-report.png" \
    --story-id STORY-001
```

### 5. 代码审查失败

```bash
# 审查有问题但未达到3次阈值
python3 scripts/nflow_notify.py \
    --node "代码审查" \
    --status warning \
    --message "发现 2 个 🟡 Suggestion，需要修复后重新审查" \
    --screenshot "sprints/sprint-01/reviews/review-001.png" \
    --story-id STORY-001
```

### 6. 审查失败达到3次（人工干预）

```bash
python3 scripts/nflow_notify.py \
    --node "代码审查-人工干预" \
    --status failure \
    --message "⚠️ 审查失败 3 次！需要 Tech Lead 人工介入审查 STORY-001" \
    --story-id STORY-001
```

### 7. 测试执行失败

```bash
python3 scripts/nflow_notify.py \
    --node "测试执行" \
    --status failure \
    --message "测试失败: test_user_registration 失败，请查看截图" \
    --screenshot "sprints/sprint-01/test-reports/failure-001.png" \
    --story-id STORY-001
```

### 8. E2E 测试完成（含报告）

```bash
python3 scripts/nflow_notify.py \
    --node "E2E测试" \
    --status success \
    --message "E2E 测试完成: 10/12 通过，2 个失败（详见报告）" \
    --screenshot "sprints/sprint-01/acceptance-report-001.png" \
    --story-id STORY-001
```

### 9. 代码合并完成

```bash
python3 scripts/nflow_notify.py \
    --node "代码合并" \
    --status success \
    --message "feature/story-001 已合并到 main 分支" \
    --story-id STORY-001
```

### 10. Story 状态更新

```bash
python3 scripts/nflow_notify.py \
    --node "Tracker更新" \
    --status success \
    --message "STORY-001: ⏳ TODO → ✅ DONE" \
    --story-id STORY-001
```

---

## 通知格式预览

发送的通知格式如下：

```
✅ **NFlow 开发节点报告**

**节点:** TDD开发
**状态:** SUCCESS
**时间:** 15:30:45
**Story:** STORY-001
**Sprint:** sprint-01

**详情:**
RED→GREEN→REFACTOR 完成，覆盖率 85%

---
_由 NFlow 自动发送_
```

---

## 完整通知节点一览

### Phase 1: 需求定义 (/nflow-requirements)

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| 市场调研 | ✅ | 可选 | 调研报告预览 |
| PRD 草稿 | ✅ | 可选 | PRD 待审核 |
| PRD 批准 | ✅/⚠️/❌ | 可选 | 审核结果 |
| 架构设计 | ✅ | 可选 | 架构图 |

### Phase 2-3: 设计 (/nflow-design)

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| 设计系统 | ✅ | 是 | design-pattern.json 可视化 |
| 设计系统审核 | ✅/⚠️/❌ | 可选 | 审核反馈 |
| UX 线框图 | ✅ | 是 | 线框图截图 |
| 线框图汇总 | ✅ | 是 | 流程图截图 |

### Phase 4-5: 原型 (/nflow-prototype)

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| Approval Gate | ✅/⚠️/❌ | 可选 | 审核结果 |
| 文档更新 | ✅ | 可选 | 更新内容 |
| UI 原型生成 | ✅ | 是 | HTML 原型截图 |
| 原型审核 | ✅/⚠️/❌ | 是 | 审核反馈 |

### Phase 6-7: 规划 (/nflow-plan)

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| Backlog 生成 | ✅ | 否 | Epic + Stories 列表 |
| Sprint 规划 | ✅ | 否 | Sprint 计划 |

### Phase 8: 开发 (/nflow-dev)

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| Story 选择 | ✅/❌ | 否 | 选择结果 |
| Git Worktree | ✅/❌ | 否 | 创建结果 |
| E2E 用例编写 | ✅/❌ | 是 | 用例截图 |
| TDD 开发 | ✅/❌ | 可选 | 失败截图 |
| 代码审查 | ✅/⚠️/❌ | 可选 | 问题截图 |
| 测试执行 | ✅/❌ | 是 | 失败截图 |
| E2E 测试 | ✅/❌ | 是 | 报告截图 |
| 代码合并 | ✅/❌ | 否 | 合并状态 |
| Tracker 更新 | ✅ | 否 | 状态确认 |
| 人工干预 | ⚠️ | 可选 | 紧急通知 |

### Phase 9: 评审 (/nflow-review)

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| 最终评审 | ✅ | 可选 | 评审结果 |
| 项目完成 | ✅ | 否 | 完成通知 |

---

## 在命令中集成通知

### Python 脚本中调用

```python
import subprocess

def notify(node, status, message, story_id=None, screenshot=None):
    cmd = [
        "python3", "scripts/nflow_notify.py",
        "--node", node,
        "--status", status,
        "--message", message
    ]
    if story_id:
        cmd.extend(["--story-id", story_id])
    if screenshot:
        cmd.extend(["--screenshot", screenshot])
    
    subprocess.run(cmd)

# 使用
notify("TDD开发", "success", "RED→GREEN→REFACTOR 完成", "STORY-001")
```

### Shell 脚本中调用

```bash
#!/bin/bash
python3 scripts/nflow_notify.py \
    --node "节点名称" \
    --status success \
    --message "$message"
```

---

## 调试模式

使用 `--dry-run` 仅打印通知内容，不发送：

```bash
python3 scripts/nflow_notify.py \
    --node "测试" \
    --status success \
    --message "测试消息" \
    --dry-run
```

输出：
```
=== 干运行 - 不发送 ===
✅ **NFlow 开发节点报告**
...
```
