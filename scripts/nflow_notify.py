#!/usr/bin/env python3
"""
NFlow 通用通知脚本
支持多渠道发送通知（Telegram、Discord、Slack 等）

配置方式:
    在项目根目录创建 .nflow/notify-config.json
    或通过 --config 指定配置文件路径

配置格式:
{
    "channel": "telegram",           // 发送渠道
    "target": "7314529482",         // 目标（chat_id, channel_id 等）
    "enabled": true                  // 是否启用通知
}

支持的渠道:
- telegram: 使用 openclaw message send --channel telegram
- discord:  使用 openclaw message send --channel discord
- slack:    使用 openclaw message send --channel slack
- ... 其他 openclaw 支持的渠道

用法:
    python3 scripts/nflow_notify.py --node "节点" --status success --message "详情"
    python3 scripts/nflow_notify.py --node "E2E测试" --status success --screenshot "report.png"
    python3 scripts/nflow_notify.py --config /path/to/config.json --node "测试" --status success
"""

import argparse
import json
import subprocess
import os
from pathlib import Path
from datetime import datetime


def load_notify_config(config_path: str = None) -> dict:
    """加载通知配置"""
    # 默认配置
    default_config = {
        "channel": "telegram",
        "target": "7314529482",
        "enabled": True
    }
    
    # 尝试从项目配置加载
    if config_path is None:
        # 尝试从 .nflow/notify-config.json 加载
        possible_paths = [
            Path.cwd() / ".nflow" / "notify-config.json",
            Path.cwd() / "notify-config.json",
            Path(__file__).parent.parent / "notify-config.json",
        ]
        
        for path in possible_paths:
            if path.exists():
                config_path = str(path)
                break
    
    if config_path and Path(config_path).exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                # 合并默认配置
                default_config.update(config)
                return default_config
        except json.JSONDecodeError:
            print(f"⚠️ 配置文件格式错误: {config_path}")
    
    return default_config


def send_notification(channel: str, target: str, message: str, media: str = None):
    """发送通知到指定渠道"""
    # 构建命令
    cmd = [
        "openclaw", "message", "send",
        "--channel", channel,
        "--target", target,
        "--message", message
    ]
    
    # 添加媒体文件
    if media:
        media_path = Path(media)
        if media_path.exists():
            cmd.extend(["--media", str(media_path.absolute())])
        else:
            message += f"\n⚠️ 截图不存在: {media}"
            # 重新构建命令（不含 media）
            cmd = [
                "openclaw", "message", "send",
                "--channel", channel,
                "--target", target,
                "--message", message
            ]
    
    # 执行
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def format_report(node_name: str, status: str, message: str = "", 
                  screenshot: str = None, story_id: str = None, 
                  sprint: str = None) -> str:
    """格式化通知消息"""
    status_emoji = {
        "success": "✅",
        "failure": "❌",
        "warning": "⚠️",
        "pending": "⏳"
    }
    
    emoji = status_emoji.get(status, "📋")
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    lines = [
        f"{emoji} **NFlow 开发节点报告**",
        "",
        f"**节点:** {node_name}",
        f"**状态:** {status.upper()}",
        f"**时间:** {timestamp}",
    ]
    
    if story_id:
        lines.append(f"**Story:** {story_id}")
    
    if sprint:
        lines.append(f"**Sprint:** {sprint}")
    
    if message:
        lines.extend(["", f"**详情:**", message])
    
    lines.extend(["", "---", "_由 NFlow 自动发送_"])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="NFlow 通用通知脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 scripts/nflow_notify.py --node "测试" --status success --message "完成"
    python3 scripts/nflow_notify.py --node "E2E" --status success --screenshot "report.png"
    python3 scripts/nflow_notify.py --node "审查" --status warning --message "有问题"
    
配置文件 (.nflow/notify-config.json):
    {
        "channel": "telegram",
        "target": "7314529482",
        "enabled": true
    }
"""
    )
    
    parser.add_argument("--node", required=True, help="节点名称")
    parser.add_argument("--status", required=True, 
                       choices=["success", "failure", "warning", "pending"], 
                       help="执行状态")
    parser.add_argument("--message", help="详细信息")
    parser.add_argument("--screenshot", help="截图路径")
    parser.add_argument("--story-id", help="Story ID")
    parser.add_argument("--sprint", help="Sprint 名称")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--dry-run", action="store_true", help="仅打印，不发送")
    parser.add_argument("--list-channels", action="store_true", help="列出支持的渠道")
    
    args = parser.parse_args()
    
    # 列出支持的渠道
    if args.list_channels:
        print("""
支持的渠道:
    - telegram    OpenClaw Telegram 集成
    - discord    OpenClaw Discord 集成
    - slack      OpenClaw Slack 集成
    - whatsapp   OpenClaw WhatsApp 集成
    - signal     OpenClaw Signal 集成
    - imessage   OpenClaw iMessage 集成
    
配置方式:
    在项目根目录创建 .nflow/notify-config.json
""")
        return
    
    # 加载配置
    config = load_notify_config(args.config)
    
    if not config.get("enabled", True):
        print("通知已禁用（enabled=false）")
        return
    
    # 格式化消息
    report = format_report(
        node_name=args.node,
        status=args.status,
        message=args.message,
        screenshot=args.screenshot,
        story_id=args.story_id,
        sprint=args.sprint
    )
    
    if args.dry_run:
        print("=== 干运行 - 不发送 ===")
        print(f"渠道: {config['channel']}")
        print(f"目标: {config['target']}")
        print("---")
        print(report)
        if args.screenshot:
            print(f"\n截图: {args.screenshot}")
        return
    
    # 发送通知
    success, stdout, stderr = send_notification(
        channel=config["channel"],
        target=config["target"],
        message=report,
        media=args.screenshot
    )
    
    if success:
        print(f"✅ 通知已发送 [{config['channel']}]: {args.node} - {args.status}")
    else:
        print(f"❌ 通知发送失败 [{config['channel']}]: {args.node}")
        if stderr:
            print(f"   错误: {stderr}")


if __name__ == "__main__":
    main()
