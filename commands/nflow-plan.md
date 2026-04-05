# /nflow-plan

## Backlog 生成 + Sprint 规划

**Phase:** Phase 6-7

**执行时机:** 完成 `/nflow-prototype` 后

**执行 Agent:** PM Agent + Architect Agent → Sprint Prioritizer Agent + Scrum Master Agent

---

## Phase 6: Backlog 生成

### Step 1: Epic 识别（PM + Architect）

**前置:** `prd.md` + `architecture.md` + `wireframes/*.md`

**输出:** `epics.md`

**Epic 拆分原则:**
- 按用户角色（用户端 vs 管理端）
- 按功能模块（认证模块 vs 订单模块）
- 按业务流程（下单 → 支付 → 发货）

### Step 2: User Story 拆分（PM + Architect）

**输出:** `stories.md`

**遵循 INVEST 原则:**

| 字母 | 含义 | 检查点 |
|------|------|--------|
| **I** ndependent | 独立 | 无循环依赖 |
| **N** egotiable | 可协商 | 可调整 |
| **V** aluable | 有价值 | 对用户/业务有价值 |
| **E** stimable | 可估算 | 工作量可评估 |
| **S** mall | 足够小 | 1-3 天可完成 |
| **T**estable | 可测试 | 验收标准明确 |

### Step 3: 故事点估算 + 优先级

**PM + Architect 协作:**
- PM Agent 确定业务优先级（P0 / P1 / P2）
- Architect Agent 评估技术复杂度（故事点）

---

## Phase 7: Sprint 规划

### Step 4: Sprint Prioritization（Sprint Prioritizer Agent）

**原则:** 只计划当前 Sprint，不提前计划后续。

**优先级算法（5 因素加权）:**

| 因素 | 权重 |
|------|------|
| 业务价值 | 30% |
| 优先级标签（P0/P1/P2）| 25% |
| 依赖关系 | 20% |
| 故事点（小优先）| 15% |
| 技术债务 | 10% |

### Step 5: Sprint 容量规划

| 团队规模 | Sprint 容量（故事点）|
|----------|-------------------|
| 2 人 | 15-20 |
| 3 人 | 25-35 |
| 5 人 | 40-55 |

### Step 6: 生成 Sprint 文件

```
sprints/
├── README.md
├── sprint-01/
│   └── sprint-01-plan.md
├── user-stories-tracker.md
└── backlog-remaining.md
```

---

## 输出文件

| 文件 | Agent | 状态 |
|------|-------|------|
| `epics.md` | PM + Architect | ⏳ |
| `stories.md` | PM + Architect | ⏳ |
| `sprints/sprint-01/sprint-01-plan.md` | Sprint Prioritizer | ⏳ |
| `sprints/user-stories-tracker.md` | Sprint Prioritizer | ⏳ |

---

## 下一步

```
/nflow-dev
```
