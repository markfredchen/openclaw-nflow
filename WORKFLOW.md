# NFlow: 自定义开发工作流

**版本：** v0.1
**融合：** BMad Method + Superpowers
**日期：** 2026-04-05

---

## 核心理念

**AI 是协作者，不是替代者。结构化流程带出最佳思考。**

---

## 双轨制复杂度适配

| 复杂度 | 判断标准 | 流程 |
|--------|----------|------|
| **L1: 快速修复** | Bug fix、明确小改动（1-3 stories） | Quick Flow |
| **L2: 标准功能** | 单一模块功能开发（4-15 stories） | Standard Flow |
| **L3: 复杂项目** | 多模块/跨团队（16-50 stories） | Full Flow |
| **L4: 平台/企业** | 架构决策、安全合规（50+ stories） | Enterprise Flow |

**复杂度由 Lead Agent 在项目启动时判定，可动态调整。**

---

## 阶段总览

```
L1 Quick Flow:    SPEC → IMPLEMENT → REVIEW
L2 Standard Flow: BRIEF → SPEC → PLAN → IMPLEMENT → REVIEW
L3 Full Flow:     RESEARCH → PRD → ARCHITECTURE → **DESIGN SYSTEM** → **UX DESIGN** → **APPROVAL GATE** → **UI PROTOTYPE** → **BACKLOG** → **SPRINT** → **IMPLEMENT** → **REVIEW**
L4 Enterprise:    ↑ + SECURITY-REVIEW + COMPLIANCE + DEVOPS
```

---

## L2+ 标准流程详解

---

### Phase 0: 项目初始化（仅 L3+）

**执行 Agent:** Lead Agent

**动作:**
1. 确定项目范围和复杂度等级
2. 创建项目目录结构
3. 初始化 `project-config.md`
4. 分配 Agent 团队角色

**输出:** `project-config.md`

---

### Phase 1: 需求定义（仅 L3+）

**目的:** 在写代码之前，先把需求和架构想清楚。

**三步流程：**

```
Step 1: Trend Researcher → market-research-report.md
     ↓
Step 2: Product Manager → prd.md
     ↓
Step 3: Software Architect → architecture.md
```

---

#### Step 1.1: 市场调研（Trend Researcher）

**执行 Agent:** Trend Researcher Agent

**目的:** 看清战场，了解市场机会和竞争格局。

**调研内容:**
- 市场规模（ TAM / SAM / SOM ）
- 竞品分析（功能/定价/定位/用户评价）
- 用户洞察（画像/痛点/购买决策因素）
- 技术趋势
- 政策/监管环境

**输出:** `market-research-report.md`

---

#### Step 1.2: 需求文档（Product Manager）

**执行 Agent:** PM Agent

**目的:** 将市场机会转化为可执行的产品需求。

**强制 brainstorming（Superpowers Socratic 方法）:**
1. PM Agent 提出至少 5 个澄清问题
2. 探索至少 2 种替代方案
3. 展示设计分段给用户确认
4. **用户明确批准后才能进入下一步**

**输出:** `prd.md`

---

#### Step 1.3: 架构设计（Software Architect）

**执行 Agent:** Architect Agent

**目的:** 将需求转化为可实施的技术方案。

**设计内容:**
- 系统架构图
- 技术栈选型
- 数据模型设计
- API 契约
- 安全架构
- 部署架构

**输出:** `architecture.md`

---

### Phase 2: DESIGN SYSTEM（设计系统）

**执行 Agent:** UI Designer Agent

**前置输入:** `prd.md` + `architecture.md`

**目的:** 在设计具体页面之前，先定义视觉语言和设计规范。

**执行步骤:**

```
Step 1: 风格定义
   - 确定整体视觉风格
   - 确定配色方案
   - 确定字体系统
   - 确定间距/布局规范

Step 2: 设计系统组件
   - 定义基础组件规范（按钮/输入框/卡片...）
   - 定义复合组件（列表项/导航/表单...）
   - 定义状态样式（normal/hover/active/disabled/error）

Step 3: 平台适配
   - Web 响应式断点
   - iOS HIG 适配
   - Android Material Design 适配

Step 4: 人工确认风格
   - 展示风格定义
   - 收集反馈
   - 调整规范

Step 5: 输出 design-pattern.json
   - 将所有设计规范结构化输出
   - JSON 格式，可被程序化读取
```

**输出:** `design-pattern.json`

**性质:** 强制规范。所有后续 UI 页面生成必须遵守。

---

### Phase 3: UX DESIGN（线框图设计）

**执行 Agent:** UX Designer Agent

**前置输入:** `prd.md` + `architecture.md` + **`design-pattern.json`**

**目的:** 将需求文档转化为可执行的界面线框图，每个页面单独一个 md 文件。

**重要:** 所有设计必须严格遵守 `design-pattern.json` 中的规范。

**输出目录:** `wireframes/`

**文件结构:**
```
wireframes/
├── README.md              # 页面索引 + 流程图
├── page-001-login.md     # 登录页
├── page-002-home.md      # 首页
└── ...
```

**执行步骤:**
1. 根据 `prd.md` 中的 User Story Map 提取所有页面
2. 为每个页面创建 ASCII 线框图（遵守 design-pattern.json）
3. 定义交互说明（点击 → API 调用）
4. 标注状态处理（空状态 / 加载状态 / 错误状态）
5. 设计响应式断点（Mobile / Tablet / Desktop）
6. 汇总到 `wireframes/README.md`

**ASCII 线框图规范:**
- 容器：┌ ─ ┐ │ └ ┘
- 按钮：[ 按钮 ]
- 输入框：┌──────────┐
- 卡片：┌─────────────┐
- 导航：← 返回 [页面标题] [操作]

**输出:** 每个页面的 `page-XXX-name.md` 文件

---

### Phase 4: 人工审核（Approval Gate）

**决策人:** 人类（项目负责人 / 产品 Owner / 技术负责人）

**目的:** 在进入开发阶段之前，确保所有文档完整、准确、无歧义。

**审核范围:**

| 文档 | 审核内容 | 责任人 |
|------|----------|--------|
| `market-research-report.md` | 市场分析是否准确？竞品覆盖是否完整？ | 项目负责人 |
| `prd.md` | 需求是否清晰？User Story 是否完整？验收标准是否可测试？ | 产品 Owner |
| `architecture.md` | 架构设计是否合理？技术选型是否可行？ | 技术负责人 |
| `wireframes/README.md` | 页面是否覆盖所有 User Story？流程是否完整？ | 产品 Owner |
| `wireframes/page-*.md` | 线框图是否清晰？交互说明是否准确？ | 产品 Owner |

**审核流程:**

```
提交审核 → 逐项检查 → 标注问题 → 修改/确认 → 通过/打回
                ↓
           [如有问题]
                ↓
         更新对应文档 → 重新提交审核
```

**审核检查清单:**

#### market-research-report.md
- [ ] 市场规模数据有来源引用
- [ ] 竞品分析至少覆盖 5 个主要竞品
- [ ] 用户痛点有具体证据支撑
- [ ] 结论有数据依据，非主观判断

#### prd.md
- [ ] 每个 User Story 都有明确的 Acceptance Criteria
- [ ] 功能范围（做/不做）已明确界定
- [ ] API 契约与 Architecture 一致
- [ ] 优先级（P0/P1/P2）已标注
- [ ] 风险和依赖已识别

#### architecture.md
- [ ] 系统架构图清晰，展示组件关系
- [ ] 数据模型与 PRD 中的功能对应
- [ ] API 契约与 PRD 中的描述一致
- [ ] 安全设计已考虑
- [ ] 部署架构可行

#### wireframes/*.md
- [ ] 每个 User Story 都有对应页面
- [ ] 页面流程覆盖所有主流程和异常流程
- [ ] 交互说明具体到 API 级别
- [ ] 响应式设计考虑周全
- [ ] 状态处理（空/加载/错误）已覆盖

**审核输出:**

审核通过后，在 `project-config.md` 中记录：
```markdown
## 审核记录

| 文档 | 审核日期 | 审核人 | 状态 | 备注 |
|------|----------|--------|------|------|
| market-research-report.md | 2026-04-05 | @PM | ✅ APPROVED | 无修改 |
| prd.md | 2026-04-05 | @PM | ✅ APPROVED | 小幅调整措辞 |
| architecture.md | 2026-04-05 | @TechLead | ⚠️ APPROVED_WITH_NOTES | 建议增加缓存层 |
| wireframes/*.md | 2026-04-05 | @PM | ✅ APPROVED | 无修改 |
```

**审核状态:**

| 状态 | 含义 | 后续动作 |
|------|------|----------|
| ✅ APPROVED | 审核通过 | 进入下一 Phase |
| ⚠️ APPROVED_WITH_NOTES | 有建议但不阻塞 | 记录建议，进入下一 Phase |
| ❌ REQUEST_CHANGES | 需要修改 | 更新文档 → 重新提交审核 |

**注意:** REQUEST_CHANGES 后，必须先更新对应文档并重新提交审核，不能跳过进入下一 Phase。

---

### Phase 5: UI PROTOTYPE（原型图生成）

**执行 Agent:** UI Designer Agent

**前置输入:**
- `prd.md`
- `architecture.md`
- `design-pattern.json`
- `wireframes/*.md`

**目的:** 将 ASCII 线框图转化为可交互的 HTML 原型图，每个页面一个 HTML 文件。

**输出目录:** `mockups/`

**文件结构:**
```
mockups/
├── README.md                      # 原型图索引 + 交互说明
├── page-001-login.html          # 登录页
├── page-002-home.html           # 首页
├── page-003-list.html           # 列表页
└── ...
```

---

#### Step 1: 原型图生成

**执行 Agent:** UI Designer Agent

**每个 HTML 原型图要求:**

1. **遵循 design-pattern.json**
   - 使用指定的颜色变量
   - 使用指定的字体
   - 使用指定的间距
   - 使用指定的圆角/阴影

2. **实现交互效果**
   - 点击按钮 → 显示 Confirm Modal
   - 表单提交 → 显示 Loading → 显示结果
   - 导航切换 → 页面跳转动画
   - 空状态/加载状态/错误状态

3. **响应式设计**
   - Mobile (< 768px)
   - Tablet (768-1024px)
   - Desktop (> 1024px)

**交互组件示例:**

```html
<!-- Confirm Modal -->
<div id="confirmModal" class="modal" style="display: none;">
  <div class="modal-content">
    <h3>确认操作</h3>
    <p>确定要提交吗？</p>
    <div class="modal-actions">
      <button class="btn-secondary" onclick="closeModal()">取消</button>
      <button class="btn-primary" onclick="confirmSubmit()">确定</button>
    </div>
  </div>
</div>

<script>
function showConfirmModal() {
  document.getElementById('confirmModal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('confirmModal').style.display = 'none';
}

function confirmSubmit() {
  // 显示 Loading
  showLoading();
  // 模拟提交
  setTimeout(() => {
    hideLoading();
    showSuccess('提交成功！');
  }, 1000);
}
</script>
```

4. **页面类型覆盖**
   - 登录/注册页
   - 首页/Dashboard
   - 列表页
   - 详情页
   - 表单页
   - 设置页
   - 错误/空状态页

---

#### Step 2: 人工审核原型图

**决策人:** 产品 Owner / 项目负责人

**审核内容:**

| 检查项 | 说明 |
|--------|------|
| 功能完整性 | 所有 wireframe 中的页面都有对应的原型图？|
| 交互正确性 | 点击/提交/导航等交互符合预期？|
| 设计一致性 | 符合 design-pattern.json 的规范？|
| 响应式适配 | 各断点下布局正常？|
| 状态覆盖 | 空状态/加载状态/错误状态都有实现？|

**审核流程:**

```
提交审核 → 逐项检查 → 标注问题 → 修改/确认 → 通过/打回
                ↓
           [如有问题]
                ↓
         更新原型图 → 重新提交审核
```

**审核状态:**

| 状态 | 含义 | 后续动作 |
|------|------|----------|
| ✅ APPROVED | 审核通过 | 进入 Phase 6 |
| ❌ REQUEST_CHANGES | 需要修改 | 更新原型图 → 重新提交审核 |

**审核输出:**

```markdown
## 原型图审核记录

| 页面 | 功能完整性 | 交互正确性 | 设计一致性 | 响应式适配 | 状态覆盖 | 状态 |
|-------|-----------|-----------|-----------|-----------|----------|------|
| page-001-login.html | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ APPROVED |
| page-002-home.html | ✅ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ APPROVED_WITH_NOTES |
| page-003-list.html | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ REQUEST_CHANGES |

**问题列表:**
- [page-003-list] 点击删除按钮未弹出确认弹窗
- [page-003-list] 列表为空时未显示空状态
```

**注意:** REQUEST_CHANGES 后，必须先更新原型图并重新提交审核，不能跳过进入 Phase 6。

---

### Phase 6: BACKLOG GENERATION（需求池生成）

**执行 Agent:** **PM Agent + Architect Agent**（协作完成）

**前置输入:** `prd.md` + `architecture.md` + `wireframes/*.md`

**目的:** 将 PRD 中的功能需求转化为可执行的 Agile Backlog（Epic + User Story）。

**分工:**

| Agent | 职责 |
|-------|------|
| **PM Agent** | 从业务角度识别 Epic、拆分 User Story、定义验收标准、确定优先级 |
| **Architect Agent** | 从技术角度评估可行性、识别技术债务、评估依赖关系、确认故事点 |

**执行步骤:**

```
Step 1: Epic 识别（PM 主导）
   - PM Agent 从 PRD 的 User Story Map 提取 Epic
   - 按功能模块/用户角色分组
   - Architect Agent 确认 Epic 边界和技术可行性

Step 2: User Story 拆分（PM + Architect 协作）
   - PM Agent 将 Epic 拆解为具体的 User Story
   - Architect Agent 从技术角度拆分（避免过度拆分或拆分不足）
   - 遵循 INVEST 原则

Step 3: Acceptance Criteria 定义（PM 主导）
   - PM Agent 定义业务验收标准
   - Architect Agent 补充技术验收标准
   - 验收标准可测试、可量化

Step 4: 依赖关系标注（Architect 主导）
   - Architect Agent 标注 Story 间技术依赖
   - PM Agent 标注 Story 间业务依赖
   - 识别外部依赖（第三方 API、团队）

Step 5: 技术债务识别（Architect 主导）
   - Architect Agent 记录已知技术债务
   - 评估对 Story 的影响
   - 提出修复建议

Step 6: 优先级和估算（PM + Architect 协作）
   - PM Agent 确定业务优先级（P0/P1/P2）
   - Architect Agent 评估技术复杂度（故事点）
```

**INVEST 原则（Story 质量检查）:**

| 字母 | 含义 | 检查点 |
|------|------|--------|
| **I** ndependent | 独立性 | Story 之间无循环依赖 |
| **N** egotiable | 可协商 | 不是硬性规定，可调整 |
| **V** aluable | 有价值 | 对用户或业务有直接价值 |
| **E** stimable | 可估算 | 工作量可评估 |
| **S** mall | 足够小 | 1-3 天可完成 |
| **T**estable | 可测试 | 验收标准明确 |

**Epic 拆分原则:**

| 维度 | 说明 | 示例 |
|------|------|------|
| 用户角色 | 按不同角色拆分 | 用户端 vs 管理端 |
| 功能模块 | 按业务领域拆分 | 认证模块 vs 订单模块 |
| 业务流程 | 按操作步骤拆分 | 下单 → 支付 → 发货 |
| 成熟度 | 按功能完整性拆分 | MVP vs 增强功能 |

**User Story 格式:**

```markdown
**AS A** [用户角色]
**I WANT** [功能描述]
**SO THAT** [价值/收益]

**Acceptance Criteria:**
- [ ] [标准1]
- [ ] [标准2]

**Technical Notes:**
- [技术实现要点]

**依赖:** [相关 Story]
**相关 API:** [API 列表]
```

**输出:**
- `epics.md` — Epic 列表和详情
- `stories.md` — User Story 列表和详情

**Backlog 汇总表示例:**

```markdown
| Epic | Story | 优先级 | 故事点 | 状态 |
|-------|-------|--------|--------|------|
| EPIC-01 | STORY-001 ~ STORY-005 | P0 | 21 | TODO |
| EPIC-02 | STORY-006 ~ STORY-012 | P0 | 34 | TODO |
| EPIC-03 | STORY-013 ~ STORY-018 | P1 | 26 | TODO |

**汇总:**
- 总 Story: 18
- 总故事点: 81
- P0: 55 (68%)
- P1: 26 (32%)
```

---

### Phase 7: SPRINT PLANNING（仅 L3+）

**执行 Agent:** **Sprint Prioritizer Agent** + Scrum Master Agent

**前置输入:** `stories.md` + `epics.md`

**原则:** **只计划当前 Sprint**，不提前计划后续 Sprint。

**原因:**
- 需求可能变更，后续 Sprint 的优先级会变化
- 每 Sprint 结束后重新评估，灵活调整
- 避免无效的计划工作

**目的:** 将 Backlog 中的 Stories 分配到当前 Sprint，生成 Sprint 计划。

**Sprint Prioritization 算法:**

| 因素 | 权重 | 说明 |
|------|------|------|
| 业务价值 | 30% | 对用户/业务的直接价值 |
| 优先级标签 | 25% | P0 / P1 / P2 |
| 依赖关系 | 20% | 被依赖的应优先完成 |
| 故事点 | 15% | 小故事优先（风险低）|
| 技术债务 | 10% | 修复技术债务优先 |

**Sprint 分配流程:**
```
1. 从 TODO 状态的 Stories 中选择
2. 按优先级分数降序排列
3. 依次尝试加入当前 Sprint
4. 检查 Sprint 容量（不超过目标容量）
5. 检查依赖（被依赖的 Story 必须在当前 Sprint 或已完成）
6. 直到容量填满
```

**Sprint 容量规划:**

| 团队规模 | 建议 Sprint 容量（故事点）|
|----------|--------------------------|
| 2 人 | 15-20 |
| 3 人 | 25-35 |
| 5 人 | 40-55 |
| 8 人 | 60-80 |

**文件结构:**
```
sprints/
├── README.md                    # Sprint 总览（当前 Sprint 信息）
├── sprint-01/
│   └── sprint-01-plan.md       # Sprint 1 计划
├── user-stories-tracker.md     # 全局 Stories 状态追踪（必须维护）
└── backlog-remaining.md         # 剩余 Backlog（未规划 Stories）
```

**输出:**
- `sprints/sprint-01/ sprint-01-plan.md` — 当前 Sprint 的计划
- `sprints/user-stories-tracker.md` — 全局 Stories 状态追踪
- `sprints/backlog-remaining.md` — 剩余 Backlog（下一 Sprint 候选）

**注意:** Sprint 结束后，根据完成情况和新的变更，**重新执行 Phase 7** 计划下一个 Sprint。

---

### Phase 8: IMPLEMENT（开发循环）

**执行 Agent:**
- **Git Workflow Master Agent** — Git worktree 管理、代码合并
- **Frontend Developer Agent** — 前端 UI 实现
- **Backend Developer Agent** — 后端 API 实现
- **Mobile App Builder Agent** — 移动端实现（如果涉及移动端）
- **Code Reviewer Agent** — 代码审查

**前置输入:** `stories.md` + `architecture.md` + `wireframes/*.md` + `design-pattern.json`

**原则:** 每个 Story 独立开发，通过 Git worktree 隔离，并行执行。

---

## 8.1 Story 任务分配

**任务类型判断:**

| Story 类型 | 分配给 | 技术栈 |
|-----------|--------|--------|
| 纯前端功能 | Frontend Developer | React/Vue/Angular |
| 纯后端功能 | Backend Developer | Node.js/Python/Go |
| 全栈功能 | Frontend + Backend | 两端都需要 |
| 移动端功能 | Mobile App Builder | React Native/Flutter/Swift/Kotlin |

**分配规则:**
- 独立 Story 可并行分配给不同 Developer
- 有依赖的 Story 需串行执行（前端 Story 依赖后端 API 完成）

---

## 8.2 收集需求和技术设计

**每个 Story 开发前，必须收集:**

1. **Story Acceptance Criteria** — 来自 `stories.md`
2. **API 契约** — 来自 `architecture.md` 中的 API 设计
3. **数据模型** — 来自 `architecture.md` 中的数据库设计
4. **Wireframe** — 来自 `wireframes/*.md` 中的页面设计
5. **设计规范** — 来自 `design-pattern.json`

**输出:** `story-implementation-plan-{id}.md` — 每个 Story 的实现计划

---

## 8.3 创建 Git Worktree

**执行 Agent:** Git Workflow Master Agent

**流程:**
```bash
# 为当前 Story 创建 worktree
git fetch origin
git worktree add ../worktrees/story-{$ID}-{$FEATURE_NAME} origin/main

# 创建功能分支
git checkout -b feat/story-{$ID}-{$FEATURE_NAME}

# 推送分支
git push -u origin feat/story-{$ID}-{$FEATURE_NAME}
```

**Worktree 命名规范:**
```
story-001-user-auth
story-002-user-login
story-003-content-list
```

---

## 8.4 QA E2E 测试用例编写（并行）

**执行 Agent:** QA Agent

**目的:** 与 Developer 的 TDD 开发并行进行，QA Agent 提前编写 E2E 测试用例。

**触发时机:** Story 分配后，与 7.5 TDD 开发并行开始。

---

#### Step 1: 理解 User Story

**QA Agent 动作:**
1. 阅读 `stories.md` 中对应 Story 的 Acceptance Criteria
2. 阅读 `wireframes/*.md` 中对应页面的线框图
3. 阅读 `architecture.md` 中 API 契约
4. 识别测试场景和边界条件

**输出:** 理解文档，记录关键测试点

---

#### Step 2: 编写 E2E 测试用例

**每个 Story 生成独立文件:**

```
sprints/sprint-01/
├── sprint-01-plan.md
├── e2e-test-cases/
│   ├── STORY-001-user-registration.spec.ts
│   ├── STORY-002-user-login.spec.ts
│   └── STORY-003-content-list.spec.ts
└── ...
```

**E2E 测试用例格式:**

```typescript
// e2e-test-cases/STORY-001-user-registration.spec.ts
import { test, expect } from '@playwright/test';

/**
 * STORY-001: 用户注册
 * 
 * User Story:
 * AS A 游客
 * I WANT 通过手机号注册账号
 * SO THAT 成为系统用户，使用完整功能
 * 
 * Acceptance Criteria:
 * - [ ] 可以输入手机号获取验证码
 * - [ ] 验证码有效期为 5 分钟
 * - [ ] 可以设置密码（至少 8 位，包含字母和数字）
 * - [ ] 注册成功后自动登录
 * - [ ] 同一手机号不能重复注册
 */

test.describe('STORY-001: 用户注册', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/register');
  });

  test('成功注册并自动登录', async ({ page }) => {
    // 输入手机号
    await page.fill('[data-testid=phone-input]', '+8613800138000');
    
    // 点击获取验证码
    await page.click('[data-testid=send-code-btn]');
    
    // 验证倒计时显示
    await expect(page.locator('[data-testid=countdown]')).toContainText('60');
    
    // 模拟接收到验证码（实际测试中需要 mock SMS API）
    // 输入验证码
    await page.fill('[data-testid=verify-code-input]', '123456');
    
    // 输入密码
    await page.fill('[data-testid=password-input]', 'SecurePass123');
    
    // 提交注册
    await page.click('[data-testid=register-btn]');
    
    // 验证跳转到首页
    await expect(page).toHaveURL('/home');
    
    // 验证用户已登录（显示用户信息）
    await expect(page.locator('[data-testid=user-avatar]')).toBeVisible();
  });

  test('重复手机号注册失败', async ({ page }) => {
    // 先注册一个账号
    await page.fill('[data-testid=phone-input]', '+8613800138000');
    await page.click('[data-testid=send-code-btn]');
    await page.fill('[data-testid=verify-code-input]', '123456');
    await page.fill('[data-testid=password-input]', 'SecurePass123');
    await page.click('[data-testid=register-btn]');
    
    // 尝试用同一手机号再次注册
    await page.goto('/register');
    await page.fill('[data-testid=phone-input]', '+8613800138000');
    await page.click('[data-testid=send-code-btn]');
    
    // 验证显示错误提示
    await expect(page.locator('[data-testid=error-message]')).toContainText('该手机号已注册');
  });

  test('弱密码注册失败', async ({ page }) => {
    await page.fill('[data-testid=phone-input]', '+8613800138001');
    await page.click('[data-testid=send-code-btn]');
    await page.fill('[data-testid=verify-code-input]', '123456');
    await page.fill('[data-testid=password-input]', '123');
    await page.click('[data-testid=register-btn]');
    
    // 验证显示密码强度不足提示
    await expect(page.locator('[data-testid=password-error]')).toContainText('密码至少8位');
  });

  test('验证码过期后无法注册', async ({ page }) => {
    // 等待验证码过期（实际测试中可以使用时间 mock）
    await page.fill('[data-testid=phone-input]', '+8613800138002');
    await page.click('[data-testid=send-code-btn]');
    
    // 等待验证码过期（模拟 5 分钟后）
    // 实际测试中需要操作时间或使用 mock
    await page.fill('[data-testid=verify-code-input]', '123456');
    await page.fill('[data-testid=password-input]', 'SecurePass123');
    await page.click('[data-testid=register-btn]');
    
    // 验证显示验证码过期提示
    await expect(page.locator('[data-testid=error-message]')).toContainText('验证码已过期');
  });

});
```

---

#### Step 3: 更新 User Story 文档

**执行 Agent:** QA Agent

**动作:** 在 `stories.md` 中对应的 Story 下，添加 E2E 测试用例链接：

```markdown
### STORY-001: 用户注册

**AS A** 游客
**I WANT** 通过手机号注册账号
**SO THAT** 成为系统用户，使用完整功能

**Acceptance Criteria:**
- [ ] 可以输入手机号获取验证码
- [ ] 验证码有效期为 5 分钟
- [ ] 可以设置密码（至少 8 位，包含字母和数字）
- [ ] 注册成功后自动登录
- [ ] 同一手机号不能重复注册

**E2E 测试用例:** `sprints/sprint-01/e2e-test-cases/STORY-001-user-registration.spec.ts`
```

---

#### Step 4: 标记 E2E 用例状态

| 状态 | 含义 |
|------|------|
| 📝 DRAFT | 测试用例初稿，待评审 |
| 🔍 IN_REVIEW | 测试用例评审中 |
| ✅ APPROVED | 测试用例已确认，可在 CI 中运行 |
| 🚫 DEPRECATED | 测试用例已废弃（Story 变更）|

---

**并行执行说明:**

```
┌──────────────────────────────────────────────────────────────────┐
│  7.3 Git Worktree 创建                                          │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────┐    ┌─────────────────────────────┐
│  7.4 QA E2E 用例编写     │    │  7.5 Developer TDD 开发    │
│  QA Agent 并行进行         │    │  Developer Agent 并行进行   │
│                            │    │                            │
│  • 理解 Story             │    │  • 编写单元测试（RED）      │
│  • 编写 E2E 测试用例       │    │  • 编写实现（GREEN）        │
│  • 更新 stories.md         │    │  • 重构（REFACTOR）        │
│                            │    │                            │
└─────────────────────────────┘    └─────────────────────────────┘
                              ↓
                    两个任务都完成后继续
```

**注意:**
- 7.4 和 7.5 是并行执行，不阻塞对方
- E2E 测试用例在 Story 开发完成后执行
- QA Agent 编写用例时不需要等待代码完成

---

## 8.5 TDD 开发循环

**执行 Agent:** 对应的 Developer Agent（Frontend / Backend / Mobile）

**强制 TDD 流程（不可跳过）:**

```
FOR EACH Story:
    ┌─────────────────────────────────────────────┐
    │ Step 1: 编写测试用例（RED）                  │
    │ - 理解 Acceptance Criteria                    │
    │ - 编写单元测试 / E2E 测试                    │
    │ - 运行测试，确认失败                         │
    └─────────────────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────┐
    │ Step 2: 实现代码（GREEN）                   │
    │ - 编写最简实现让测试通过                     │
    │ - 不写未来可能用到的代码                     │
    │ - 保持代码简洁                              │
    └─────────────────────────────────────────────┘
                       ↓
    ┌─────────────────────────────────────────────┐
    │ Step 3: 重构优化（REFACTOR）               │
    │ - 消除重复代码                               │
    │ - 提升可读性                                 │
    │ - 优化性能（如需要）                         │
    │ - 确保测试仍然通过                           │
    └─────────────────────────────────────────────┘
                       ↓
                   Story 完成
```

---

## 8.6 代码审查

**执行 Agent:** Code Reviewer Agent

**审查维度:**

| 维度 | 检查点 |
|------|--------|
| **正确性** | 代码是否实现了 Acceptance Criteria？|
| **安全性** | 有无注入/越权/敏感数据暴露？|
| **可维护性** | 6个月后还能看懂吗？|
| **性能** | 有无 N+1 查询/阻塞主线程？|
| **测试** | 重要路径都有测试吗？|

**Review 结果:**

| 结果 | 含义 | 动作 |
|------|------|------|
| ✅ APPROVED | 可以合并 | 进入下一步 |
| 🔴 REQUEST_CHANGES | 需要修改 | 返回给开发者修复 |

**审查反馈格式:**

```markdown
🔴 **Blocker:** SQL 注入风险
Line 42: 用户输入直接拼接到 SQL 查询中。

**建议:** 使用参数化查询：
```sql
SELECT * FROM users WHERE phone = $1
```

🟡 **Suggestion:** 可以用 Promise.all() 并行请求

💭 **Nit:** 变量名 `d` 可以改成 `data`
```

---

## 8.7 修复审查问题

**执行 Agent:** 对应的 Developer Agent

**流程:**
```
收到 REQUEST_CHANGES
    ↓
修复所有 🔴 Blocker（必须）
    ↓
修复 🟡 Suggestion（如有必要）
    ↓
处理 💭 Nit（如有必要）
    ↓
重新提交 Code Review
```

---

## 8.8 执行测试

**执行 Agent:** QA Agent

**测试类型:**

| 测试类型 | 覆盖率目标 | 执行时机 |
|----------|-----------|----------|
| 单元测试 | > 80% | 每次 commit |
| 集成测试 | > 60% | PR 创建时 |
| E2E 测试 | 核心流程覆盖 | Sprint 结束时（可选）|

**测试报告:**
```markdown
## Test Report: STORY-001

| 测试类型 | 用例数 | 通过 | 失败 | 覆盖率 |
|---------|--------|------|------|--------|
| 单元测试 | 24 | 24 | 0 | 87% |
| 集成测试 | 8 | 8 | 0 | 65% |
| E2E 测试 | 3 | 2 | 1 | - |

**失败用例:**
- [E2E-001] 注册成功后未跳转首页 → 已修复
```

---

## 8.9 E2E 测试（可选）

**执行 Agent:** QA Agent

**E2E 测试范围:**
- 核心用户流程（注册 → 登录 → 主要功能）
- 高风险功能（支付/订单/敏感操作）

**工具推荐:**
- Web: Playwright / Cypress
- Mobile: Appium / Detox

---

## 8.10 代码合并

**执行 Agent:** Git Workflow Master Agent

**合并流程:**
```bash
# 1. 确保所有测试通过
# 2. 确保 Code Review 通过
# 3. Rebase 最新 main 分支
git fetch origin
git rebase origin/main

# 4. 合并到 main
git checkout main
git merge --no-ff feat/story-{$ID}-{$FEATURE_NAME}

# 5. 删除分支和 worktree
git branch -d feat/story-{$ID}-{$FEATURE_NAME}
git worktree remove ../worktrees/story-{$ID}-{$FEATURE_NAME}

# 6. 推送
git push origin main
git push origin --delete feat/story-{$ID}-{$FEATURE_NAME}
```

---

## 8.11 更新 Sprint 追踪

**执行 Agent:** Sprint Prioritizer Agent + Scrum Master Agent

**目的:** 在 Story 完成后，及时更新 `user-stories-tracker.md`，保持状态可见。

**更新内容:**

| 字段 | 更新值 |
|------|--------|
| Story 状态 | `✅ DONE` |
| 完成日期 | 当前日期 |
| 实际故事点 | 与预估对比 |

**Story 状态流转:**
```
⏳ TODO → 🔄 IN_PROGRESS → 🔍 CODE_REVIEW → 🧪 TESTING → ✅ DONE
```

**更新格式示例:**
```markdown
| STORY-001 | 用户注册 | P0 | 3 | Sprint 01 | ✅ DONE | 2026-04-05 | @dev1 |
```

**触发时机:**
- 代码成功合并到 main 分支后
- 所有测试通过后
- Code Review 通过后

**注意:**
- 每次 Story 状态变更都应立即更新 tracker
- 保持 tracker 是团队唯一的真相来源（Single Source of Truth）
- Sprint 结束时，tracker 状态作为 Sprint Review 的依据---

## Phase 8 完整流程

```
┌──────────────────────────────────────────────────────────────────┐
│  Story 分配 → Frontend / Backend / Mobile Developer             │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Git Workflow Master: 创建 Worktree                             │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────┐    ┌─────────────────────────────┐
│  7.4 QA E2E 用例编写     │    │  7.5 Developer TDD 开发    │
│  QA Agent 并行            │    │  Developer Agent 并行       │
│                           │    │                            │
│  • 理解 Story            │    │  • 编写单元测试（RED）      │
│  • 编写 E2E 测试用例    │    │  • 编写实现（GREEN）        │
│  • 更新 stories.md        │    │  • 重构（REFACTOR）        │
└─────────────────────────────┘    └─────────────────────────────┘
                              ↓
                    两个任务都完成后继续
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Code Reviewer: 代码审查                                         │
│  🔴 REQUEST_CHANGES? → 返回修复 → 重新审查                      │
│  ✅ APPROVED → 继续                                              │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  QA Agent: 执行测试 → 生成测试报告                               │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  E2E 测试（如需要）→ 生成测试报告                                │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Git Workflow Master: 合并 Worktree 到 Main                     │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  **7.10 更新 Sprint 追踪**                                      │
│  Sprint Prioritizer Agent: 更新 user-stories-tracker.md          │
└──────────────────────────────────────────────────────────────────┘
                              ↓
                         Story 完成
```

**输出:**
- 完成的代码（已合并到 main）
- 测试报告（`test-report-{story-id}.md`）
- 更新的 `user-stories-tracker.md`

---

### Phase 9: CODE REVIEW

**执行 Agent:** Tech Lead Agent + QA Agent

**检查清单:**
- [ ] 代码符合 Architecture
- [ ] 测试覆盖率达标
- [ ] 无安全漏洞
- [ ] 文档已更新

**输出:** `review-report.md`

---

## 需求变更控制（Change Control Gate）

**这是核心机制。任何变更必须经过此流程。**

---

### 变更触发条件

以下情况必须触发 Change Control Gate：
- SPEC 已批准后，提出新需求
- 实现过程中，修改已批准的 SPEC 内容
- 发现遗漏需求，要求补充

---

### Change Control Gate 流程

```
变更请求 → 影响评估 → 变更决策 → 更新文档 → 重新同步
    ↑                                              ↓
    └──────────── 拒绝变更（返回原计划）─────────────┘
```

---

### Step 1: 变更请求

**执行 Agent:** PM Agent 或 Developer Agent

**动作:**
- 记录变更内容
- 说明变更原因
- 标注变更来源（用户/开发/外部）

**输出:** `change-request.md`

---

### Step 2: 影响评估

**执行 Agent:** Architect Agent + Tech Lead

**评估维度:**
1. **范围影响** — 哪些 Stories 会受影响？
2. **时间影响** — 预计增加多少工作量？
3. **技术影响** — 需要修改哪些架构/设计？
4. **风险影响** — 引入什么新风险？

**输出:** 影响评估报告（内附 `change-request.md`）

---

### Step 3: 变更决策

**决策人:** 人类（项目负责人/产品 owner）

**三种决策:**
| 决策 | 含义 |
|------|------|
| **APPROVED** | 接受变更，更新文档，纳入下一 Sprint |
| **REJECTED** | 拒绝变更，维持原计划 |
| **DEFERRED** | 推迟到下个版本，不影响当前 Sprint |

**文档化:** 决策结果记录在 `change-log.md`

---

### Step 4: 更新文档

**执行 Agent:** PM Agent + Architect Agent

**变更批准后:**
- 更新 `spec.md`（如有必要）
- 更新 `stories.md`
- 更新 `sprint-XX.md`
- 通知所有相关 Agent

---

### Step 5: 重新同步

**执行 Agent:** Scrum Master Agent

**动作:**
- 重新评估 Sprint 计划
- 调整 Stories 优先级
- 更新进度报告
- 向团队广播变更通知

---

### 变更日志（必须维护）

文件: `change-log.md`

```markdown
| ID | 日期 | 变更描述 | 影响评估 | 决策 | 执行者 |
|----|------|----------|----------|------|--------|
| CHG-001 | 2026-04-05 | 添加支付模块 | +3 stories, +2 days | APPROVED | @alice |
| CHG-002 | 2026-04-06 | 修改用户认证逻辑 | +1 story, +4 hours | APPROVED | @bob |
```

---

## Agent 团队角色

详细 Persona 定义见 [`agents/`](./agents/) 目录。

| Agent | Emoji | 职责 | 关键能力 |
|-------|-------|------|----------|
| **Lead Agent** | 🎯 | 项目总负责，复杂度判定 | 项目管理 |
| **Trend Researcher Agent** | 🔍 | 市场调研，竞品分析 | 情报收集 |
| **PM Agent** | 📋 | 需求管理，PRD | 沟通，Socratic 提问 |
| **UI Designer Agent** | 🎨 | 设计系统，风格规范 | 视觉设计 |
| **UX Designer Agent** | 🎨 | 线框图设计，交互设计 | ASCII Art |
| **Architect Agent** | 🏗️ | 技术设计，架构决策 | 系统设计 |
| **Frontend Developer Agent** | 🖥️ | 前端开发，React/Vue/Angular | UI 实现，性能优化 |
| **Backend Developer Agent** | 🏗️ | 后端开发，API/数据库 | 微服务，安全实现 |
| **Mobile App Builder Agent** | 📲 | 移动端开发，iOS/Android | React Native/Flutter |
| **Git Workflow Master Agent** | 🌿 | Git worktree，分支管理 | commit 规范，代码合并 |
| **Code Reviewer Agent** | 👁️ | 代码审查，质量把关 | 安全性，可维护性 |
| **Tech Lead Agent** | 🔧 | 代码质量，技术指导 | Code Review |
| **QA Agent** | 🎯 | 测试，质量保障 | 自动化测试 |
| **Scrum Master Agent** | ⚡ | 流程把控，Sprint 管理 | 敏捷管理 |
| **Sprint Prioritizer Agent** | 📊 | Sprint 规划，优先级排序 | 优先级算法 |
| **Analyst Agent** | 📊 | 调研，风险评估 | 研究分析 |

---

## 文档体系

| 文档 | 阶段 | 用途 |
|------|------|------|
| `project-config.md` | INIT | 项目配置 |
| `market-research-report.md` | Phase 1.1 | 市场调研报告 |
| `prd.md` | Phase 1.2 | 产品需求文档 |
| `architecture.md` | Phase 1.3 | 技术架构文档 |
| `design-pattern.json` | Phase 2 | **设计系统规范（强制）** |
| `wireframes/README.md` | Phase 3 | 页面索引 + 流程图 |
| `wireframes/page-XXX-*.md` | Phase 3 | 页面线框图（每个页面一个文件）|
| `approval-record.md` | Phase 4 | 人工审核记录 |
| `epics.md` | Phase 5 | Epic 列表 |
| `stories.md` | Phase 5 | Story 列表 |
| `sprints/README.md` | Phase 7 | Sprint 总览 |
| `sprints/sprint-XX/ sprint-XX-plan.md` | Phase 7 | Sprint 计划（每个 Sprint 一个文件夹）|
| `sprints/user-stories-tracker.md` | Phase 7 | **Stories 状态追踪（必须维护）** |
| `story-implementation-plan-{id}.md` | Phase 7 | Story 实现计划 |
| `worktrees/story-XXX-*.md` | Phase 7 | Worktree 状态 |
| `test-report-{story-id}.md` | Phase 7 | 测试报告 |
| `tech-debt.md` | 持续 | 技术债务记录 |
| `change-request.md` | CHANGE | 变更请求 |
| `change-log.md` | CHANGE | 变更日志 |
| `review-report.md` | Phase 8 | 评审报告 |

---

## 快速参考

### 启动新项目
```
1. 确定复杂度等级（L1-L4）
2. 创建项目目录
3. 运行对应流程
```

### 提交变更
```
1. 创建 change-request.md
2. 等待影响评估
3. 等待决策（APPROVED/REJECTED/DEFERRED）
4. 执行或放弃
```

---

**下一步：模板化 + 工具化**
