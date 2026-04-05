# NFlow 通知系统

## 概述

NFlow 支持通过多种渠道发送开发节点通知，不仅仅是 Telegram。

---

## 通知配置

### 配置文件位置

项目根目录：`.nflow/notify-config.json`

### 配置格式

```json
{
    "channel": "telegram",
    "target": "7314529482",
    "enabled": true,
    "notify_on": {
        "phase_complete": true,
        "story_complete": true,
        "review_required": true,
        "intervention_required": true,
        "sprint_complete": true
    }
}
```

### 配置字段说明

| 字段 | 说明 | 可选值 |
|------|------|--------|
| channel | 通知渠道 | telegram, discord, slack, whatsapp, signal, imessage |
| target | 目标标识 | chat_id（Telegram）、channel_id（Discord）等 |
| enabled | 是否启用 | true, false |
| notify_on.* | 通知触发条件 | true, false |

### 支持的渠道

| 渠道 | target 格式 | 说明 |
|------|------------|------|
| telegram | Chat ID 或 @username | 即时通讯，默认配置 |
| discord | Channel ID | 需配置 Discord Bot |
| slack | Channel ID | 需配置 Slack App |
| whatsapp | Phone number | 需配置 WhatsApp Business |
| signal | Phone number | 需配置 Signal Gateway |
| imessage | Chat ID | macOS only |

---

## 通知脚本

**位置:** `scripts/nflow_notify.py`

### 基本用法

```bash
python3 scripts/nflow_notify.py \
    --node "节点名称" \
    --status success \
    --message "详情信息"
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--node` | 是 | 节点名称 |
| `--status` | 是 | success / failure / warning / pending |
| `--message` | 否 | 详细信息 |
| `--screenshot` | 否 | 截图路径 |
| `--story-id` | 否 | Story ID |
| `--sprint` | 否 | Sprint 名称 |
| `--config` | 否 | 配置文件路径（默认从项目加载） |
| `--dry-run` | 否 | 仅打印不发送 |
| `--list-channels` | 否 | 列出支持的渠道 |

### 状态说明

| 状态 | Emoji | 用途 |
|------|-------|------|
| success | ✅ | 节点成功完成 |
| failure | ❌ | 节点执行失败 |
| warning | ⚠️ | 节点有警告但继续 |
| pending | ⏳ | 节点等待中 |

---

## 在命令中集成

### Python 调用

```python
import subprocess

def notify(node, status, message, story_id=None, screenshot=None):
    cmd = [
        "python3", "scripts/nflow_notify.py",
        "--node", node,
        "--status", status,
        "--message", message
    ]
    if story_id:
        cmd.extend(["--story-id", story_id])
    if screenshot:
        cmd.extend(["--screenshot", screenshot])
    
    result = subprocess.run(cmd)
    return result.returncode == 0

# 使用
notify("TDD开发", "success", "RED→GREEN→REFACTOR 完成", "STORY-001")
```

### Shell 调用

```bash
#!/bin/bash
python3 scripts/nflow_notify.py \
    --node "节点名称" \
    --status success \
    --message "$message" \
    --story-id "$STORY_ID"
```

---

## 通知触发规则

通过 `notify_on` 配置控制通知触发：

```json
{
    "notify_on": {
        "phase_complete": true,      // Phase 完成后通知
        "story_complete": true,      // Story 完成时通知
        "review_required": true,      // 需要审核时通知
        "intervention_required": true, // 需要人工干预时通知（始终通知）
        "sprint_complete": true      // Sprint 完成时通知
    }
}
```

---

## 调试模式

```bash
# 列出支持的渠道
python3 scripts/nflow_notify.py --list-channels

# 干运行（不发送）
python3 scripts/nflow_notify.py \
    --node "测试" \
    --status success \
    --message "测试消息" \
    --dry-run
```

干运行输出示例：
```
=== 干运行 - 不发送 ===
渠道: telegram
目标: 7314529482
---
✅ **NFlow 开发节点报告**

**节点:** 测试
**状态:** SUCCESS
**时间:** 15:30:45

**详情:**
测试消息

---
_由 NFlow 自动发送_
```

---

## 项目初始化时配置

在 `/nflow-init` 过程中，会询问通知渠道：

```
通知发送到哪里？

当前已配置的渠道：
  1. Telegram (default) ✅

请选择通知渠道：
A. Telegram - 发送消息到 Telegram
B. Discord - 发送消息到 Discord
C. Slack - 发送消息到 Slack
D. 暂不启用 - 不发送通知
```

选择后会创建 `.nflow/notify-config.json` 配置文件。

---

## 迁移现有项目

如果已有项目，想启用通知：

1. 创建 `.nflow/` 目录
2. 创建 `notify-config.json`：
```json
{
    "channel": "telegram",
    "target": "你的chat_id",
    "enabled": true
}
```
3. 从现在起所有节点完成都会发送通知
