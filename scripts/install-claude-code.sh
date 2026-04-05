#!/bin/bash
# install-claude-code.sh
# Install NFlow for Claude Code
#
# Usage:
#   ./install-claude-code.sh --local [path]  # 安装到项目目录，默认当前目录
#   ./install-claude-code.sh --global        # 全局安装
#   ./install-claude-code.sh                 # 默认安装到当前目录

set -e

INSTALL_MODE="local"
TARGET_PROJECT="$(pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --local)
            INSTALL_MODE="local"
            # 如果下一个参数不是 flag，则是路径
            if [[ -n "$2" && "$2" != --* ]]; then
                TARGET_PROJECT="$2"
                shift
            fi
            shift
            ;;
        --global)
            INSTALL_MODE="global"
            shift
            ;;
        --help|-h)
            INSTALL_MODE="help"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Show help
if [[ "$INSTALL_MODE" == "help" ]]; then
    echo "Usage: $0 [OPTIONS] [path]"
    echo ""
    echo "Options:"
    echo "  --local [path]   安装到项目目录（默认: 当前目录）"
    echo "                    示例: $0 --local ~/my-project"
    echo "                         $0 --local"
    echo "  --global          全局安装（默认: ~/.claude/skills/）"
    echo "  --help, -h       显示此帮助"
    echo ""
    echo "Examples:"
    echo "  $0                      # 安装到当前目录"
    echo "  $0 --local              # 安装到当前目录"
    echo "  $0 --local ~/my-project # 安装到指定目录"
    echo "  $0 --global             # 全局安装"
    exit 0
fi

# Get current script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Global install
if [[ "$INSTALL_MODE" == "global" ]]; then
    echo "Installing NFlow for Claude Code (Global)..."
    
    SKILLS_DIR="$HOME/.claude/skills"
    SKILL_PATH="$SKILLS_DIR/nflow"
    mkdir -p "$SKILLS_DIR"
    
    echo "📁 全局安装目录: $SKILL_PATH"
    
    # Copy skill files to ~/.claude/skills/nflow/
    rm -rf "$SKILL_PATH"
    cp -r "$SKILL_DIR" "$SKILL_PATH/"
    
    echo ""
    echo "✅ 全局安装完成！"
    echo ""
    echo "📁 安装位置："
    echo "   $SKILL_PATH/"
    echo ""
    echo "🚀 开始使用："
    echo "   /nflow-init"
    exit 0
fi

# Local install
echo "Installing NFlow for Claude Code (Local)..."
echo "📁 项目目录: $TARGET_PROJECT"

# Project skills directory
PROJECT_SKILLS_DIR="$TARGET_PROJECT/.claude/skills"
PROJECT_SKILL_PATH="$PROJECT_SKILLS_DIR/nflow"

mkdir -p "$PROJECT_SKILLS_DIR"

# Copy skill files to .claude/skills/nflow/
rm -rf "$PROJECT_SKILL_PATH"
cp -r "$SKILL_DIR" "$PROJECT_SKILL_PATH/"

echo ""
echo "✅ 项目安装完成！"
echo ""
echo "📁 安装位置："
echo "   $PROJECT_SKILL_PATH/"
echo ""
echo "📋 目录结构："
echo "   $PROJECT_SKILL_PATH/SKILL.md"
echo "   $PROJECT_SKILL_PATH/commands/"
echo "   $PROJECT_SKILL_PATH/agents/"
echo "   $PROJECT_SKILL_PATH/templates/"
echo ""
echo "🚀 开始使用："
echo "   在 Claude Code 中："
echo "   /nflow-init"
