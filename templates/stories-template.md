# User Stories 列表

**项目:** [项目名称]
**版本:** v1.0
**日期:** YYYY-MM-DD
**状态:** DRAFT | APPROVED
**负责人:** PM Agent + Architect Agent（协作生成）

---

## Stories 概览

| Story ID | Epic | Story 名称 | 优先级 | 故事点 | 负责人 | 状态 |
|----------|------|-----------|--------|--------|--------|------|
| STORY-001 | EPIC-01 | 用户注册 | P0 | 3 | @dev1 | TODO |
| STORY-002 | EPIC-01 | 用户登录 | P0 | 5 | @dev1 | TODO |
| STORY-003 | EPIC-01 | 用户登出 | P0 | 2 | @dev2 | TODO |
| ... | ... | ... | ... | ... | ... | ... |

**汇总:**
- 总 Story 数: XX
- 总故事点: XX
- P0 故事点: XX
- P1 故事点: XX
- P2 故事点: XX

---

## Stories 详情

### STORY-001

**所属 Epic:** EPIC-01
**标题:** 用户注册
**优先级:** P0
**故事点:** 3
**负责人:** @dev1
**状态:** TODO

**AS A** 游客
**I WANT** 通过手机号注册账号
**SO THAT** 成为系统用户，使用完整功能

**Acceptance Criteria:**
- [ ] 可以输入手机号获取验证码
- [ ] 验证码有效期为 5 分钟
- [ ] 可以设置密码（至少 8 位，包含字母和数字）
- [ ] 注册成功后自动登录
- [ ] 同一手机号不能重复注册
- [ ] 密码加密存储（bcrypt）

**Technical Notes:**
- 使用 JWT 进行身份验证
- 验证码存储在 Redis，有效期 5 分钟
- 密码使用 bcrypt 加密（cost=12）

**依赖 Stories:**
- STORY-002（登录功能）

**相关 API:**
- `POST /api/v1/auth/send-code` - 发送验证码
- `POST /api/v1/auth/register` - 注册

---

### STORY-002

**所属 Epic:** EPIC-01
**标题:** 用户登录
**优先级:** P0
**故事点:** 5
**负责人:** @dev1
**状态:** TODO

**AS A** 已注册用户
**I WANT** 通过手机号+密码登录
**SO THAT** 使用系统功能

**Acceptance Criteria:**
- [ ] 可以通过手机号+密码登录
- [ ] 登录成功返回 JWT token
- [ ] 密码错误超过 5 次，锁定账号 30 分钟
- [ ] 可以记住登录状态（7 天有效）

**Technical Notes:**
- JWT token 有效期 1 小时
- Refresh token 有效期 7 天
- 登录失败次数记录在 Redis

**依赖 Stories:**
- None

**相关 API:**
- `POST /api/v1/auth/login` - 登录
- `POST /api/v1/auth/refresh` - 刷新 Token

---

### STORY-003

**所属 Epic:** EPIC-01
**标题:** 用户登出
**优先级:** P0
**故事点:** 2
**负责人:** @dev2
**状态:** TODO

**AS A** 已登录用户
**I WANT** 退出登录
**SO THAT** 清除登录状态，保护账号安全

**Acceptance Criteria:**
- [ ] 退出登录后 Token 失效
- [ ] 退出登录后跳转到登录页
- [ ] 清除本地存储的 Token

**Technical Notes:**
- 将 Token 加入黑名单（Redis）

**依赖 Stories:**
- STORY-002（登录功能）

**相关 API:**
- `POST /api/v1/auth/logout` - 登出

---

## Story 拆分原则

### 垂直拆分（推荐）
按照用户价值拆分，每个 Story 交付一个完整的用户功能。

### 水平拆分（谨慎）
按照技术层拆分（API / Service / DB），仅在团队并行开发时使用。

### 拆分检查清单
```
□ 每个 Story 可以在 1-3 天内完成
□ 每个 Story 有明确的验收标准
□ 每个 Story 独立可测试
□ Story 之间无循环依赖
□ Story 有清晰的价值交付
```

---

## 故事点估算标准

| 故事点 | 复杂度 | 工作量 | 示例 |
|--------|--------|--------|------|
| 1 | 非常简单 | 0.5 天 | 简单的文案修改 |
| 2 | 简单 | 1 天 | 单个 API CRUD |
| 3 | 中等 | 2 天 | 简单的表单+验证 |
| 5 | 较复杂 | 3-4 天 | 复杂业务逻辑/多个 API |
| 8 | 复杂 | 5-7 天 | 需要设计决策/多方集成 |
| 13 | 非常复杂 | 1-2 周 | 全新模块/高风险 |

---

## 优先级定义

| 优先级 | 定义 | 交付要求 |
|--------|------|----------|
| P0 | 核心功能，不上线无法用 | 必须 Sprint 1 完成 |
| P1 | 重要功能，影响核心体验 | Sprint 2 完成 |
| P2 | 增强功能，优化体验 | 后续迭代 |

---

## 状态定义

| 状态 | 含义 |
|------|------|
| TODO | 未开始 |
| IN_PROGRESS | 开发中 |
| CODE_REVIEW | Code Review 中 |
| TESTING | 测试中 |
| DONE | 完成 |
| BLOCKED | 被阻塞 |

---

## 依赖关系图

```
STORY-001 (注册) ──依赖──> STORY-002 (登录)
      │
      └── 不依赖

STORY-004 (下单) ──依赖──> STORY-005 (支付)
      │
      └── 依赖 ──> STORY-006 (购物车)
```

---

## 技术债务

| Story ID | 技术债务描述 | 影响 | 修复建议 | 优先级 |
|----------|-------------|------|----------|--------|
| - | 缺少 refresh token 机制 | 安全风险 | STORY-XXX 增加 refresh token | HIGH |
| - | 没有统一的错误处理 | 维护困难 | STORY-XXX 重构 error middleware | MEDIUM |
