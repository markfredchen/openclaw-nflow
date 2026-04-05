# /nflow-prototype

## 原型图生成 + 人工审核

**Phase:** Phase 4-5

**执行时机:** 完成 `/nflow-design` 后

**执行 Agent:** UI Designer Agent → 用户（审核）

---

## 通知机制

原型阶段每个节点完成后发送通知，包含原型截图：

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| Approval Gate 审核 | ✅/❌ | 可选 | 审核结果 |
| UI 原型生成 | ✅ | 是 | HTML 原型截图 |
| 原型审核 | ✅/❌ | 是 | 审核反馈 |

---

## Phase 4: 人工审核（Approval Gate）

### Step 1: 审核文档

**审核人:** 产品 Owner / 项目负责人 / 技术负责人

**审核范围:**

| 文档 | 审核内容 |
|------|----------|
| `market-research-report.md` | 市场分析准确性 |
| `prd.md` | 需求清晰度、User Story 完整性 |
| `architecture.md` | 架构合理性、技术选型可行性 |
| `design-pattern.json` | 设计规范完整性 |
| `wireframes/*.md` | 页面覆盖、交互说明 |

### Step 2: 标注问题

- ✅ APPROVED — 审核通过
- ⚠️ APPROVED_WITH_NOTES — 有建议但不阻塞
- ❌ REQUEST_CHANGES — 需要修改

### Approval Gate 审核结果通知

```bash
# 审核通过
python3 scripts/nflow_notify.py \
    --node "ApprovalGate审核" \
    --status success \
    --message "审核通过：所有文档符合要求，可以进入 UI 原型阶段" \
    --sprint sprint-01

# 审核有问题但不阻塞
python3 scripts/nflow_notify.py \
    --node "ApprovalGate审核" \
    --status warning \
    --message "审核通过但有建议：建议补充性能指标定义，请确认" \
    --screenshot "docs/review-notes.png" \
    --sprint sprint-01

# 需要修改
python3 scripts/nflow_notify.py \
    --node "ApprovalGate审核" \
    --status failure \
    --message "审核不通过：prd.md 中用户注册流程描述不清，请补充后重新提交" \
    --screenshot "docs/review-feedback.png" \
    --sprint sprint-01
```

### Step 3: 更新文档

如有 REQUEST_CHANGES，更新对应文档后重新提交审核。

**重新提交审核通知：**

```bash
python3 scripts/nflow_notify.py \
    --node "文档更新" \
    --status success \
    --message "已根据审核反馈更新 prd.md，重新提交审核" \
    --screenshot "docs/prd-updated.png" \
    --sprint sprint-01
```

---

## Phase 5: UI 原型图

### Step 4: 生成 HTML 原型（UI Designer Agent）

**前置:** Approval Gate 通过

**输出:** `mockups/*.html`

**每个页面一个 HTML 文件：**

```html
<!-- mockups/page-001-login.html -->
<!DOCTYPE html>
<html>
<head>
    <!-- 使用 design-pattern.json 中的 CSS 变量 -->
    <style>
        :root {
            --color-primary: #1890FF;
            --spacing-lg: 16px;
        }
    </style>
</head>
<body>
    <!-- 登录表单 -->
    <form id="loginForm">
        <input type="tel" placeholder="手机号">
        <input type="password" placeholder="密码">
        <button type="submit">登录</button>
    </form>
    
    <!-- Confirm Modal -->
    <div id="confirmModal" class="modal">
        <h3>确认登录</h3>
        <p>确定要登录吗？</p>
        <button onclick="closeModal()">取消</button>
        <button onclick="confirmLogin()">确定</button>
    </div>
</body>
</html>
```

**交互要求:**
- 点击按钮 → Confirm Modal 弹出
- 表单提交 → Loading → 结果反馈
- 响应式适配（Mobile / Tablet / Desktop）

### UI 原型生成完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "UI原型生成" \
    --status success \
    --message "已完成 12 个页面的 HTML 原型，包含登录、注册、首页等核心流程" \
    --screenshot "mockups/preview-login.png" \
    --sprint sprint-01
```

---

### Step 5: 审核原型图

**审核人:** 产品 Owner

**检查项:**
- 功能完整性
- 交互正确性
- 设计一致性（遵守 design-pattern.json）
- 响应式适配
- 状态覆盖（空状态/加载/错误）

### 原型审核结果通知

```bash
# 审核通过
python3 scripts/nflow_notify.py \
    --node "原型审核" \
    --status success \
    --message "原型审核通过：所有页面交互正确，设计一致，请确认后进入开发阶段" \
    --screenshot "mockups/final-preview.png" \
    --sprint sprint-01

# 审核有问题
python3 scripts/nflow_notify.py \
    --node "原型审核" \
    --status warning \
    --message "原型需要修改：登录页缺少忘记密码入口，请补充" \
    --screenshot "mockups/review-feedback.png" \
    --sprint sprint-01

# 审核不通过
python3 scripts/nflow_notify.py \
    --node "原型审核" \
    --status failure \
    --message "原型审核不通过：注册流程交互不符合预期，请重新设计" \
    --screenshot "mockups/review-issue.png" \
    --sprint sprint-01
```

---

## 输出文件

| 文件 | Agent | 状态 |
|------|-------|------|
| `approval-record.md` | 审核人 | ⏳ |
| `mockups/page-001-*.html` | UI Designer | ⏳ |
| `mockups/README.md` | UI Designer | ⏳ |

---

## 下一步

```
/nflow-plan
```

---

## 相关脚本

- `scripts/nflow_notify.py` - Telegram 通知脚本
