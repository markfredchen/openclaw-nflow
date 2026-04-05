# /nflow-requirements

## 需求定义

**Phase:** Phase 1

**执行时机:** 完成 `/nflow-init` 后

**执行 Agent:** Trend Researcher Agent → PM Agent → Architect Agent

---

## 通知机制

需求定义阶段每个节点完成后发送通知：

| 节点 | 状态 | 截图 | 说明 |
|------|------|------|------|
| 市场调研 | ✅ | 可选 | 调研报告 |
| PRD 草稿 | ✅ | 可选 | PRD 待审核 |
| PRD 批准 | ✅/❌ | 可选 | 审核结果 |
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
    --screenshot "docs/market-research-preview.png" \
    --sprint sprint-01
```

---

### Step 2: 需求文档（PM Agent）

**前置:** 市场调研完成

**输出:** `prd.md`

**强制 brainstorming（Socratic 方法）:**
1. 提出至少 5 个澄清问题
2. 探索至少 2 种替代方案
3. 展示设计给用户确认
4. **用户批准后才能继续**

**PRD 内容:**
- Executive Summary
- Goals & Success Metrics
- User Story Map
- Functional Requirements
- Non-Functional Requirements
- Out of Scope

### PRD 草稿完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "PRD草稿" \
    --status success \
    --message "PRD 草稿完成，包含 8 个 Epic、24 个 User Story，请确认需求范围" \
    --screenshot "docs/prd-preview.png" \
    --sprint sprint-01
```

### PRD 批准通知

```bash
# PRD 批准
python3 scripts/nflow_notify.py \
    --node "PRD批准" \
    --status success \
    --message "PRD 已批准：所有澄清问题已解答，需求范围已确认，可以进入架构设计阶段" \
    --sprint sprint-01

# PRD 需要修改
python3 scripts/nflow_notify.py \
    --node "PRD审核" \
    --status warning \
    --message "PRD 需要修改：用户注册流程需要补充第三方登录场景，请更新后重新提交" \
    --screenshot "docs/prd-feedback.png" \
    --sprint sprint-01
```

---

### Step 3: 架构设计（Architect Agent）

**前置:** PRD 批准

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
    --message "架构设计完成：微服务架构，包含用户服务、订单服务、支付服务，技术栈已确定" \
    --screenshot "docs/architecture-diagram.png" \
    --sprint sprint-01
```

---

## 输出文件

| 文件 | Agent | 状态 |
|------|-------|------|
| `market-research-report.md` | Trend Researcher | ⏳ |
| `prd.md` | PM Agent | ⏳ |
| `architecture.md` | Architect Agent | ⏳ |

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
