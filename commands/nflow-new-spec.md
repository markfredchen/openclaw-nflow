# /nflow-new-spec

## 新需求 / Bug 录入

**用途：** Sprint 开发完成后，发现 bug 或有新需求时使用

**触发方式：** `/nflow-new-spec "新需求描述"` 或 `/nflow-new-spec "bug 描述"`

---

## 执行步骤

### 1. 需求录入

**执行 Agent:** PM Agent

**询问用户：**
- 需求/问题描述是什么？
- 发现场景/复现步骤（如是 bug）
- 优先级建议（P0/P1/P2）
- 影响范围（影响哪些功能/用户）

**创建变更请求文档：**

**输出:** `change-request-{timestamp}.md`

```markdown
# Change Request: {需求名称}

**日期:** YYYY-MM-DD
**类型:** NEW_REQUIREMENT / BUG_FIX / IMPROVEMENT
**状态:** 📝 DRAFT

## 描述
{用户描述的需求内容}

## 发现场景（Bug 必填）
{Bug 复现步骤}

## 初步评估
- **优先级建议:** P0 / P1 / P2
- **影响范围:** {功能/用户}
- **紧迫程度:** 🔴 高 / 🟡 中 / 🟢 低

## 评估结果
- **评估人:**
- **评估日期:**
```

---

### 2. 影响评估

**执行 Agent:** PM Agent + Architect Agent

**评估范围：**

| 文档 | 评估内容 |
|------|----------|
| `prd.md` | 是否需要修改功能描述？是否影响现有需求？ |
| `architecture.md` | 是否需要修改数据模型/API/架构？ |
| `mockups/*.html` | 是否需要新增/修改页面？ |
| `stories.md` | 是否需要新增/修改 Story？ |
| `epics.md` | 属于哪个 Epic？是否需要新建 Epic？ |

**评估输出:**

```markdown
## 评估结果

### PRD 影响
- [ ] 需要修改
- [ ] 不需要修改
- **说明:** {如果需要，说明修改什么}

### Architecture 影响
- [ ] 需要修改
- [ ] 不需要修改
- **说明:** {如果需要，说明修改什么}

### Mockup 影响
- [ ] 需要新增页面
- [ ] 需要修改现有页面
- [ ] 不需要修改
- **说明:** {如果需要，说明修改什么}

### Epic 归属
- [ ] 归属现有 Epic: EPIC-XX
- [ ] 新建 Epic: EPIC-XX
- **说明:**
```

---

### 3. 变更决策

**决策人:** 项目负责人 / 产品 Owner

**决策选项：**

| 决策 | 含义 | 后续动作 |
|------|------|----------|
| ✅ **APPROVED** | 接受变更 | 进入下一步 |
| ❌ **REJECTED** | 拒绝变更 | 结束，记录原因 |
| ⏳ **DEFERRED** | 推迟到下个 Sprint | 记录到 backlog-remaining |

---

### 4. 更新文档

**执行 Agent:** PM Agent + Architect Agent

**如果 APPROVED：**

#### 4.1 更新 PRD（如需要）
在 `prd.md` 中添加/修改相关内容。

#### 4.2 更新 Architecture（如需要）
在 `architecture.md` 中添加/修改相关内容。

#### 4.3 更新 Mockups（如需要）
在 `mockups/` 中新增/修改 HTML 页面。

#### 4.4 创建/更新 Epic（如需要）
在 `epics.md` 中新增 Epic 或更新现有 Epic。

#### 4.5 创建 User Story
在 `stories.md` 中添加新 Story，关联到对应 Epic：

```markdown
### STORY-XXN: {Story 名称}

**Epic:** EPIC-XX
**优先级:** P0 / P1 / P2
**故事点:** {估算}

**AS A** {用户角色}
**I WANT** {功能描述}
**SO THAT** {价值}

**Acceptance Criteria:**
- [ ] {标准1}
- [ ] {标准2}

**依赖:** STORY-XXX（如果需要）
**相关 API:** /api/v1/...（如果需要）
```

#### 4.6 更新 Change Log
在 `change-log.md` 中记录：

```markdown
| ID | 日期 | 类型 | 描述 | 影响评估 | 决策 | Epic/Story |
|----|------|------|------|----------|------|-------------|
| CR-001 | YYYY-MM-DD | NEW_REQUIREMENT | {描述} | 需新增1个Story | APPROVED | EPIC-01/STORY-XXN |
```

---

### 5. 决定处理方式

| 情况 | 处理方式 |
|------|----------|
| 当前 Sprint 紧急 bug | 立即修复，合并到当前 Sprint |
| 当前 Sprint 非紧急需求 | 推入 backlog-remaining，下个 Sprint 处理 |
| 下个 Sprint 需求 | 记录到 backlog-remaining |

---

## 输出文件

| 文件 | Agent | 状态 |
|------|-------|------|
| `change-request-{timestamp}.md` | PM Agent | ⏳ |
| `prd.md`（更新）| PM Agent | ⏳ |
| `architecture.md`（更新）| Architect Agent | ⏳ |
| `mockups/*.html`（更新）| UI Designer Agent | ⏳ |
| `epics.md`（更新）| PM + Architect | ⏳ |
| `stories.md`（更新）| PM + Architect | ⏳ |
| `change-log.md`（更新）| PM Agent | ⏳ |

---

## 下一步

| 情况 | 后续命令 |
|------|----------|
| 紧急 Bug | 继续 `/nflow-dev` 修复 |
| 新需求（当前 Sprint）| 继续 `/nflow-dev` 实现 |
| 非紧急需求 | 等待下个 Sprint `/nflow-plan` |

---

## 示例场景

### 场景 1：发现 Bug

```
/nflow-new-spec "用户无法登录，密码正确但返回401"
```

评估：
- PRD：不需要修改
- Architecture：不需要修改
- Mockups：不需要修改
- Story：新建 STORY-999 "修复用户登录 bug"
- 决策：APPROVED
- 处理：立即修复，加入当前 Sprint

### 场景 2：新需求

```
/nflow-new-spec "需要新增微信登录功能"
```

评估：
- PRD：需要添加微信登录功能描述
- Architecture：需要添加微信 OAuth API
- Mockups：需要新增微信登录入口页面
- Epic：新建 EPIC-05 "第三方登录"
- Story：新建 STORY-101 "微信登录"
- 决策：DEFERRED（推到下个 Sprint）
