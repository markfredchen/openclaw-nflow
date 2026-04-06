#!/bin/bash
# quick-install.sh
# 一键安装 NFlow 到项目
#
# 用法:
#   curl -sSL https://raw.githubusercontent.com/markfredchen/openclaw-nflow/main/scripts/quick-install.sh | bash
#   curl -sSL https://raw.githubusercontent.com/markfredchen/openclaw-nflow/main/scripts/quick-install.sh | bash -s -- my-project
#   ./scripts/quick-install.sh /path/to/project --target openclaw
#
# 选项:
#   --target <target>   安装目标: openclaw, claude-code, codex（必须）
#   --path <path>      项目路径
#
# 示例:
#   $0 --target openclaw --path /path/to/project
#   $0 --target claude-code --path ~/my-app
#   $0 my-app            # 使用字符串作为目录名，在当前目录创建

set -e

TARGET=""
PROJECT_PATH=""
CURRENT_DIR="$(pwd)"

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
            echo "Usage: $0 [OPTIONS] [project-name]"
            echo ""
            echo "Options:"
            echo "  --target <target>   安装目标（必须）: openclaw, claude-code, codex"
            echo "  --path <path>      项目路径"
            echo "  --help, -h         显示帮助"
            echo ""
            echo "Examples:"
            echo "  $0 --target openclaw --path /path/to/project"
            echo "  $0 --target claude-code --path ~/my-app"
            echo "  $0 my-project       # 在当前目录创建 my-project 目录"
            exit 0
            ;;
        -*)
            echo "❌ 未知选项: $1"
            echo "   使用 --help 查看帮助"
            exit 1
            ;;
        *)
            # 非选项参数：如果是第一个且不是路径（不包含/），作为目录名
            if [[ -z "$PROJECT_PATH" && "$1" != -* ]]; then
                if [[ "$1" == *"/"* ]]; then
                    # 包含 /，当作路径
                    PROJECT_PATH="$1"
                else
                    # 不包含 /，当作目录名，在当前目录创建
                    PROJECT_PATH="$CURRENT_DIR/$1"
                fi
            fi
            shift
            ;;
    esac
done

# 1. 检查 target 是否提供
if [[ -z "$TARGET" ]]; then
    echo "❌ 错误: --target 参数必须提供"
    echo ""
    echo "用法: $0 --target <target> [--path <path>]"
    echo ""
    echo "支持的安装目标:"
    echo "  openclaw     - OpenClaw 全局安装"
    echo "  claude-code  - Claude Code 项目内安装"
    echo "  codex        - Codex 项目内安装"
    echo ""
    echo "示例:"
    echo "  $0 --target openclaw --path ~/my-project"
    echo "  $0 --target claude-code my-project"
    exit 1
fi

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

# 3. 如果没有提供 path，使用目录名作为项目名（默认当前目录下创建）
if [[ -z "$PROJECT_PATH" ]]; then
    PROJECT_PATH="$CURRENT_DIR/nflow-project"
    echo "⚠️  未指定项目路径，默认使用: $PROJECT_PATH"
fi

echo ""
echo "🚀 NFlow 一键安装"
echo "=================="
echo "目标: $TARGET"
echo "项目: $PROJECT_PATH"
echo ""

# 4. 创建项目目录
echo "📁 创建项目目录..."
mkdir -p "$PROJECT_PATH"

# 5. 如果 nflow 目录已存在，先删除
if [[ -d "$PROJECT_PATH/.nflow" ]]; then
    echo "🗑️  删除旧版 NFlow..."
    rm -rf "$PROJECT_PATH/.nflow"
fi

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

# 通知配置
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

# 项目状态
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
echo "   1. 编辑 .nflow/notify-config.json 设置通知渠道"
echo "   2. 运行 /nflow-init 开始项目初始化"
echo ""
echo "📚 NFlow 命令:"
echo "   /nflow-init           - 项目初始化"
echo "   /nflow-requirements  - 需求定义"
echo "   /nflow-design        - 设计"
echo "   /nflow-dev           - 开发循环"
echo ""
