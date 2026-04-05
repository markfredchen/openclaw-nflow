# PRD Template: [项目名称]

**版本:** v1.0
**日期:** YYYY-MM-DD
**状态:** DRAFT | IN_REVIEW | APPROVED
**负责人:** PM Agent

---

## 1. Executive Summary

[1-2段概述：做什么、解决什么问题、核心价值主张]

---

## 2. Goals & Success Metrics

### 2.1 Product Goals

| 目标 | 衡量指标 | 目标值 |
|------|----------|--------|
| [目标1] | [KPI] | [数值] |
| [目标2] | [KPI] | [数值] |

### 2.2 Success Metrics

- **Primary:** [核心指标，如DAU/GMV/转化率]
- **Secondary:** [辅助指标]
- **North Star:** [北极星指标]

---

## 3. User Stories

### 3.1 Target Users

| 用户角色 | 描述 | 使用场景 |
|----------|------|----------|
| [角色1] | [描述] | [场景] |
| [角色2] | ... | ... |

### 3.2 User Story Map

```
[Epic 1]
├── [Story 1.1]
├── [Story 1.2]
└── [Story 1.3]

[Epic 2]
├── [Story 2.1]
└── [Story 2.2]
```

### 3.3 Detailed User Stories

#### Story: [ID-001]
**AS A** [用户角色]
**I WANT** [功能描述]
**SO THAT** [价值/收益]

**Acceptance Criteria:**
- [ ] [标准1]
- [ ] [标准2]
- [ ] [标准3]

**Priority:** P0 | P1 | P2
**Story Points:** 1 | 2 | 3 | 5 | 8 | 13

---

## 4. Functional Requirements

### 4.1 Core Features

| Feature | Description | Priority | Notes |
|---------|-------------|----------|-------|
| [功能1] | [描述] | P0 | [备注] |
| [功能2] | [描述] | P1 | ... |

### 4.2 User Flows

```
[流程名称]
─────────────────────────────
User Action → System Response
     ↓              ↓
  [步骤1]  →   [响应1]
  [步骤2]  →   [响应2]
  ...
```

### 4.3 Data Requirements

| 数据 | 来源 | 更新频率 | 存储 |
|------|------|----------|------|
| [数据1] | [来源] | [频率] | [方式] |

### 4.4 API Contracts

#### [API名称]
**Endpoint:** `POST /api/v1/...`
**Request:**
```json
{
  "field1": "string",
  "field2": "number"
}
```
**Response:**
```json
{
  "code": 0,
  "data": {}
}
```

---

## 5. Non-Functional Requirements

| 维度 | 要求 |
|------|------|
| Performance | [响应时间 < Xms] |
| Availability | [99.9%] |
| Scalability | [支持 N 并发用户] |
| Security | [认证/加密等] |
| Compatibility | [iOS X / Android Y / Browser Z] |

---

## 6. Out of Scope

- ~~[明确不做的功能1]~~
- ~~[明确不做的功能2]~~

---

## 7. Risks & Mitigations

| 风险 | 影响 | 概率 | 应对策略 |
|------|------|------|----------|
| [风险1] | [高/中/低] | [高/中/低] | [策略] |

---

## 8. Dependencies

| 依赖方 | 依赖内容 | 状态 | 备注 |
|--------|----------|------|------|
| [团队/系统] | [内容] | [就绪/待定/阻塞] | ... |

---

## 9. Glossary

| 术语 | 定义 |
|------|------|
| [术语1] | [定义] |

---

## 10. Revision History

| 版本 | 日期 | 修改内容 | 修改人 |
|------|------|----------|--------|
| v1.0 | YYYY-MM-DD | 初始版本 | PM Agent |
