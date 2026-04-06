# /nflow-deploy

## 部署流程（独立流程）

**注意：** 部署是独立流程，不在 Sprint 内执行。

---

## 概述

部署分为两个独立阶段：

| 阶段 | 说明 | 时机 |
|------|------|------|
| 本地开发环境 | 开发人员本地调试环境搭建 | 项目启动时 / 人员加入时 |
| 生产环境部署 | 应用发布到生产环境 | Sprint 完成后 / 独立发布周期 |

---

## Part 1: 本地开发环境

### 执行者

DevOps Agent / Tech Lead

### 步骤

#### 1. 环境需求定义

**输出:** `deploy/local/environment-spec.md`

```markdown
# 本地开发环境规格

## 依赖服务
| 服务 | 版本 | 端口 | 说明 |
|------|------|------|------|
| PostgreSQL | 15 | 5432 | 主数据库 |
| Redis | 7 | 6379 | 缓存 |
| MinIO | latest | 9000 | 对象存储 |

## 环境变量
| 变量 | 示例值 | 说明 |
|------|--------|------|
| DATABASE_URL | postgresql://user:pass@localhost:5432/db | 数据库连接 |
| REDIS_URL | redis://localhost:6379 | Redis 连接 |
| API_BASE_URL | http://localhost:3000 | API 地址 |

## 启动命令
```bash
docker-compose up -d
npm run dev
```
```

#### 2. Docker Compose 配置

**输出:** `deploy/local/docker-compose.yml`

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin

volumes:
  postgres_data:
```

#### 3. 环境验证

**验证清单：**
- [ ] 数据库连接正常
- [ ] Redis 连接正常
- [ ] 应用启动无报错
- [ ] API 可访问（`curl localhost:3000/health`）

#### 4. 文档更新

- 开发环境 README 更新
- 新成员加入流程更新

---

## Part 2: 生产环境部署

### 执行者

DevOps Agent / Tech Lead / 运维团队

### 步骤

#### 1. 部署前检查

**检查清单：**

```
□ Sprint Review 已完成
□ 所有 Stories 已完成并测试
□ 代码已合并到 main/master
□ E2E 测试全部通过
□ 安全扫描已完成
□ 性能测试已完成（如适用）
□ 备份已创建
□ 回滚方案已准备
```

#### 2. 生产环境规格

**输出:** `deploy/production/environment-spec.md`

```markdown
# 生产环境规格

## 服务器
| 组件 | 规格 | 数量 |
|------|------|------|
| Web Server | 2C4G | 2 |
| API Server | 4C8G | 3 |
| Database | 8C16G | 1 |
| Redis | 2C4G | 2 |

## 域名配置
| 环境 | 域名 | 说明 |
|------|------|------|
| Production | api.example.com | 生产 API |
| Staging | staging-api.example.com | 预发布环境 |

## 环境变量（Secrets）
- DATABASE_URL
- REDIS_URL
- JWT_SECRET
- API Keys
```

#### 3. CI/CD 流水线

**输出:** `deploy/production/pipeline.yml`

**流水线阶段：**

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  BUILD  │ → │  TEST   │ → │ DEPLOY  │ → │VERIFY   │
│  编译   │    │  测试   │    │  部署   │    │  验证   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

**CI/CD 配置示例（GitHub Actions）：**

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build and push to Staging
        run: |
          docker build -t app:${{ github.sha }} .
          docker push registry.example.com/app:${{ github.sha }}
      
      - name: Deploy to Staging
        run: |
          kubectl set image deployment/app api=registry.example.com/app:${{ github.sha }}
          kubectl rollout status deployment/app

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
      - name: Deploy to Production
        run: |
          kubectl set image deployment/app api=registry.example.com/app:${{ github.sha }}
          kubectl rollout status deployment/app
```

#### 4. 部署执行

**步骤：**

1. **创建备份**
   ```bash
   # 数据库备份
   pg_dump -Fc app > backup_$(date +%Y%m%d).dump
   
   # 配置备份
   kubectl get configmap -o yaml > configmap_backup.yaml
   ```

2. **部署新版本**
   ```bash
   # 更新镜像
   kubectl set image deployment/app api=registry.example.com/app:v1.2.3
   
   # 监控滚动更新
   kubectl rollout status deployment/app
   ```

3. **验证部署**
   ```bash
   # 健康检查
   curl https://api.example.com/health
   
   # 冒烟测试
   curl https://api.example.com/api/v1/users
   ```

#### 5. 回滚方案

**触发条件：**
- 健康检查失败
- 错误率超过阈值
- 性能严重下降

**回滚命令：**
```bash
# 回滚到上一版本
kubectl rollout undo deployment/app

# 回滚到指定版本
kubectl rollout undo deployment/app --to-revision=3
```

---

## 部署完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "本地环境就绪" \
    --status success \
    --message "本地开发环境已搭建完成，可以开始开发" \
    --screenshot "deploy/local/setup-complete.png"
```

```bash
python3 scripts/nflow_notify.py \
    --node "生产环境部署" \
    --status success \
    --message "v1.2.3 已部署到生产环境" \
    --screenshot "deploy/production/deploy-confirm.png"
```

---

## 部署文档结构

```
deploy/
├── local/
│   ├── docker-compose.yml
│   ├── environment-spec.md
│   └── setup-guide.md
├── staging/
│   ├── kubernetes/
│   │   ├── deployment.yml
│   │   ├── service.yml
│   │   └── ingress.yml
│   └── pipeline.yml
├── production/
│   ├── kubernetes/
│   │   ├── deployment.yml
│   │   ├── service.yml
│   │   ├── ingress.yml
│   │   └── hpa.yml
│   ├── pipeline.yml
│   └── environment-spec.md
└── README.md
```

---

## 部署检查清单

### 部署前
- [ ] Sprint Review 完成
- [ ] 所有 Stories DONE
- [ ] E2E 测试通过
- [ ] 安全扫描通过
- [ ] 性能测试通过（如需要）
- [ ] 备份已创建

### 部署后
- [ ] 健康检查通过
- [ ] 冒烟测试通过
- [ ] 监控指标正常
- [ ] 日志无 Error
- [ ] 用户反馈正常

### 回滚准备
- [ ] 回滚方案已文档化
- [ ] 回滚命令测试过
- [ ] 联系人列表更新

---

## 下一步

部署完成后，可以：
- 开始新的 Sprint 规划
- 进行下一个版本的开发
- 持续监控和优化

---

## 相关脚本

- `scripts/nflow_notify.py` - 部署通知
