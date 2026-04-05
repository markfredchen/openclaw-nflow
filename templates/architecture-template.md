# Architecture Document: [项目名称]

**版本:** v1.0
**日期:** YYYY-MM-DD
**状态:** DRAFT | IN_REVIEW | APPROVED
**负责人:** Architect Agent

---

## 1. Overview

[2-3段描述系统整体架构和设计理念]

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  [Web App]  [Mobile App]  [Admin Portal]                   │
└────────────────────────┬──────────────────────────────────┘
                         │ HTTPS / REST / GraphQL
┌────────────────────────▼──────────────────────────────────┐
│                       API Gateway                            │
│  [Auth] [Rate Limit] [Load Balancer]                       │
└────┬───────────────┬────────────────────┬───────────────────┘
     │               │                    │
┌────▼────┐   ┌──────▼──────┐   ┌────────▼────────┐
│ Service │   │   Service   │   │    Service      │
│   A     │   │     B       │   │      C         │
└────┬────┘   └──────┬──────┘   └────────┬────────┘
     │               │                    │
     └───────────────┼────────────────────┘
                     │
         ┌───────────▼───────────┐
         │     Message Queue    │
         │  [Kafka / RabbitMQ]  │
         └───────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐     ┌─────▼─────┐    ┌─────▼─────┐
│ Cache │     │ Database  │    │  Search   │
│ Redis │     │  Postgres  │    │ Elasticsearch│
└───────┘     └───────────┘    └───────────┘
```

---

## 3. System Components

### 3.1 Frontend Layer

| 组件 | 技术栈 | 职责 | 部署 |
|------|--------|------|------|
| Web App | React / Vue | 用户界面 | CDN |
| Mobile | React Native / Flutter | 移动端 | App Store |
| Admin | React + Ant Design | 管理后台 | ECS |

### 3.2 API Gateway

| 功能 | 实现 | 说明 |
|------|------|------|
| 认证 | JWT / OAuth2 | 统一鉴权 |
| 限流 | Redis + Token Bucket | 防刷 |
| 路由 | Nginx / Kong | 动态路由 |

### 3.3 Backend Services

| 服务 | 职责 | 技术栈 | 团队 |
|------|------|--------|------|
| Auth Service | 用户认证/授权 | Node.js | @team-a |
| Order Service | 订单管理 | Go | @team-b |
| Payment Service | 支付处理 | Python | @team-c |
| Notification | 消息通知 | Node.js | @team-a |

### 3.4 Data Layer

| 组件 | 用途 | 规格 |
|------|------|------|
| PostgreSQL | 主数据库 | 主从复制 |
| Redis | 缓存/Session | Cluster 模式 |
| Elasticsearch | 搜索 | 3节点集群 |
| Kafka | 消息队列 | 3 Broker |

---

## 4. Data Model

### 4.1 ER Diagram Overview

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │────<│  Order  │────<│ OrderItem│
└─────────┘     └─────────┘     └─────────┘
     │               │
     │               │
     ▼               ▼
┌─────────┐     ┌─────────┐
│ Address │     │ Payment │
└─────────┘     └─────────┘
```

### 4.2 Core Entities

#### User
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| email | VARCHAR(255) | 唯一邮箱 |
| password_hash | VARCHAR(255) | 加密密码 |
| created_at | TIMESTAMP | 创建时间 |

#### Order
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | UUID | 外键→User |
| status | ENUM | pending/paid/shipped |
| total_amount | DECIMAL | 总金额 |

---

## 5. API Design

### 5.1 API Style

- **REST** with JSON
- **Versioning:** `/api/v1/`
- **Authentication:** Bearer Token (JWT)

### 5.2 Core APIs

#### Auth APIs
```
POST   /api/v1/auth/register    注册
POST   /api/v1/auth/login      登录
POST   /api/v1/auth/refresh    刷新Token
POST   /api/v1/auth/logout     登出
```

#### Order APIs
```
GET    /api/v1/orders          订单列表
POST   /api/v1/orders          创建订单
GET    /api/v1/orders/:id      订单详情
PUT    /api/v1/orders/:id      更新订单
DELETE /api/v1/orders/:id      取消订单
```

### 5.3 Error Response Format

```json
{
  "code": 40001,
  "message": "参数错误",
  "data": null
}
```

| HTTP Status | Code Range | 说明 |
|-------------|------------|------|
| 400 | 40000-49999 | 客户端错误 |
| 401 | 40100 | 未认证 |
| 403 | 40300 | 无权限 |
| 500 | 50000 | 服务器错误 |

---

## 6. Security Architecture

### 6.1 Authentication Flow

```
[Client] → [API Gateway] → [Auth Service] → [JWT] → [Resource]
                ↑                                      ↓
                └─────────── [Refresh] ───────────────┘
```

### 6.2 Security Measures

| 安全措施 | 实现 |
|----------|------|
| 传输加密 | HTTPS (TLS 1.3) |
| 密码存储 | bcrypt (cost=12) |
| Token | JWT (RS256), 1h expiry |
| 防注入 | Parameterized Query |
| CORS | 白名单控制 |

---

## 7. Deployment Architecture

### 7.1 Environments

| 环境 | 用途 | 部署方式 |
|------|------|----------|
| Dev | 开发测试 | Docker Compose |
| Staging | 预发布 | Kubernetes |
| Prod | 生产 | Kubernetes (Multi-AZ) |

### 7.2 Infrastructure

```yaml
# Kubernetes Deployment (示例)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
```

---

## 8. Observability

### 8.1 Monitoring
- **Metrics:** Prometheus + Grafana
- **Tracing:** Jaeger
- **Logging:** ELK Stack

### 8.2 SLOs

| Service | Availability | Latency (p99) |
|---------|--------------|---------------|
| API Gateway | 99.95% | < 100ms |
| Auth Service | 99.9% | < 50ms |
| Order Service | 99.9% | < 200ms |

---

## 9. Architecture Decision Records

### ADR-001: 选择微服务 vs Monolith

**Status:** Accepted

**Context:** 需要快速迭代，但团队只有5人

**Decision:** 初期 Monolith，后续按需拆分为微服务

**Consequences:**
- Positive: 快速交付，运维简单
- Negative: 未来可能需要重构

---

## 10. Tech Stack Summary

| Layer | Technology |
|-------|------------|
| Frontend | React 18, TypeScript, TailwindCSS |
| Backend | Go, Node.js |
| Database | PostgreSQL 15, Redis 7 |
| Queue | Kafka |
| Search | Elasticsearch |
| Cache | Redis Cluster |
| CI/CD | GitHub Actions, ArgoCD |
| Cloud | AWS (ECS, RDS, ElastiCache) |
