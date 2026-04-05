#!/usr/bin/env python3
"""
NFlow Telegram 通知脚本
在每个开发节点完成后发送任务结果通知

用法:
    python3 scripts/nflow_notify.py --node "节点名称" --status success --message "详情"
    python3 scripts/nflow_notify.py --node "TDD开发" --status success --screenshot "path/to/screenshot.png"
    python3 scripts/nflow_notify.py --node "E2E测试" --status failure --message "测试失败原因"
"""

import argparse
import subprocess
from pathlib import Path
from datetime import datetime


TELEGRAM_TARGET = "7314529482"  # 老大


def send_telegram_message(message: str, media: str = None):
    """发送 Telegram 消息"""
    cmd = [
        "openclaw", "message", "send",
        "--channel", "telegram",
        "--target", TELEGRAM_TARGET,
        "--message", message
    ]
    
    if media:
        # 检查截图是否存在
        media_path = Path(media)
        if media_path.exists():
            cmd.extend(["--media", str(media_path.absolute())])
        else:
            message += f"\n⚠️ 截图不存在: {media}"
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def format_node_report(node_name: str, status: str, message: str = "", screenshot: str = None, story_id: str = None, sprint: str = None):
    """格式化节点报告"""
    status_emoji = {
        "success": "✅",
        "failure": "❌",
        "warning": "⚠️",
        "pending": "⏳"
    }
    
    emoji = status_emoji.get(status, "📋")
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    report = [
        f"{emoji} **NFlow 开发节点报告**",
        f"",
        f"**节点:** {node_name}",
        f"**状态:** {status.upper()}",
        f"**时间:** {timestamp}",
    ]
    
    if story_id:
        report.append(f"**Story:** {story_id}")
    
    if sprint:
        report.append(f"**Sprint:** {sprint}")
    
    if message:
        report.append(f"")
        report.append(f"**详情:**")
        report.append(message)
    
    report.append(f"")
    report.append(f"---")
    report.append(f"_由 NFlow 自动发送_")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="NFlow Telegram 通知")
    parser.add_argument("--node", required=True, help="节点名称")
    parser.add_argument("--status", required=True, choices=["success", "failure", "warning", "pending"], help="执行状态")
    parser.add_argument("--message", help="详细信息")
    parser.add_argument("--screenshot", help="截图路径")
    parser.add_argument("--story-id", help="Story ID")
    parser.add_argument("--sprint", help="Sprint 名称")
    parser.add_argument("--dry-run", action="store_true", help="仅打印，不发送")
    
    args = parser.parse_args()
    
    # 格式化报告
    report = format_node_report(
        node_name=args.node,
        status=args.status,
        message=args.message,
        screenshot=args.screenshot,
        story_id=args.story_id,
        sprint=args.sprint
    )
    
    if args.dry_run:
        print("=== 干运行 - 不发送 ===")
        print(report)
        if args.screenshot:
            print(f"\n截图: {args.screenshot}")
        return
    
    # 发送通知
    success = send_telegram_message(report, args.screenshot)
    
    if success:
        print(f"✅ 通知已发送: {args.node} - {args.status}")
    else:
        print(f"❌ 通知发送失败: {args.node}")


if __name__ == "__main__":
    main()
