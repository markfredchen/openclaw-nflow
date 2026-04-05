#!/bin/bash
# quick-install.sh
# 一键安装 NFlow 到项目
#
# 用法:
#   curl -sSL https://raw.githubusercontent.com/markfredchen/openclaw-nflow/main/scripts/quick-install.sh | bash
#   curl -sSL https://raw.githubusercontent.com/markfredchen/openclaw-nflow/main/scripts/quick-install.sh | bash -s -- --target claude-code
#   ./scripts/quick-install.sh /path/to/project --target openclaw
#
# 选项:
#   --target <target>   安装目标: openclaw (默认), claude-code, codex
#   --path <path>      项目路径（可选）

set -e

TARGET="openclaw"
PROJECT_PATH=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --target)
            TARGET="$2"
            shift 2
            ;;
        --path)
            PROJECT_PATH="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --target <target>   安装目标: openclaw (默认), claude-code, codex"
            echo "  --path <path>      项目路径"
            echo "  --help, -h         显示帮助"
            echo ""
            echo "Examples:"
            echo "  $0 --target openclaw"
            echo "  $0 --path /path/to/project --target claude-code"
            exit 0
            ;;
        *)
            # 第一个非选项参数作为项目路径
            if [[ -z "$PROJECT_PATH" && "$1" != -* ]]; then
                PROJECT_PATH="$1"
            fi
            shift
            ;;
    esac
done

# 默认项目路径
if [[ -z "$PROJECT_PATH" ]]; then
    PROJECT_PATH="$HOME/projects/nflow-project"
fi

echo "🚀 NFlow 一键安装"
echo "=================="
echo "目标: $TARGET"
echo "项目: $PROJECT_PATH"
echo ""

# 1. 创建项目目录
echo "📁 创建项目目录..."
mkdir -p "$PROJECT_PATH"
cd "$PROJECT_PATH"

# 2. 克隆 NFlow
echo "📦 克隆 NFlow..."
if [[ -d ".nflow" ]]; then
    echo "   NFlow 已存在，更新中..."
    cd .nflow && git pull origin main && cd ..
else
    git clone https://github.com/markfredchen/openclaw-nflow.git .nflow
fi

NFLOW_DIR="$(pwd)/.nflow"

# 3. 根据目标安装
install_openclaw() {
    echo "🔧 安装 OpenClaw 集成..."
    
    # 链接到 OpenClaw skills
    mkdir -p "$HOME/.openclaw/skills"
    ln -sfn "$NFLOW_DIR" "$HOME/.openclaw/skills/nflow"
    
    echo "   ✅ OpenClaw 集成安装完成"
    echo "   位置: $HOME/.openclaw/skills/nflow"
}

install_claude_code() {
    echo "🔧 安装 Claude Code 集成..."
    
    # 创建 .claude 目录
    mkdir -p "$PROJECT_PATH/.claude/skills"
    
    # 复制 NFlow skill
    cp -r "$NFLOW_DIR" "$PROJECT_PATH/.claude/skills/nflow"
    
    # 创建配置
    cat > "$PROJECT_PATH/.claude/config.json" << 'EOF'
{
    "skills": {
        "nflow": {
            "path": ".claude/skills/nflow"
        }
    }
}
EOF
    
    echo "   ✅ Claude Code 集成安装完成"
    echo "   位置: $PROJECT_PATH/.claude/skills/nflow"
}

install_codex() {
    echo "🔧 安装 Codex 集成..."
    
    # Codex 使用 OpenAI API，配置方式类似 Claude Code
    mkdir -p "$PROJECT_PATH/.codex/skills"
    cp -r "$NFLOW_DIR" "$PROJECT_PATH/.codex/skills/nflow"
    
    echo "   ✅ Codex 集成安装完成"
    echo "   位置: $PROJECT_PATH/.codex/skills/nflow"
}

# 执行安装
case "$TARGET" in
    openclaw)
        install_openclaw
        ;;
    claude-code)
        install_claude_code
        ;;
    codex)
        install_codex
        ;;
    *)
        echo "❌ 未知目标: $TARGET"
        echo "   支持: openclaw, claude-code, codex"
        exit 1
        ;;
esac

# 4. 创建项目结构
echo "📂 创建项目结构..."
mkdir -p docs design/wireframes design/mockups sprints/backlog sprints/sprint-01

# 5. 创建 NFlow 配置
echo "⚙️  配置 NFlow..."
mkdir -p .nflow-config

# 通知配置
cat > .nflow-config/notify-config.json << 'EOF'
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

# 项目状态
cat > .nflow-config/project-state.json << EOF
{
    "phase": 0,
    "complexity": "L2",
    "workflow": "nflow",
    "sprint": null,
    "last_command": null,
    "last_update": "$(date +%Y-%m-%d)"
}
EOF

echo ""
echo "✅ 安装完成！"
echo ""
echo "📁 项目: $PROJECT_PATH"
echo "🎯 目标: $TARGET"
echo ""
echo "📋 下一步:"
if [[ "$TARGET" == "openclaw" ]]; then
    echo "   1. 编辑 .nflow-config/notify-config.json 设置通知渠道"
    echo "   2. 运行 /nflow-init 开始项目初始化"
else
    echo "   1. 编辑 .nflow-config/notify-config.json 设置通知渠道"
    echo "   2. 使用 /nflow-init 开始项目初始化"
fi
echo ""
echo "📚 NFlow 命令:"
echo "   /nflow-init           - 项目初始化"
echo "   /nflow-requirements  - 需求定义"
echo "   /nflow-design        - 设计"
echo "   /nflow-dev           - 开发循环"
echo ""
