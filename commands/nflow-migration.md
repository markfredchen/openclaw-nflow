# /nflow-migration

## 数据迁移流程（独立流程）

**注意：** 数据迁移是独立流程，通常与部署配合使用。

---

## 概述

数据迁移用于：
- 数据库 schema 变更
- 数据格式转换
- 历史数据处理
- 数据清洗

---

## 执行时机

| 时机 | 场景 |
|------|------|
| 部署前 | 迁移脚本先运行，新版本依赖新 schema |
| 部署后 | 数据回填、修复 |
| 独立触发 | 数据修复、清洗 |

---

## 执行步骤

### Step 1: 迁移分析

**输出:** `deploy/migrations/YYYYMMDD_description.md`

**分析内容：**

```markdown
# 迁移分析

**日期:** YYYY-MM-DD
**执行者:** DevOps / Tech Lead

## 迁移目的
- 描述为什么要做这次迁移

## 影响范围
- 影响的表/集合
- 影响的数据量
- 影响的用户

## 迁移类型
- [ ] Schema 变更
- [ ] 数据转换
- [ ] 数据清洗
- [ ] 数据回填

## 风险评估
| 风险 | 级别 | 影响 | 缓解措施 |
|------|------|------|----------|
| 数据丢失 | 高 | 用户数据丢失 | 先备份 |
| 服务中断 | 中 | 迁移期间不可用 | 使用蓝绿部署 |
| 回滚失败 | 低 | 无法回滚到旧版本 | 测试环境验证 |
```

---

### Step 2: 迁移脚本编写

**输出:** `deploy/migrations/YYYYMMDD_description/`

```
deploy/migrations/
├── 20260406_add_user_table/
│   ├── 001_up.sql           # 正向迁移
│   ├── 001_down.sql         # 回滚脚本
│   └── README.md            # 说明
```

**迁移脚本规范：**

```sql
-- 001_up.sql
BEGIN;

-- 创建新表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 数据迁移（从旧表到新表）
INSERT INTO users (email, created_at)
SELECT email, created_date FROM legacy_users WHERE status = 'active';

-- 创建索引
CREATE INDEX idx_users_email ON users(email);

COMMIT;
```

```sql
-- 001_down.sql
BEGIN;

DROP TABLE IF EXISTS users;

COMMIT;
```

---

### Step 3: 备份

**备份命令：**

```bash
# PostgreSQL
pg_dump -Fc app > backup_$(date +%Y%m%d_%H%M%S).dump

# MySQL
mysqldump -u root -p app > backup_$(date +%Y%m%d_%H%M%S).sql

# MongoDB
mongodump --db app --out backup_$(date +%Y%m%d)
```

**备份验证：**

```bash
# PostgreSQL
pg_restore --list backup_file.dump | head -20

# 验证备份完整性
pg_restore --dbname=app_test --dry-run backup_file.dump
```

---

### Step 4: 预演（Dry Run）

**在测试环境执行：**

```bash
# PostgreSQL
psql -f 001_up.sql --echo-queries

# 查看影响行数
SELECT count(*) FROM legacy_users WHERE status = 'active';
```

**检查清单：**
- [ ] 脚本语法正确
- [ ] 影响行数符合预期
- [ ] 执行时间可接受
- [ ] 锁等待时间可接受

---

### Step 5: 执行迁移

**生产环境执行：**

```bash
# 1. 进入维护模式（可选）
kubectl scale deployment app --replicas=0

# 2. 执行迁移
psql -f 001_up.sql --echo-queries

# 3. 验证迁移结果
psql -c "SELECT count(*) FROM users;"
psql -c "SELECT count(*) FROM legacy_users;"

# 4. 退出维护模式
kubectl scale deployment app --replicas=3
```

---

### Step 6: 验证

**验证清单：**

```markdown
## 迁移验证

### 数据完整性
- [ ] 新表记录数 = 预期记录数
- [ ] 旧表数据已正确迁移
- [ ] 索引已创建
- [ ] 外键关系正确

### 应用验证
- [ ] 应用启动正常
- [ ] API 响应正常
- [ ] 读写操作正常

### 日志检查
- [ ] 无错误日志
- [ ] 无警告日志
```

---

### Step 7: 回滚（如需要）

**回滚命令：**

```bash
# 执行回滚脚本
psql -f 001_down.sql --echo-queries

# 验证回滚
psql -c "SELECT count(*) FROM users;"  # 应该为 0
```

**回滚后检查：**
- [ ] 旧表数据完整
- [ ] 应用正常回滚到旧版本
- [ ] 服务恢复

---

## 迁移通知

```bash
# 迁移开始
python3 scripts/nflow_notify.py \
    --node "数据迁移" \
    --status pending \
    --message "开始执行数据迁移：添加 users 表，预计影响 10000 条记录"

# 迁移完成
python3 scripts/nflow_notify.py \
    --node "数据迁移" \
    --status success \
    --message "数据迁移完成：users 表已创建，10000 条记录已迁移"

# 迁移失败
python3 scripts/nflow_notify.py \
    --node "数据迁移" \
    --status failure \
    --message "数据迁移失败：需要人工介入检查"
```

---

## 迁移文档结构

```
deploy/migrations/
├── README.md                      # 迁移总览
├── 20260406_add_user_table/
│   ├── 001_up.sql               # 正向迁移
│   ├── 001_down.sql             # 回滚脚本
│   ├── validation.sql            # 验证脚本
│   └── README.md                 # 说明
├── 20260415_rename_columns/
│   ├── 001_up.sql
│   ├── 001_down.sql
│   └── README.md
└── pending/                      # 待执行的迁移
```

---

## 迁移检查清单

### 迁移前
- [ ] 迁移分析已完成
- [ ] 迁移脚本已编写
- [ ] 测试环境已验证
- [ ] 备份已创建
- [ ] 回滚方案已准备
- [ ] 维护窗口已沟通

### 迁移后
- [ ] 数据完整性验证
- [ ] 应用功能验证
- [ ] 性能检查
- [ ] 监控告警检查
- [ ] 文档已更新

---

## 最佳实践

| 实践 | 说明 |
|------|------|
| 幂等脚本 | 多次执行结果一致 |
| 可回滚 | 必须有 down 脚本 |
| 小步迁移 | 大数据量分批处理 |
| 监控进度 | 大数据量迁移时监控进度 |
| 低峰期执行 | 避开业务高峰期 |

---

## 相关命令

| 命令 | 说明 |
|------|------|
| `/nflow-deploy` | 部署流程 |
| `/nflow-rollback` | 回滚流程（如需要） |
