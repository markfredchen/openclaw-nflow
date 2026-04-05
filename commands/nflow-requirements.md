# /nflow-requirements

## 需求定义（含 Brainstorming）

**Phase:** Phase 1

**执行时机:** 完成 `/nflow-init` 后

**执行 Agent:** Trend Researcher Agent → PM Agent → Architect Agent

---

## 通知机制

需求定义阶段每个节点完成后发送通知：

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| 市场调研 | ✅ | 可选 | 调研报告 |
| 需求提取 | ✅ | 可选 | 从调研提取的需求 |
| Brainstorming | ✅ | 可选 | 澄清问题 |
| 需求确认 | ✅/❌ | 可选 | 用户确认结果 |
| PRD 草稿 | ✅ | 可选 | PRD 待审核 |
| 架构设计 | ✅ | 可选 | 架构图 |

---

## 执行步骤

### Step 1: 市场调研（Trend Researcher Agent）

**输出:** `market-research-report.md`

**调研内容:**
- 市场规模（TAM / SAM / SOM）
- 竞品分析（至少 5 个）
- 用户洞察（画像/痛点/购买驱动）
- 技术趋势
- 政策/监管环境

### 市场调研完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "市场调研" \
    --status success \
    --message "市场调研完成：分析了 5 个竞品，定义了目标用户画像，请审核" \
    --screenshot "docs/market-research-preview.png"
```

---

### Step 2: 需求提取（PM Agent）

**前置:** 市场调研完成

**输入:** `market-research-report.md`

**输出:** `requirements-extracted.md`

**提取内容:**
- 核心用户需求（从竞品分析和用户洞察提取）
- 功能优先级（基于市场机会和用户痛点）
- 关键成功因素

### 需求提取完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "需求提取" \
    --status success \
    --message "从市场调研中提取了 12 个核心需求，按优先级排序，请确认" \
    --screenshot "docs/requirements-extracted-preview.png"
```

---

### Step 3: NFlow Brainstorming（PM Agent）

**前置:** 需求提取完成

**输出:** `brainstorming-record.md`

这是 NFlow 特有的需求澄清流程，融合了 BMad 和 Superpowers 的最佳实践。

#### 3.1 澄清问题（至少 5 个）

**核心原则：一次只问一个问题**

每个问题单独提问，等待用户回答后再提下一个。

**Socratic 提问原则：**
- 一次只问一个问题
- 问题聚焦一个主题
- 问题开放但不模糊
- 探索"为什么"而非"是什么"
- 等用户回答后再问下一个

**问题类型：**

| 类型 | 示例 |
|------|------|
| 目标类 | 这个功能解决用户的什么问题？ |
| 场景类 | 用户在什么情况下会使用这个功能？ |
| 边界类 | 这个功能不适合哪些场景？ |
| 优先级类 | 如果只能实现 3 个功能，是哪 3 个？ |
| 验证类 | 怎么衡量这个功能是否成功？ |

**交互流程：**
```
PM Agent: "Q1: xxx？"
用户回答 → PM Agent: "Q2: xxx？"
用户回答 → PM Agent: "Q3: xxx？"
...
全部回答 → PM Agent: 总结所有回答
```

**输出格式：**
```markdown
## Brainstorming 澄清问题

### Q1: [主题]
**问题:** xxx
**目的:** 澄清 xxx
**回答:** [用户填写]

### Q2: [主题]
**问题:** xxx
**目的:** 澄清 xxx
**回答:** [用户填写]

...
```

#### 3.2 替代方案探索（至少 2 个）

对每个核心需求，探索至少 2 种实现方案：

**格式：**
```markdown
## 替代方案探索

### 需求: [功能名称]

#### 方案 A: [方案名称]
- 优点: xxx
- 缺点: xxx
- 成本: 低/中/高

#### 方案 B: [方案名称]
- 优点: xxx
- 缺点: xxx
- 成本: 低/中/高

**推荐:** 方案 A
**原因:** xxx
```

#### 3.3 用户确认

**必须确认后才能继续：**

1. ✅ 核心需求列表已确认
2. ✅ 替代方案选择已确认
3. ✅ 优先级排序已确认
4. ✅ 排除的需求已确认

### Brainstorming 完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "Brainstorming" \
    --status success \
    --message "Brainstorming 完成：澄清了 8 个问题，探索了 4 个替代方案，请确认" \
    --screenshot "docs/brainstorming-preview.png"
```

---

### Step 4: 需求确认（用户）

**前置:** Brainstorming 完成

**输出:** `requirements-confirmed.md`

**确认清单：**

```
## 需求确认书

### 核心需求（已确认）
1. [需求1] ✅
2. [需求2] ✅
3. [需求3] ✅

### 排除的需求
1. [需求A] - 原因: xxx
2. [需求B] - 原因: xxx

### 确认人: [姓名]
### 确认日期: YYYY-MM-DD
```

**重要：用户签字确认后才能生成 PRD 草稿**

### 需求确认通知

```bash
# 确认通过
python3 scripts/nflow_notify.py \
    --node "需求确认" \
    --status success \
    --message "需求已确认：12 个核心需求，4 个排除需求，可以生成 PRD 草稿" \
    --sprint sprint-01

# 需要修改
python3 scripts/nflow_notify.py \
    --node "需求确认" \
    --status warning \
    --message "需求需要修改：第 3 条优先级需调整，请更新后重新确认" \
    --screenshot "docs/requirements-feedback.png"
```

---

### Step 5: PRD 草稿生成（PM Agent）

**前置:** 需求确认完成

**输入:**
- `market-research-report.md`
- `requirements-extracted.md`
- `brainstorming-record.md`
- `requirements-confirmed.md`

**输出:** `prd.md`

**PRD 内容:**
1. Executive Summary（执行摘要）
2. Goals & Success Metrics（目标和成功指标）
3. User Story Map（用户故事地图）
4. Functional Requirements（功能需求）
5. Non-Functional Requirements（非功能需求）
6. Out of Scope（排除范围）

### PRD 草稿完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "PRD草稿" \
    --status success \
    --message "PRD 草稿完成：包含 8 个 Epic、24 个 User Story，请审核" \
    --screenshot "docs/prd-preview.png" \
    --sprint sprint-01
```

---

### Step 6: PRD 审核（用户）

**审核标准：**
- 需求清晰，无歧义
- User Story 符合 INVEST 原则
- Acceptance Criteria 明确可测
- 优先级合理

**审核结果：**
- ✅ APPROVED — 进入架构设计
- ⚠️ APPROVED_WITH_NOTES — 有建议但可继续
- ❌ REQUEST_CHANGES — 需要修改后重新提交

---

### Step 7: 架构设计（Architect Agent）

**前置:** PRD 审核通过

**输出:** `architecture.md`

**设计内容:**
- 系统架构图
- 技术栈选型
- 数据模型
- API 契约
- 安全架构
- 部署架构

### 架构设计完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "架构设计" \
    --status success \
    --message "架构设计完成：微服务架构，包含用户服务、订单服务、支付服务" \
    --screenshot "docs/architecture-diagram.png" \
    --sprint sprint-01
```

---

## 输出文件

| 文件 | Agent | 状态 |
|------|-------|------|
| `market-research-report.md` | Trend Researcher | ⏳ |
| `requirements-extracted.md` | PM Agent | ⏳ |
| `brainstorming-record.md` | PM Agent | ⏳ |
| `requirements-confirmed.md` | 用户 | ⏳ |
| `prd.md` | PM Agent | ⏳ |
| `architecture.md` | Architect Agent | ⏳ |

---

## 流程图

```
市场调研 (Trend Researcher)
        ↓
需求提取 (PM Agent)
        ↓
NFlow Brainstorming (PM Agent)
    ├── 澄清问题（≥5个）
    ├── 替代方案探索（≥2个）
    └── 用户确认 ✅
        ↓
PRD 草稿 (PM Agent)
        ↓
PRD 审核（用户）
        ↓
架构设计 (Architect Agent)
```

---

## 审核要求

Phase 1 的输出将在 `/nflow-design` 阶段的 Approval Gate 中统一审核。

---

## 下一步

```
/nflow-design
```

---

## 相关脚本

- `scripts/nflow_notify.py` - Telegram 通知脚本
