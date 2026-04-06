#!/bin/bash
# quick-install.sh
# 一键安装 NFlow 到项目
#
# 用法:
#   curl -sSL https://raw.githubusercontent.com/markfredchen/openclaw-nflow/main/scripts/quick-install.sh | bash
#   curl -sSL https://raw.githubusercontent.com/markfredchen/openclaw-nflow/main/scripts/quick-install.sh | bash -s -- --target openclaw --path my-project
#   ./scripts/quick-install.sh --target claude-code --path my-app
#
# 选项:
#   --target <target>   安装目标（必须）: openclaw, claude-code, codex
#   --path <name>      项目名称，在当前目录下创建目录
#
# 示例:
#   $0 --target openclaw --path my-project     # 在当前目录创建 my-project/
#   $0 --target claude-code --path my-app      # 在当前目录创建 my-app/
#   $0 my-project                             # 等于 --path my-project（target 仍需单独指定）

set -e

TARGET="openclaw"
PROJECT_NAME=""
CURRENT_DIR="$(pwd)"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --target)
            TARGET="$2"
            shift 2
            ;;
        --path)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS] [project-name]"
            echo ""
            echo "Options:"
            echo "  --target <target>   安装目标（默认 openclaw）: openclaw, claude-code, codex"
            echo "  --path <name>      项目名称（必须），在当前目录下创建目录"
            echo "  --help, -h         显示帮助"
            echo ""
            echo "Examples:"
            echo "  $0 --path my-project                # 默认 openclaw"
            echo "  $0 --target claude-code --path my-app"
            echo "  $0 --target codex my-project"
            exit 0
            ;;
        -*)
            echo "❌ 未知选项: $1"
            echo "   使用 --help 查看帮助"
            exit 1
            ;;
        *)
            # 第一个非选项参数作为项目名称
            if [[ -z "$PROJECT_NAME" && "$1" != -* ]]; then
                PROJECT_NAME="$1"
            fi
            shift
            ;;
    esac
done

# 1. target 默认为 openclaw，无需检查

# 2. 验证 target 有效性
case "$TARGET" in
    openclaw|claude-code|codex)
        ;;
    *)
        echo "❌ 未知目标: $TARGET"
        echo "   支持: openclaw, claude-code, codex"
        exit 1
        ;;
esac

# 3. 项目名称处理
if [[ -z "$PROJECT_NAME" ]]; then
    echo "❌ 错误: --path 参数必须提供"
    echo ""
    echo "用法: $0 --target <target> --path <project-name>"
    echo ""
    echo "示例:"
    echo "  $0 --target openclaw --path my-project"
    exit 1
fi

# 项目路径：在当前目录下创建
PROJECT_PATH="$CURRENT_DIR/$PROJECT_NAME"

echo ""
echo "🚀 NFlow 一键安装"
echo "=================="
echo "目标: $TARGET"
echo "项目: $PROJECT_NAME"
echo "路径: $PROJECT_PATH"
echo ""

# 4. 如果项目目录已存在，先删除
if [[ -d "$PROJECT_PATH" ]]; then
    echo "🗑️  删除旧项目目录..."
    rm -rf "$PROJECT_PATH"
fi

# 5. 创建项目目录
echo "📁 创建项目目录..."
mkdir -p "$PROJECT_PATH"

# 6. 克隆 NFlow
echo "📦 克隆 NFlow..."
git clone https://github.com/markfredchen/openclaw-nflow.git "$PROJECT_PATH/.nflow"

NFLOW_DIR="$PROJECT_PATH/.nflow"

# 7. 根据目标安装
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
    
    mkdir -p "$PROJECT_PATH/.claude/skills"
    cp -r "$NFLOW_DIR" "$PROJECT_PATH/.claude/skills/nflow"
    
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
esac

# 8. 创建项目结构
echo "📂 创建项目结构..."
mkdir -p "$PROJECT_PATH/nflow-docs/docs"
mkdir -p "$PROJECT_PATH/nflow-docs/design/wireframes"
mkdir -p "$PROJECT_PATH/nflow-docs/design/mockups"
mkdir -p "$PROJECT_PATH/nflow-docs/sprints/backlog"
mkdir -p "$PROJECT_PATH/nflow-docs/sprints/sprint-01"
mkdir -p "$PROJECT_PATH/deploy/local"
mkdir -p "$PROJECT_PATH/deploy/staging"
mkdir -p "$PROJECT_PATH/deploy/production"
mkdir -p "$PROJECT_PATH/deploy/migrations"

# 9. 创建 NFlow 配置
echo "⚙️  配置 NFlow..."
mkdir -p "$PROJECT_PATH/.nflow"

cat > "$PROJECT_PATH/.nflow/notify-config.json" << 'EOF'
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

cat > "$PROJECT_PATH/.nflow/project-state.json" << EOF
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
echo "   1. cd $PROJECT_NAME"
echo "   2. 编辑 .nflow/notify-config.json 设置通知渠道"
echo "   3. 运行 /nflow-init 开始项目初始化"
echo ""
echo "📚 NFlow 命令:"
echo "   /nflow-init           - 项目初始化"
echo "   /nflow-requirements  - 需求定义"
echo "   /nflow-design        - 设计"
echo "   /nflow-dev           - 开发循环"
echo ""
