#!/bin/bash
# install-openclaw.sh
# Install NFlow to OpenClaw
#
# Usage:
#   ./install-openclaw.sh --mode agent    # Agent 模式（独立 workspace）
#   ./install-openclaw.sh --mode subagent # Subagent 模式（spawn 方式）
#   ./install-openclaw.sh                 # 默认 agent 模式

set -e

INSTALL_MODE="agent"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            INSTALL_MODE="$2"
            shift 2
            ;;
        --help|-h)
            INSTALL_MODE="help"
            shift
            ;;
        *)
            shift
            ;;
    esac
done

if [[ "$INSTALL_MODE" == "help" ]]; then
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --mode agent     Agent 模式（默认）"
    echo "                    每个 Agent 是独立进程，拥有独立 workspace"
    echo "                    适用于复杂项目，需要强隔离"
    echo "  --mode subagent  Subagent 模式"
    echo "                    使用 spawn 方式启动 Agent"
    echo "                    适用于轻量级协作，共享上下文"
    echo "  --help, -h       显示帮助"
    echo ""
    echo "Examples:"
    echo "  $0 --mode agent"
    echo "  $0 --mode subagent"
    exit 0
fi

echo "Installing NFlow for OpenClaw..."
echo "Mode: $INSTALL_MODE"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Create OpenClaw skills directory
OPENCLAW_SKILLS_DIR="$HOME/.openclaw/skills/nflow"
mkdir -p "$OPENCLAW_SKILLS_DIR"

# Copy skill files
cp -r "$SKILL_DIR"/* "$OPENCLAW_SKILLS_DIR/"

# Generate mode configuration
cat > "$OPENCLAW_SKILLS_DIR/.nflow-mode" << EOF
$INSTALL_MODE
EOF

echo ""
echo "✅ NFlow 安装完成！"
echo ""
echo "📁 安装位置: $OPENCLAW_SKILLS_DIR"
echo "⚙️  运行模式: $INSTALL_MODE"
echo ""
echo "📋 可用命令:"
echo "   /nflow-init          - 项目初始化"
echo "   /nflow-requirements  - 需求定义"
echo "   /nflow-design        - 设计"
echo "   /nflow-prototype    - 原型"
echo "   /nflow-plan         - Backlog + Sprint"
echo "   /nflow-dev          - 开发循环"
echo "   /nflow-resume       - 恢复循环"
echo "   /nflow-story        - 单个 Story"
echo "   /nflow-review       - 最终评审"
echo "   /nflow-new-spec     - 新需求/Bug"
echo ""
echo "🚀 开始使用:"
echo "   /nflow-init"
