# /nflow-dev-tdd

## TDD 开发流程

**Phase:** Phase 8.5

**执行 Agent:** Developer Agent

---

## 通知机制

TDD 每个阶段完成后发送通知：
- RED 阶段完成
- GREEN 阶段完成
- REFACTOR 阶段完成
- 最终 TDD 循环完成

---

## TDD 循环

```
RED → GREEN → REFACTOR

1. RED:     编写一个失败的测试
2. GREEN:   编写最少量代码让测试通过
3. REFACTOR: 重构代码，消除重复
```

---

## RED - 编写失败的测试

### 步骤

1. **理解 Story 的 Acceptance Criteria**
2. **阅读 architecture.md 了解接口设计**
3. **编写单元测试**
   - 测试应该描述期望的行为
   - 不需要实现代码，测试应该失败

### RED 阶段通知

```bash
python3 scripts/nflow_notify.py \
    --node "TDD-RED" \
    --status success \
    --message "RED 阶段完成：已编写 5 个失败测试，等待 GREEN 阶段实现" \
    --story-id STORY-001 \
    --sprint sprint-01
```

### 示例

```python
# test_user_registration.py

def test_user_can_register_with_email():
    # RED: 测试应该失败，因为功能还没实现
    user = register_user(email="test@example.com")
    assert user.email == "test@example.com"
    assert user.is_verified == False
```

---

## GREEN - 让测试通过

### 步骤

1. **编写最少量代码**
   - 不要过度设计
   - 只让测试通过即可

2. **运行测试**
   - 确认测试通过

### GREEN 阶段通知

```bash
python3 scripts/nflow_notify.py \
    --node "TDD-GREEN" \
    --status success \
    --message "GREEN 阶段完成：所有测试通过，最小化实现完成" \
    --story-id STORY-001 \
    --sprint sprint-01
```

### 示例

```python
# user.py

class User:
    def __init__(self, email):
        self.email = email
        self.is_verified = False

def register_user(email):
    return User(email=email)
```

---

## REFACTOR - 重构

### 步骤

1. **改进代码结构**
   - 消除重复代码
   - 提高可读性
   - 保持测试通过

2. **确保测试仍然通过**

### REFACTOR 阶段通知

```bash
python3 scripts/nflow_notify.py \
    --node "TDD-REFACTOR" \
    --status success \
    --message "REFACTOR 阶段完成：代码重构完成，测试覆盖率 85%" \
    --screenshot "sprints/sprint-01/coverage-report.png" \
    --story-id STORY-001 \
    --sprint sprint-01
```

---

## TDD 最终完成通知

```bash
python3 scripts/nflow_notify.py \
    --node "TDD开发" \
    --status success \
    --message "TDD 循环完成：RED→GREEN→REFACTOR，代码覆盖率 85%" \
    --screenshot "sprints/sprint-01/coverage-report.png" \
    --story-id STORY-001 \
    --sprint sprint-01
```

---

## TDD 规则

| 规则 | 说明 |
|------|------|
| 每个新功能必须先写测试 | 没有测试的代码不允许提交 |
| 测试必须独立 | 不依赖其他测试的状态 |
| 测试必须可重复 | 每次运行结果一致 |
| 测试必须有意义 | 测试行为，不测试实现 |

---

## 失败处理

```
测试失败
    ↓
分析失败原因
    ↓
是代码问题？
    ├── 是 → 修复代码
    └── 否 → 修复测试
    ↓
重新运行测试
    ↓
通过？
    ├── 是 → 继续下一个测试
    └── 否 → 继续修复
```

**失败通知：**
```bash
python3 scripts/nflow_notify.py \
    --node "TDD测试" \
    --status failure \
    --message "测试失败: test_user_registration，请查看截图" \
    --screenshot "sprints/sprint-01/test-reports/failure-001.png" \
    --story-id STORY-001
```

---

## 测试覆盖率

- 新代码必须有测试覆盖
- 目标覆盖率 > 80%
- 使用工具检查覆盖率

---

## 相关文件

- `sprints/sprint-XX/implementations/` - 实现代码
- `sprints/sprint-XX/test-reports/` - 测试报告
- `scripts/nflow_notify.py` - Telegram 通知脚本
