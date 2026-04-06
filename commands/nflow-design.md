# /nflow-design

## 设计系统 + 线框图

**Phase:** Phase 2-3

**执行时机:** `/nflow-requirements` 的 Step 7（架构设计）审核通过后

**执行 Agent:** UI Designer Agent → UX Designer Agent

---

## 前置检查

**⚠️ 必须满足以下条件才能执行此命令：**

| 检查项 | 说明 | 未满足时的错误信息 |
|--------|------|--------------------|
| project-state.json 存在 | 项目状态文件 | ❌ 错误：项目未初始化，请先执行 /nflow-init |
| current_step == "architecture_approved" | 架构设计已审核通过 | ❌ 错误：Phase 1 架构设计未完成，请先完成 /nflow-requirements |
| architecture.md 存在 | 架构文档已生成 | ❌ 错误：架构文档不存在 |

---

## 执行前检查脚本

```bash
# 检查是否满足执行条件
python3 scripts/nflow_tools.py check-prerequisites --step design
```

**检查逻辑：**
```python
def check_prerequisites(step: str):
    state = load_project_state()
    
    if step == "design":
        if state.get("current_step") != "architecture_approved":
            raise WorkflowError(
                "Phase 1 架构设计未完成。"
                "请先完成 /nflow-requirements 中的 Step 7（架构设计）"
            )
        if not Path("architecture.md").exists():
            raise WorkflowError(
                "架构文档不存在。"
                "请先执行 /nflow-requirements 生成 architecture.md"
            )
```

---

## 通知机制

设计阶段每个节点完成后发送通知，包含设计稿截图（如有）：

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| 设计系统 | ✅ | 是 | design-pattern.json 可视化 |
| 线框图 | ✅ | 是 | ASCII 线框图截图 |
| 审核结果 | ✅/❌ | 可选 | 审核反馈 |

---

## Phase 2: 设计系统

### Step 1: 设计系统定义（UI Designer Agent）

**前置:** `prd.md` + `architecture.md`

**输出:** `design-pattern.json`

**设计内容:**
1. **视觉风格** — 整体定位/配色/字体/间距
2. **组件规范** — 按钮/输入框/卡片/导航
3. **平台适配** — iOS HIG / Android Material / Web 响应式

### 设计系统完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "设计系统" \
    --status success \
    --message "设计系统已完成，包含：配色方案、字体规范、组件库定义" \
    --screenshot "docs/design-pattern-preview.png" \
    --sprint sprint-01
```

---

### Step 2: 人工确认设计系统

**决策人:** 产品 Owner / 用户

审核设计系统定义，确认后继续。

**审核结果通知：**

```bash
# 审核通过
python3 scripts/nflow_notify.py \
    --node "设计系统审核" \
    --status success \
    --message "设计系统审核通过，已确认配色方案和组件规范" \
    --screenshot "docs/design-pattern-final.png"

# 审核有问题
python3 scripts/nflow_notify.py \
    --node "设计系统审核" \
    --status warning \
    --message "设计系统需要修改：主色调调整为 #2B4CBA，请重新提交" \
    --screenshot "docs/design-pattern-annotated.png"
```

---

## Phase 3: UX 线框图

### Step 3: 线框图设计（UX Designer Agent）

**前置:** `design-pattern.json` 已确认

**输出:** `wireframes/*.md`

**每个页面一个文件，ASCII 线框图：**

```markdown
# 页面线框图: 登录页

## 页面结构
┌─────────────────────────────┐
│  ← 返回    [登录]           │
├─────────────────────────────┤
│                             │
│       [Logo]               │
│                             │
│  ┌───────────────────────┐  │
│  │ 手机号              │  │
│  └───────────────────────┘  │
│                             │
│  ┌───────────────────────┐  │
│  │ 密码                │  │
│  └───────────────────────┘  │
│                             │
│  [       登录       ]      │
│                             │
│  忘记密码？注册           │
└─────────────────────────────┘

## 交互说明
| 元素 | 交互 | 行为 |
|------|------|------|
| 登录按钮 | 点击 | 调用 /api/auth/login |
```

### 线框图完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "UX线框图" \
    --status success \
    --message "已完成 12 个页面的线框图设计，覆盖登录、注册、首页等核心流程" \
    --screenshot "wireframes/wireframes-preview.png" \
    --sprint sprint-01
```

---

### Step 4: 汇总到 wireframes/README.md

页面索引 + 用户流程图

**汇总完成通知：**

```bash
python3 scripts/nflow_notify.py \
    --node "线框图汇总" \
    --status success \
    --message "线框图索引和用户流程图已生成，请审核" \
    --screenshot "wireframes/flow-diagram.png" \
    --sprint sprint-01
```

---

## 审核要求

Phase 2-3 的输出将在 `/nflow-prototype` 阶段的 Approval Gate 中统一审核。

---

## 下一步

```
/nflow-prototype
```

---

## 相关脚本

- `scripts/nflow_notify.py` - Telegram 通知脚本
