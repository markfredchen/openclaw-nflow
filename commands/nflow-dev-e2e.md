# /nflow-dev-e2e

## E2E 测试流程

**Phase:** Phase 8.4 / 8.9

**执行 Agent:** QA Agent

---

## 通知机制

E2E 每个关键节点完成后发送通知，包含截图：
- E2E 用例编写完成
- E2E 测试执行完成
- 验收报告生成

---

## E2E 测试用例编写

### 步骤

1. **理解 Story 的用户场景**
2. **阅读 wireframes 和 mockups**
3. **编写 E2E 测试用例**
   - 每个步骤需要截图
   - 包含预期结果

### 截图命名规则

```
us{id}-case{id}-step{n}.png

示例：
us001-case001-step1.png   # Story 1, Case 1, Step 1
us001-case001-step2.png   # Story 1, Case 1, Step 2
```

### E2E 用例编写完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "E2E用例编写" \
    --status success \
    --message "已完成 5 个测试用例，覆盖登录、注册核心流程" \
    --screenshot "sprints/sprint-01/screenshots/us001-case001-step1.png" \
    --story-id STORY-001 \
    --sprint sprint-01
```

---

## E2E 测试用例格式

```markdown
### Test Case: TC-{id}

**Story:** {story_id}
**描述:** {描述}

**前置条件:**
- {条件}

**测试步骤:**
1. 打开页面
2. 点击登录按钮
3. 输入用户名密码
4. 点击提交

**预期结果:**
- 显示登录成功提示
- 跳转到首页
```

---

## 执行 E2E 测试

### 步骤

1. **准备测试环境**
   - 启动开发服务器
   - 确保数据库干净

2. **执行测试用例**
   - 按步骤执行
   - 每步截图保存

3. **记录结果**
   - 成功/失败
   - 失败截图
   - 错误日志

### 截图保存

```bash
# 目录结构
sprints/sprint-XX/screenshots/
├── us001-case001-step1.png
├── us001-case001-step2.png
└── ...
```

### E2E 测试执行通知

```bash
# 测试完成（成功）
python3 scripts/nflow_notify.py \
    --node "E2E测试执行" \
    --status success \
    --message "E2E 测试完成：10/12 通过，2 个失败（详见报告）" \
    --screenshot "sprints/sprint-01/screenshots/test-summary.png" \
    --story-id STORY-001 \
    --sprint sprint-01

# 测试失败
python3 scripts/nflow_notify.py \
    --node "E2E测试执行" \
    --status failure \
    --message "E2E 测试失败：登录流程出错，请查看截图" \
    --screenshot "sprints/sprint-01/screenshots/failure-login.png" \
    --story-id STORY-001
```

---

## 生成验收报告 HTML

**使用脚本生成（推荐）：**

1. LLM 返回 JSON 数据
2. 脚本处理模板生成 HTML

**JSON 数据格式：**

```json
{
  "story_id": "STORY-001",
  "story_name": "用户注册",
  "sprint_name": "sprint-01",
  "date": "2026-04-05",
  "passed": 5,
  "failed": 1,
  "total_steps": 12,
  "duration": "15 min",
  "test_cases": [
    {
      "id": "TC-001",
      "description": "用户注册成功",
      "status": "pass",
      "steps": [
        {"step": 1, "action": "打开注册页", "screenshot": "us001-case001-step1.png"},
        {"step": 2, "action": "填写表单", "screenshot": "us001-case001-step2.png"}
      ]
    }
  ]
}
```

**生成命令：**

```bash
python3 scripts/generate_html_report.py \
    --template templates/acceptance-report-template.html \
    --data /tmp/report-data.json \
    --output sprints/sprint-01/acceptance-report-001.html
```

**模板:** `templates/acceptance-report-template.html`

**输出:** `sprints/sprint-XX/acceptance-report-{id}.html`

### 验收报告完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "E2E验收报告" \
    --status success \
    --message "STORY-001 验收报告已生成，请审核" \
    --screenshot "sprints/sprint-01/acceptance-report-001.png" \
    --story-id STORY-001 \
    --sprint sprint-01
```

---

## E2E 测试规则

| 规则 | 说明 |
|------|------|
| 每个 Story 至少一个 E2E 用例 | 覆盖核心功能 |
| 测试必须可重复 | 不依赖手动操作 |
| 失败立即截图 | 保留现场 |
| 清理测试数据 | 不污染环境 |

---

## 输出文件

| 文件 | 路径 |
|------|------|
| E2E 测试用例 | `sprints/sprint-XX/e2e-test-cases/*.spec.ts` |
| 截图 | `sprints/sprint-XX/screenshots/us{id}-*.png` |
| 验收报告 | `sprints/sprint-XX/acceptance-report-{id}.html` |

---

## 相关脚本

- `scripts/nflow_notify.py` - Telegram 通知脚本
- `scripts/generate_html_report.py` - HTML 报告生成
