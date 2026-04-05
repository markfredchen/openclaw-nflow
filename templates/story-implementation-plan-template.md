# User Story Implementation Plan

**Story ID:** STORY-001
**Story 名称:** 用户注册
**Epic:** EPIC-01 用户模块
**Sprint:** Sprint 01
**负责人:** @dev1
**创建日期:** YYYY-MM-DD

---

## 1. 需求收集

### 1.1 Story 信息

```markdown
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
```

### 1.2 技术设计（来自 architecture.md）

```markdown
**API 端点:**
- POST /api/v1/auth/send-code — 发送验证码
- POST /api/v1/auth/register — 注册

**数据模型:**
- users 表: id, phone, password_hash, created_at, updated_at

**技术栈:**
- Backend: Node.js + Express
- Database: PostgreSQL
- Cache: Redis（验证码存储）
- Auth: JWT
```

### 1.3 设计规范（来自 design-pattern.json）

```markdown
**颜色:**
- Primary: #1890FF
- Error: #FF4D4F

**按钮尺寸:**
- Large: 40px 高
- Medium: 32px 高

**间距:**
- 页面边距: 16px (Mobile)
- 组件间距: 12px
```

---

## 2. 任务拆分

| 任务 | 类型 | 预估时间 | 依赖 |
|------|------|----------|------|
| 创建数据库迁移 | DB | 1h | - |
| 实现 send-code API | Backend | 2h | Redis |
| 实现 register API | Backend | 3h | DB, send-code |
| 编写单元测试 | Test | 2h | APIs |
| 前端注册表单 | Frontend | 3h | API 契约 |
| 前端验证码倒计时 | Frontend | 1h | - |
| E2E 测试 | Test | 2h | 前后端 |
| **总计** | | **14h** | |

---

## 3. Git Worktree

```bash
# 创建 worktree
git fetch origin
git worktree add ../worktrees/story-001-user-registration feature/story-001

# 分支信息
git checkout -b feat/story-001-user-registration
```

---

## 4. 实现步骤

### Step 1: 数据库迁移

```sql
-- migrations/001_create_users_table.sql
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  phone VARCHAR(20) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_phone ON users(phone);
```

### Step 2: 后端 API 实现

**Redis 验证码存储:**
```
Key: sms:verify:{phone}
Value: {code: "123456", expires_at: timestamp}
TTL: 300 seconds
```

**API: POST /api/v1/auth/send-code**
- Request: `{ "phone": "+8613800138000" }`
- Response: `{ "success": true, "expires_in": 300 }`
- 生成6位验证码，存储到 Redis，TTL 5分钟

**API: POST /api/v1/auth/register**
- Request: `{ "phone": "+8613800138000", "code": "123456", "password": "SecurePass123" }`
- Response: `{ "success": true, "token": "eyJhbGciOiJIUzI1NiIs..." }`
- 验证验证码，检查手机号唯一性，bcrypt 加密密码，创建用户，生成 JWT

### Step 3: 前端实现

**注册页面流程:**
```
用户输入手机号 → 点击获取验证码 → 60秒倒计时 → 输入验证码和密码 → 提交注册 → 自动登录 → 跳转首页
```

**组件结构:**
```
pages/RegisterPage/
├── RegisterPage.tsx        # 主页面
├── PhoneInput.tsx          # 手机号输入
├── VerifyCodeInput.tsx     # 验证码输入（带倒计时）
├── PasswordInput.tsx       # 密码输入（强度指示）
└── RegisterForm.tsx        # 表单容器
```

---

## 5. 测试计划

### 5.1 单元测试

| 模块 | 测试用例 | 状态 |
|------|----------|------|
| sendCode API | 有效手机号返回成功 | ⏳ TODO |
| sendCode API | 60秒内重复请求返回错误 | ⏳ TODO |
| register API | 正确验证码和密码注册成功 | ⏳ TODO |
| register API | 错误验证码返回失败 | ⏳ TODO |
| register API | 重复手机号返回错误 | ⏳ TODO |
| register API | 弱密码返回错误 | ⏳ TODO |

### 5.2 E2E 测试

```typescript
// e2e/auth.spec.ts
test('用户注册流程', async ({ page }) => {
  await page.goto('/register');
  
  // 输入手机号
  await page.fill('[data-testid=phone-input]', '+8613800138000');
  await page.click('[data-testid=send-code-btn]');
  
  // 验证倒计时显示
  await expect(page.locator('[data-testid=countdown]')).toContainText('60');
  
  // 输入验证码（mock SMS API）
  await page.fill('[data-testid=verify-code-input]', '123456');
  
  // 输入密码
  await page.fill('[data-testid=password-input]', 'SecurePass123');
  
  // 提交
  await page.click('[data-testid=register-btn]');
  
  // 验证跳转首页
  await expect(page).toHaveURL('/home');
});
```

---

## 6. 状态追踪

| 步骤 | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 数据库迁移 | ✅ DONE | 04/01 | |
| send-code API | ✅ DONE | 04/01 | |
| register API | 🔄 IN_PROGRESS | - | |
| 单元测试 | ⏳ TODO | - | |
| 前端注册表单 | ⏳ TODO | - | |
| E2E 测试 | ⏳ TODO | - | |
| Code Review | ⏳ TODO | - | |
| 合并到 main | ⏳ TODO | - | |

---

## 7. Code Review 检查清单

- [ ] API 符合 architecture.md 设计
- [ ] 数据库索引已创建
- [ ] 密码使用 bcrypt 加密（cost=12）
- [ ] 验证码存储在 Redis，TTL 5分钟
- [ ] JWT token 生成正确
- [ ] 单元测试覆盖率 > 80%
- [ ] 所有测试通过
- [ ] 无安全漏洞（注入/越权/弱密码）
- [ ] 遵循 design-pattern.json

---

**最后更新:** YYYY-MM-DD HH:mm
