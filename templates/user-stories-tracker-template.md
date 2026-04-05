# User Stories 状态追踪

**项目:** [项目名称]
**版本:** v当前版本
**最后更新:** YYYY-MM-DD
**负责人:** Scrum Master Agent

---

## 概览

| 指标 | 值 |
|------|-----|
| 总 Story 数 | 18 |
| 总故事点 | 81 |
| 已完成 | 5 | 27.8%
| 开发中 | 3 | 16.7%
| 待开发 | 10 | 55.5% |

**当前 Sprint:**

| Sprint | 日期范围 | 承诺故事点 | 已完成 | 进度 |
|--------|----------|-----------|--------|------|
| Sprint 01 | 04/01 ~ 04/14 | 42 | 20 | 🔄 48% |

**后续 Sprint:** 待 Sprint 01 结束后计划

---

## Stories 详情

### EPIC-01: 用户模块（5 Stories, 21 故事点）

| Story ID | 名称 | 优先级 | 故事点 | Sprint | 状态 | 负责人 | 备注 |
|----------|------|--------|--------|--------|------|--------|------|
| STORY-001 | 用户注册 | P0 | 3 | Sprint 01 | ✅ DONE | @dev1 | |
| STORY-002 | 用户登录 | P0 | 5 | Sprint 01 | ✅ DONE | @dev1 | |
| STORY-003 | 用户登出 | P0 | 2 | Sprint 01 | ✅ DONE | @dev2 | |
| STORY-004 | 修改密码 | P1 | 5 | Sprint 02 | 🔄 IN_PROGRESS | @dev2 | |
| STORY-005 | 忘记密码 | P1 | 6 | Sprint 02 | ⏳ TODO | @dev1 | 依赖 STORY-004 |

---

### EPIC-02: 内容模块（8 Stories, 34 故事点）

| Story ID | 名称 | 优先级 | 故事点 | Sprint | 状态 | 负责人 | 备注 |
|----------|------|--------|--------|--------|------|--------|------|
| STORY-006 | 内容列表 | P0 | 5 | Sprint 01 | ✅ DONE | @dev3 | |
| STORY-007 | 内容详情 | P0 | 3 | Sprint 01 | ✅ DONE | @dev3 | |
| STORY-008 | 创建内容 | P0 | 8 | Sprint 02 | 🔄 IN_PROGRESS | @dev3 | |
| STORY-009 | 编辑内容 | P1 | 5 | Sprint 02 | ⏳ TODO | @dev3 | 依赖 STORY-008 |
| STORY-010 | 删除内容 | P1 | 3 | Sprint 02 | ⏳ TODO | @dev3 | 依赖 STORY-008 |
| STORY-011 | 内容搜索 | P2 | 3 | Sprint 03 | ⏳ TODO | @dev4 | |
| STORY-012 | 内容分类 | P2 | 3 | Sprint 03 | ⏳ TODO | @dev4 | |
| STORY-013 | 内容置顶 | P2 | 4 | Sprint 03 | ⏳ TODO | @dev4 | |

---

### EPIC-03: 订单模块（6 Stories, 26 故事点）

| Story ID | 名称 | 优先级 | 故事点 | Sprint | 状态 | 负责人 | 备注 |
|----------|------|--------|--------|--------|------|--------|------|
| STORY-014 | 创建订单 | P0 | 8 | Sprint 02 | 🔄 IN_PROGRESS | @dev1 | |
| STORY-015 | 订单列表 | P0 | 5 | Sprint 02 | ⏳ TODO | @dev2 | 依赖 STORY-014 |
| STORY-016 | 订单详情 | P1 | 3 | Sprint 03 | ⏳ TODO | - | |
| STORY-017 | 取消订单 | P1 | 5 | Sprint 03 | ⏳ TODO | - | |
| STORY-018 | 订单导出 | P2 | 3 | Sprint 03 | ⏳ TODO | - | |
| STORY-019 | 订单统计 | P2 | 2 | Sprint 03 | ⏳ TODO | - | |

---

## 状态说明

| 状态 | 含义 | 进度 |
|------|------|------|
| ⏳ TODO | 尚未开始 | 0% |
| 🔄 IN_PROGRESS | 开发中 | 1-99% |
| 🔍 CODE_REVIEW | Code Review 中 | 80% |
| 🧪 TESTING | 测试中 | 90% |
| ✅ DONE | 已完成 | 100% |
| 🚫 BLOCKED | 被阻塞 | 0% |

---

## Sprint 分配表

### Sprint 01 (04/01 ~ 04/14) ✅ 已完成

**目标:** 完成用户认证和基础内容模块

| Story | 名称 | 故事点 | 状态 |
|-------|------|--------|------|
| STORY-001 | 用户注册 | 3 | ✅ DONE |
| STORY-002 | 用户登录 | 5 | ✅ DONE |
| STORY-003 | 用户登出 | 2 | ✅ DONE |
| STORY-006 | 内容列表 | 5 | ✅ DONE |
| STORY-007 | 内容详情 | 3 | ✅ DONE |

**Sprint 01 总结:** 承诺 18 故事点，实际完成 18 故事点，进度 100%

---

### Sprint 02 (04/15 ~ 04/28) 🔄 进行中

**目标:** 完成内容管理和订单模块

| Story | 名称 | 故事点 | 状态 |
|-------|------|--------|------|
| STORY-004 | 修改密码 | 5 | 🔄 IN_PROGRESS |
| STORY-005 | 忘记密码 | 6 | ⏳ TODO |
| STORY-008 | 创建内容 | 8 | 🔄 IN_PROGRESS |
| STORY-009 | 编辑内容 | 5 | ⏳ TODO |
| STORY-010 | 删除内容 | 3 | ⏳ TODO |
| STORY-014 | 创建订单 | 8 | 🔄 IN_PROGRESS |
| STORY-015 | 订单列表 | 5 | ⏳ TODO |

**Sprint 02 进行中:** 承诺 40 故事点，已完成 13 故事点，进度 32%

**当前阻塞:**
- SMS API 限流导致 STORY-005 依赖的验证码功能不稳定

---

### Sprint 03 (04/29 ~ 05/12) ⏳ 待开始

**目标:** 完成订单管理和内容增强功能

| Story | 名称 | 故事点 | 状态 |
|-------|------|--------|------|
| STORY-011 | 内容搜索 | 3 | ⏳ TODO |
| STORY-012 | 内容分类 | 3 | ⏳ TODO |
| STORY-013 | 内容置顶 | 4 | ⏳ TODO |
| STORY-016 | 订单详情 | 3 | ⏳ TODO |
| STORY-017 | 取消订单 | 5 | ⏳ TODO |
| STORY-018 | 订单导出 | 3 | ⏳ TODO |
| STORY-019 | 订单统计 | 2 | ⏳ TODO |

---

## 速度趋势

```
Sprint 01: ████████████████████ 18/18 故事点 (100%)
Sprint 02: ████████░░░░░░░░░░░ 13/40 故事点 (32%) [进行中]
Sprint 03: ░░░░░░░░░░░░░░░░░░ 0/26 故事点 (0%) [待开始]
```

**平均速度:** 18 故事点/Sprint

---

## 风险追踪

| ID | 风险 | 概率 | 影响 | 应对 | 状态 |
|----|------|------|------|------|------|
| RISK-001 | SMS API 限流 | 高 | 中 | 接入备用供应商 | 🔍 监控中 |
| RISK-002 | 第三方支付回调延迟 | 中 | 高 | 增加重试机制 | ⏳ 待实施 |

---

## 依赖关系追踪

| Story | 依赖 | 被依赖 | 当前状态 |
|-------|------|--------|----------|
| STORY-001 | - | STORY-002 | ✅ DONE |
| STORY-002 | STORY-001 | - | ✅ DONE |
| STORY-005 | STORY-004 | - | ⏳ TODO |
| STORY-008 | - | STORY-009, STORY-010 | 🔄 IN_PROGRESS |
| STORY-014 | - | STORY-015 | 🔄 IN_PROGRESS |

---

**最后更新:** YYYY-MM-DD HH:mm
**下次更新:** 每日站会后
