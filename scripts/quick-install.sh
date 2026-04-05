#!/bin/bash
# quick-install.sh
# 一键安装 NFlow 到项目
#
# 用法:
#   curl -sSL https://raw.githubusercontent.com/markfredchen/openclaw-nflow/main/scripts/quick-install.sh | bash
#   ./scripts/quick-install.sh /path/to/project

set -e

PROJECT_PATH="${1:-$HOME/projects/my-nflow-project}"

echo "🚀 NFlow 一键安装"
echo "=================="
echo ""

# 1. 创建项目目录
echo "📁 创建项目目录: $PROJECT_PATH"
mkdir -p "$PROJECT_PATH"
cd "$PROJECT_PATH"

# 2. 克隆 NFlow
echo "📦 克隆 NFlow..."
if [ -d ".nflow" ]; then
    echo "   NFlow 已存在，跳过克隆"
else
    git clone https://github.com/markfredchen/openclaw-nflow.git .nflow
fi

# 3. 链接到 OpenClaw skills
echo "🔗 链接到 OpenClaw..."
mkdir -p "$HOME/.openclaw/skills"
ln -sfn "$(pwd)/.nflow" "$HOME/.openclaw/skills/nflow"

# 4. 创建示例项目结构
echo "📂 创建项目结构..."
mkdir -p docs design/wireframes design/mockups sprints/backlog sprints/sprint-01

# 5. 创建通知配置
echo "⚙️  配置通知渠道..."
mkdir -p .nflow
cat > .nflow/notify-config.json << 'EOF'
{
    "channel": "telegram",
    "target": "YOUR_CHAT_ID",
    "enabled": false,
    "notify_on": {
        "phase_complete": true,
        "story_complete": true,
        "review_required": true,
        "intervention_required": true,
        "sprint_complete": true
    }
}
EOF

# 6. 创建 project-state.json
cat > .nflow/project-state.json << 'EOF'
{
    "phase": 0,
    "complexity": "L2",
    "workflow": "nflow",
    "sprint": null,
    "last_command": null,
    "last_update": "2026-04-06"
}
EOF

echo ""
echo "✅ 安装完成！"
echo ""
echo "📁 项目: $PROJECT_PATH"
echo "🔗 NFlow: $HOME/.openclaw/skills/nflow"
echo ""
echo "📋 下一步:"
echo "   1. 编辑 .nflow/notify-config.json 设置通知渠道"
echo "   2. 运行 /nflow-init 开始项目初始化"
echo ""
echo "📚 NFlow 命令:"
echo "   /nflow-init          - 项目初始化"
echo "   /nflow-requirements - 需求定义"
echo "   /nflow-design       - 设计"
echo "   /nflow-dev          - 开发循环"
echo ""
