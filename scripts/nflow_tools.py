#!/usr/bin/env python3
"""
NFlow 工具脚本 - 内部状态扫描和管理
避免 LLM 消耗 token 处理常规状态查询

用法:
    python3 nflow_tools.py <command> [options]

命令:
    scan-sprints          扫描所有 Sprint 状态（默认包含 Hotfix）
    scan-sprints --include-hotfix  扫描时包含 Hotfix Sprint
    scan-sprints --no-hotfix      扫描时不包含 Hotfix Sprint
    get-next-story        获取下一个待处理的 Story
    get-story <id>        获取指定 Story 的详细信息
    update-state <id> <state>  更新 Story 状态
    increment-test-fail <id>   测试失败次数 +1
    increment-review-fail <id> 审查失败次数 +1
    check-blocked          检查被阻塞的 Stories
    list-worktrees         列出 Git worktree 状态
    show-backlog           显示 Backlog 概览
    
    init-memory            初始化项目记忆文件
    update-memory          更新项目记忆
    log-decision           记录决策
    generate-context       生成外部 Agent 上下文
"""

import os
import sys
import re
import json
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime
from argparse import ArgumentParser


@dataclass
class Story:
    id: str
    name: str
    priority: str
    points: int
    sprint: str
    state: str
    assignee: str
    notes: str = ""
    test_fail_count: int = 0
    review_fail_count: int = 0


class NFlowTools:
    """NFlow 状态管理工具"""
    
    # 状态 emoji 映射
    STATE_MAP = {
        "⏳": "TODO",
        "🔄": "IN_PROGRESS",
        "🔍": "CODE_REVIEW",
        "🧪": "TESTING",
        "✅": "DONE",
        "🚫": "BLOCKED"
    }
    
    REVERSE_STATE_MAP = {v: k for k, v in STATE_MAP.items()}
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.docs_dir = self.project_root / "docs"
        self.sprints_dir = self.project_root / "sprints"
        self.templates_dir = Path(__file__).parent.parent / "templates"
    
    # ============ Sprint 扫描 ============
    
    def scan_sprints(self, include_hotfix: bool = True) -> dict:
        """扫描所有 Sprint 状态"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "sprints": [],
            "hotfix_sprints": [],
            "total": {"sprints": 0, "stories": 0, "done": 0},
            "next_action": None
        }
        
        state_counts = {"TODO": 0, "IN_PROGRESS": 0, "CODE_REVIEW": 0, 
                       "TESTING": 0, "DONE": 0, "BLOCKED": 0}
        
        # 扫描普通 Sprint（sprint-* 但不是 hotfix-*）
        for sprint_dir in sorted(self.sprints_dir.glob("sprint-*")):
            if not sprint_dir.is_dir():
                continue
            
            # 跳过 hotfix 目录
            if sprint_dir.name.startswith("hotfix-"):
                continue
            
            tracker = sprint_dir / "user-stories-tracker.md"
            if not tracker.exists():
                continue
            
            sprint_data = self._parse_tracker(tracker)
            sprint_name = sprint_dir.name
            
            done = sum(1 for s in sprint_data["stories"] if s.state == "DONE")
            total = len(sprint_data["stories"])
            
            sprint_info = {
                "name": sprint_name,
                "type": "sprint",
                "stories_total": total,
                "stories_done": done,
                "progress_percent": (done * 100 // total) if total > 0 else 0,
                "state_breakdown": sprint_data["state_counts"]
            }
            
            result["sprints"].append(sprint_info)
            result["total"]["sprints"] += 1
            result["total"]["stories"] += total
            result["total"]["done"] += done
            
            for state, count in sprint_data["state_counts"].items():
                if state in state_counts:
                    state_counts[state] += count
        
        # 扫描 Hotfix Sprint
        if include_hotfix:
            for sprint_dir in sorted(self.sprints_dir.glob("hotfix-*")):
                if not sprint_dir.is_dir():
                    continue
                
                tracker = sprint_dir / "user-stories-tracker.md"
                if not tracker.exists():
                    continue
                
                sprint_data = self._parse_tracker(tracker)
                sprint_name = sprint_dir.name
                
                done = sum(1 for s in sprint_data["stories"] if s.state == "DONE")
                total = len(sprint_data["stories"])
                remaining = total - done
                
                sprint_info = {
                    "name": sprint_name,
                    "type": "hotfix",
                    "stories_total": total,
                    "stories_done": done,
                    "stories_remaining": remaining,
                    "progress_percent": (done * 100 // total) if total > 0 else 0,
                    "state_breakdown": sprint_data["state_counts"]
                }
                
                result["hotfix_sprints"].append(sprint_info)
        
        result["state_counts"] = state_counts
        result["total"]["remaining"] = result["total"]["stories"] - result["total"]["done"]
        result["next_action"] = self._determine_next_action(result, include_hotfix)
        
        return result
    
    def _parse_tracker(self, tracker_path: Path) -> dict:
        """解析 user-stories-tracker.md 文件"""
        stories = []
        state_counts = {"TODO": 0, "IN_PROGRESS": 0, "CODE_REVIEW": 0,
                       "TESTING": 0, "DONE": 0, "BLOCKED": 0}
        
        if not tracker_path.exists():
            return {"stories": stories, "state_counts": state_counts}
        
        content = tracker_path.read_text(encoding='utf-8')
        
        for line in content.split('\n'):
            for emoji, state in self.STATE_MAP.items():
                if emoji in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 8:
                        story = Story(
                            id=parts[1] if parts[1] else "",
                            name=parts[2] if parts[2] else "",
                            priority=parts[3] if parts[3] else "P2",
                            points=int(parts[4]) if parts[4].isdigit() else 0,
                            sprint=parts[5] if parts[5] else "",
                            state=state,
                            assignee=parts[6] if len(parts) > 6 else "",
                            notes=parts[7] if len(parts) > 7 else ""
                        )
                        
                        notes = story.notes
                        if "测试失败" in notes:
                            match = re.search(r'测试失败第(\d+)次', notes)
                            if match:
                                story.test_fail_count = int(match.group(1))
                        if "审查第" in notes:
                            match = re.search(r'审查第(\d+)次', notes)
                            if match:
                                story.review_fail_count = int(match.group(1))
                        
                        stories.append(story)
                        state_counts[state] += 1
                    break
        
        return {"stories": stories, "state_counts": state_counts}
    
    def _determine_next_action(self, scan_result: dict, include_hotfix: bool = True) -> dict:
        """确定下一步动作（Hotfix Sprint 优先）"""
        
        # P0: 检查 Hotfix Sprint
        if include_hotfix and scan_result.get("hotfix_sprints"):
            for sprint in scan_result["hotfix_sprints"]:
                remaining = sprint["stories_total"] - sprint["stories_done"]
                if remaining > 0:
                    return {
                        "action": "continue_hotfix",
                        "sprint": sprint["name"],
                        "priority": "P0",
                        "remaining_stories": remaining
                    }
        
        # P1: 检查普通 Sprint
        for sprint in scan_result["sprints"]:
            remaining = sprint["stories_total"] - sprint["stories_done"]
            if remaining > 0:
                return {
                    "action": "continue_sprint",
                    "sprint": sprint["name"],
                    "priority": "P1",
                    "remaining_stories": remaining
                }
        
        # P2: 无 Stories
        if scan_result["total"]["stories"] == 0:
            return {"action": "plan_new_sprint"}
        
        # P3: 全部完成
        return {"action": "all_complete"}
    
    # ============ Story 操作 ============
    
    def get_next_story(self, sprint_name: str = None) -> Optional[Story]:
        """获取下一个待处理的 Story"""
        if sprint_name:
            tracker = self.sprints_dir / sprint_name / "user-stories-tracker.md"
            if tracker.exists():
                data = self._parse_tracker(tracker)
                for story in data["stories"]:
                    if story.state == "TODO":
                        return story
        else:
            for sprint_dir in sorted(self.sprints_dir.glob("sprint-*"), reverse=True):
                tracker = sprint_dir / "user-stories-tracker.md"
                if tracker.exists():
                    data = self._parse_tracker(tracker)
                    for story in data["stories"]:
                        if story.state == "TODO":
                            return story
        return None
    
    def get_story(self, story_id: str) -> Optional[Story]:
        """获取指定 Story"""
        for sprint_dir in self.sprints_dir.glob("sprint-*"):
            tracker = sprint_dir / "user-stories-tracker.md"
            if tracker.exists():
                data = self._parse_tracker(tracker)
                for story in data["stories"]:
                    if story.id == story_id:
                        return story
        return None
    
    def update_story_state(self, story_id: str, new_state: str) -> bool:
        """更新 Story 状态"""
        if new_state not in self.REVERSE_STATE_MAP:
            print(f"❌ 无效状态: {new_state}")
            return False
        
        emoji = self.REVERSE_STATE_MAP[new_state]
        
        for sprint_dir in self.sprints_dir.glob("sprint-*"):
            tracker = sprint_dir / "user-stories-tracker.md"
            if tracker.exists():
                content = tracker.read_text(encoding='utf-8')
                
                for line in content.split('\n'):
                    if story_id in line and any(e in line for e in self.STATE_MAP.keys()):
                        # 找到该 story 的行，替换状态
                        for old_emoji, state in self.STATE_MAP.items():
                            if old_emoji in line and state == new_state:
                                # 已经是这个状态
                                return True
                            elif old_emoji in line:
                                new_line = line.replace(old_emoji, emoji)
                                content = content.replace(line, new_line)
                                tracker.write_text(content, encoding='utf-8')
                                print(f"✅ {story_id} 状态更新为 {emoji} {new_state}")
                                return True
        return False
    
    def increment_test_fail(self, story_id: str) -> int:
        """测试失败次数 +1"""
        new_count = 0
        for sprint_dir in self.sprints_dir.glob("sprint-*"):
            tracker = sprint_dir / "user-stories-tracker.md"
            if tracker.exists():
                content = tracker.read_text(encoding='utf-8')
                
                for line in content.split('\n'):
                    if story_id in line:
                        match = re.search(rf'{re.escape(story_id)}.*?测试失败第(\d+)次', line)
                        current = int(match.group(1)) if match else 0
                        new_count = current + 1
                        
                        if "测试失败" in line:
                            new_line = re.sub(r'测试失败第\d+次', f'测试失败第{new_count}次', line)
                        else:
                            new_line = line + f' 测试失败第{new_count}次'
                        
                        content = content.replace(line, new_line)
                        tracker.write_text(content, encoding='utf-8')
                        print(f"✅ {story_id} 测试失败次数: {current} → {new_count}")
                        break
        return new_count
    
    def increment_review_fail(self, story_id: str) -> int:
        """审查失败次数 +1"""
        new_count = 0
        for sprint_dir in self.sprints_dir.glob("sprint-*"):
            tracker = sprint_dir / "user-stories-tracker.md"
            if tracker.exists():
                content = tracker.read_text(encoding='utf-8')
                
                for line in content.split('\n'):
                    if story_id in line:
                        match = re.search(rf'{re.escape(story_id)}.*?审查第(\d+)次', line)
                        current = int(match.group(1)) if match else 0
                        new_count = current + 1
                        
                        if "审查第" in line:
                            new_line = re.sub(r'审查第\d+次', f'审查第{new_count}次', line)
                        else:
                            new_line = line + f' 审查第{new_count}次'
                        
                        content = content.replace(line, new_line)
                        tracker.write_text(content, encoding='utf-8')
                        print(f"✅ {story_id} 审查失败次数: {current} → {new_count}")
                        break
        return new_count
    
    # ============ 检查操作 ============
    
    def check_blocked(self) -> list:
        """检查被阻塞的 Stories"""
        blocked = []
        for sprint_dir in self.sprints_dir.glob("sprint-*"):
            tracker = sprint_dir / "user-stories-tracker.md"
            if tracker.exists():
                data = self._parse_tracker(tracker)
                for story in data["stories"]:
                    if story.state == "BLOCKED":
                        blocked.append(story)
        return blocked
    
    def check_3_strikes(self, story_id: str) -> dict:
        """检查 3 次失败规则"""
        story = self.get_story(story_id)
        if not story:
            return {"found": False}
        
        return {
            "found": True,
            "story_id": story_id,
            "test_fail_count": story.test_fail_count,
            "review_fail_count": story.review_fail_count,
            "test_fail_3": story.test_fail_count >= 3,
            "review_fail_3": story.review_fail_count >= 3,
            "requires_human_intervention": story.test_fail_count >= 3 or story.review_fail_count >= 3
        }
    
    # ============ Git Worktree ============
    
    def list_worktrees(self) -> list:
        """列出 Git worktree 状态"""
        try:
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                capture_output=True, text=True, cwd=self.project_root
            )
            
            worktrees = []
            current = {}
            
            for line in result.stdout.split('\n'):
                if not line:
                    if current:
                        worktrees.append(current)
                        current = {}
                    continue
                
                if line.startswith("worktree "):
                    current["path"] = line[9:]
                elif line.startswith("HEAD "):
                    current["head"] = line[5:]
                elif line.startswith("branch "):
                    current["branch"] = line[7:]
                elif line == "bare":
                    current["bare"] = True
            
            return worktrees
        except Exception as e:
            return [{"error": str(e)}]
    
    # ============ Backlog ============
    
    def show_backlog(self) -> dict:
        """显示 Backlog 概览"""
        backlog_file = self.sprints_dir / "backlog.md"
        
        if not backlog_file.exists():
            return {"found": False, "message": "backlog.md not found"}
        
        content = backlog_file.read_text(encoding='utf-8')
        epics = re.findall(r'^##?\s*EPIC[:\-]?\s*(.+)', content, re.MULTILINE)
        stories = re.findall(r'^[-*]\s*STORY[:\-]?\s*(.+)', content, re.MULTILINE)
        
        return {
            "found": True,
            "file": str(backlog_file),
            "epics_count": len(epics),
            "stories_count": len(stories),
            "preview": content[:500]
        }
    
    # ============ 记忆管理 ============
    
    def init_memory(self, project_name: str, config: dict = None) -> bool:
        """初始化项目记忆文件"""
        config = config or {}
        
        # 确保目录存在
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.sprints_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化 project-memory.md
        memory_file = self.docs_dir / "project-memory.md"
        if not memory_file.exists():
            template = self.templates_dir / "project-memory.md"
            if template.exists():
                content = template.read_text(encoding='utf-8')
                content = content.replace("{project-name}", project_name)
                content = content.replace("{date}", datetime.now().strftime("%Y-%m-%d"))
                content = content.replace("{n}", "0")
                memory_file.write_text(content, encoding='utf-8')
                print(f"✅ 创建: {memory_file}")
            else:
                # 创建默认内容
                content = f"""# Project Memory

**项目:** {project_name}
**创建日期:** {datetime.now().strftime("%Y-%m-%d")}
**最后更新:** {datetime.now().strftime("%Y-%m-%d")}
**当前阶段:** Phase 0

---

## 项目信息

| 字段 | 值 |
|------|-----|
| 项目名称 | {project_name} |
| 项目路径 | {self.project_root} |
| 复杂度等级 | {config.get('complexity', 'L2')} |
| 开发方式 | {config.get('dev_mode', 'OpenClaw')} |

---

## 当前状态

### Sprint 进度

| Sprint | 完成 | 总计 | 状态 | 当前 Story |
|--------|------|------|------|------------|

### 关键架构决策

| ID | 决策 | 日期 |
|----|------|------|

### 已知问题

| 问题 | 影响 | 状态 |
|------|------|------|

---

## 技术栈

| 类别 | 选择 |
|------|------|
"""
                memory_file.write_text(content, encoding='utf-8')
                print(f"✅ 创建: {memory_file}")
        
        # 初始化 decision-log.md
        decision_file = self.sprints_dir / "decision-log.md"
        if not decision_file.exists():
            content = f"""# Decision Log

**项目:** {project_name}
**创建日期:** {datetime.now().strftime("%Y-%m-%d")}

---

## 架构决策

| ID | 日期 | 决策 | 原因 | 替代方案 | 状态 |
|----|------|------|------|----------|------|

---

## 技术选型

| ID | 日期 | 选择 | 原因 | 替代方案 | 状态 |
|----|------|------|------|----------|------|

---

## 设计决策

| ID | 日期 | 决策 | 原因 | 状态 |
|----|------|------|------|------|

---

## 变更记录

| 日期 | 决策 ID | 变更内容 | 原因 | 决策者 |
|------|---------|----------|------|--------|
"""
            decision_file.write_text(content, encoding='utf-8')
            print(f"✅ 创建: {decision_file}")
        
        return True
    
    def update_memory(self, updates: dict) -> bool:
        """更新项目记忆"""
        memory_file = self.docs_dir / "project-memory.md"
        if not memory_file.exists():
            print("❌ project-memory.md 不存在，请先运行 init-memory")
            return False
        
        content = memory_file.read_text(encoding='utf-8')
        
        # 更新最后更新时间
        content = re.sub(
            r'\*\*最后更新:\*\* .+',
            f'**最后更新:** {datetime.now().strftime("%Y-%m-%d")}',
            content
        )
        
        # 更新 Sprint 进度
        if "sprint_progress" in updates:
            sprint = updates["sprint_progress"]
            # 简单替换
            new_row = f"| {sprint['name']} | {sprint['done']} | {sprint['total']} | {sprint['status']} | {sprint.get('current_story', '-')} |"
            
            # 查找并替换对应 Sprint 行
            pattern = rf"\| {re.escape(sprint['name'])} \|"
            if re.search(pattern, content):
                content = re.sub(pattern + r"[^|]*\|[^|]*\|[^|]*\|[^|]*\|", new_row, content)
            else:
                # 添加新行（在表格最后一行后面）
                content = re.sub(r'(\| sprint-\d+ \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \|)\s*(?=\n##|$)', 
                              r'\1\n' + new_row, content)
        
        # 更新已知问题
        if "known_issue" in updates:
            issue = updates["known_issue"]
            new_row = f"| {issue['desc']} | {issue['impact']} | ⚠️  |"
            content = re.sub(r'(\| [^|]+ \| [^|]+ \| ⚠️  \|)\s*(?=\n##|$)', 
                            new_row + r'\n\1', content)
        
        # 更新当前阶段
        if "phase" in updates:
            content = re.sub(
                r'\*\*当前阶段:\*\* Phase \d+',
                f'**当前阶段:** Phase {updates["phase"]}',
                content
            )
        
        memory_file.write_text(content, encoding='utf-8')
        print(f"✅ 更新: {memory_file}")
        return True
    
    def log_decision(self, decision_type: str, decision: str, reason: str, 
                     alternatives: str = "", status: str = "✅") -> bool:
        """记录决策到 decision-log.md"""
        decision_file = self.sprints_dir / "decision-log.md"
        if not decision_file.exists():
            print("❌ decision-log.md 不存在，请先运行 init-memory")
            return False
        
        content = decision_file.read_text(encoding='utf-8')
        date = datetime.now().strftime("%Y-%m-%d")
        
        # 生成 ID
        if decision_type.upper() == "ARCH":
            id_prefix = "ARCH"
        elif decision_type.upper() == "TECH":
            id_prefix = "TECH"
        elif decision_type.upper() == "DESIGN":
            id_prefix = "DESIGN"
        else:
            id_prefix = "DEC"
        
        # 计算下一个 ID
        existing_ids = re.findall(rf'{id_prefix}-(\d+)', content)
        next_num = max([int(i) for i in existing_ids], default=0) + 1
        decision_id = f"{id_prefix}-{next_num:03d}"
        
        # 根据类型添加到对应表格
        new_row = f"| {decision_id} | {date} | {decision} | {reason} | {alternatives} | {status} |"
        
        if decision_type.upper() == "ARCH":
            # 添加到架构决策表格
            if "| ID | 日期 | 决策 | 原因 | 替代方案 | 状态 |" in content:
                content = content.replace(
                    "| ID | 日期 | 决策 | 原因 | 替代方案 | 状态 |",
                    "| ID | 日期 | 决策 | 原因 | 替代方案 | 状态 |\n" + "| " + "-|" * 6
                )
                content = content.replace(
                    "| " + "-|" * 6 + "\n" + new_row,
                    "| " + "-|" * 6 + "\n" + new_row
                )
        elif decision_type.upper() == "TECH":
            if "| ID | 日期 | 选择 | 原因 | 替代方案 | 状态 |" in content:
                content = content.replace(
                    "| ID | 日期 | 选择 | 原因 | 替代方案 | 状态 |",
                    "| ID | 日期 | 选择 | 原因 | 替代方案 | 状态 |\n" + "| " + "-|" * 6
                )
        
        decision_file.write_text(content, encoding='utf-8')
        print(f"✅ 记录决策: {decision_id} - {decision}")
        return True
    
    def generate_context(self, story_id: str = None) -> dict:
        """生成外部 Agent 上下文"""
        memory_file = self.docs_dir / "project-memory.md"
        decision_file = self.sprints_dir / "decision-log.md"
        
        context = {
            "project": {
                "name": self.project_root.name,
                "path": str(self.project_root),
                "memory_exists": memory_file.exists(),
                "decision_log_exists": decision_file.exists()
            },
            "sprint_status": self.scan_sprints(),
            "current_story": None,
            "memory_content": None,
            "decision_log_preview": None
        }
        
        # 如果指定了 story，获取详情
        if story_id:
            story = self.get_story(story_id)
            if story:
                context["current_story"] = asdict(story)
        
        # 读取记忆文件
        if memory_file.exists():
            context["memory_content"] = memory_file.read_text(encoding='utf-8')[:2000]
        
        # 读取决策日志预览
        if decision_file.exists():
            content = decision_file.read_text(encoding='utf-8')
            # 只取架构决策部分
            arch_section = re.search(r'## 架构决策(.+?)(?=##|$)', content, re.DOTALL)
            if arch_section:
                context["decision_log_preview"] = arch_section.group(1)[:1000]
        
        return context
    
    def get_context_for_spawn(self, story_id: str = None) -> str:
        """生成用于 spawn 外部 Agent 的上下文文本"""
        context = self.generate_context(story_id)
        
        lines = []
        lines.append("## 项目上下文")
        lines.append("")
        lines.append(f"**项目:** {context['project']['name']}")
        lines.append(f"**路径:** {context['project']['path']}")
        lines.append("")
        
        # Sprint 状态
        sprint_status = context["sprint_status"]
        if sprint_status["sprints"]:
            lines.append("### Sprint 进度")
            for sp in sprint_status["sprints"]:
                lines.append(f"- **{sp['name']}**: {sp['stories_done']}/{sp['stories_total']} ({sp['progress_percent']}%)")
            lines.append("")
        
        # 当前 Story
        if context["current_story"]:
            story = context["current_story"]
            lines.append("### 当前 Story")
            lines.append(f"- **ID**: {story['id']}")
            lines.append(f"- **名称**: {story['name']}")
            lines.append(f"- **状态**: {story['state']}")
            lines.append(f"- **优先级**: {story['priority']}")
            lines.append("")
        
        # 已知问题
        if context["memory_content"]:
            if "⚠️" in context["memory_content"]:
                lines.append("### 已知问题")
                for line in context["memory_content"].split('\n'):
                    if "⚠️" in line:
                        lines.append(f"- {line.strip()}")
                lines.append("")
        
        # 决策日志
        if context["decision_log_preview"]:
            lines.append("### 关键架构决策")
            lines.append("```")
            lines.append(context["decision_log_preview"][:500])
            lines.append("```")
            lines.append("")
        
        # 参考文档
        lines.append("### 参考文档")
        lines.append(f"- 架构: {self.docs_dir / 'architecture.md'}")
        lines.append(f"- PRD: {self.docs_dir / 'prd.md'}")
        lines.append("")
        
        return "\n".join(lines)

    # ============ Sprint Review ============
    
    def generate_sprint_review(self, sprint_name: str, retrospective: dict = None) -> bool:
        """生成 Sprint 回顾文档"""
        retrospective = retrospective or {}
        
        sprint_dir = self.sprints_dir / sprint_name
        if not sprint_dir.exists():
            print(f"❌ Sprint 目录不存在: {sprint_dir}")
            return False
        
        tracker = sprint_dir / "user-stories-tracker.md"
        sprint_data = self._parse_tracker(tracker) if tracker.exists() else {"stories": [], "state_counts": {}}
        
        total_stories = len(sprint_data["stories"])
        done_stories = sum(1 for s in sprint_data["stories"] if s.state == "DONE")
        total_points = sum(s.points for s in sprint_data["stories"])
        done_points = sum(s.points for s in sprint_data["stories"] if s.state == "DONE")
        
        review_file = sprint_dir / "review.md"
        
        lines = []
        lines.append(f"# Sprint Review - {sprint_name}")
        lines.append("")
        lines.append(f"**日期:** {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(f"**Sprint:** {sprint_name}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 执行摘要")
        lines.append("")
        lines.append("| 指标 | 值 |")
        lines.append("|------|-----|")
        lines.append(f"| 计划 Stories | {total_stories} |")
        lines.append(f"| 完成 Stories | {done_stories} |")
        lines.append(f"| 完成率 | {int(done_stories * 100 / total_stories) if total_stories > 0 else 0}% |")
        lines.append(f"| 计划故事点 | {total_points} |")
        lines.append(f"| 完成故事点 | {done_points} |")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 完成 Stories")
        lines.append("")
        lines.append("| Story ID | 名称 | 故事点 | 状态 |")
        lines.append("|----------|------|--------|------|")
        for story in sprint_data["stories"]:
            if story.state == "DONE":
                lines.append(f"| {story.id} | {story.name} | {story.points} | ✅ DONE |")
        lines.append("")
        
        incomplete = [s for s in sprint_data["stories"] if s.state != "DONE"]
        if incomplete:
            lines.append("## 未完成 Stories")
            lines.append("")
            lines.append("| Story ID | 名称 | 故事点 | 状态 | 原因 |")
            lines.append("|----------|------|--------|------|------|")
            for story in incomplete:
                lines.append(f"| {story.id} | {story.name} | {story.points} | {story.state} | {retrospective.get('reason', 'N/A')} |")
            lines.append("")
        
        lines.append("## 做得好的")
        lines.append("")
        for item in retrospective.get('went_well', []):
            lines.append(f"- {item}")
        if not retrospective.get('went_well'):
            lines.append("- (待填写)")
        lines.append("")
        
        lines.append("## 需要改进")
        lines.append("")
        for item in retrospective.get('improve', []):
            lines.append(f"- {item}")
        if not retrospective.get('improve'):
            lines.append("- (待填写)")
        lines.append("")
        
        lines.append("## 下个 Sprint 关注点")
        lines.append("")
        for item in retrospective.get('next_sprint', []):
            lines.append(f"- {item}")
        if not retrospective.get('next_sprint'):
            lines.append("- (待填写)")
        lines.append("")
        
        interventions = [s for s in sprint_data["stories"] if s.test_fail_count > 0 or s.review_fail_count > 0]
        if interventions:
            lines.append("## 人工干预记录")
            lines.append("")
            lines.append("| 日期 | Story | 问题 | 解决方案 |")
            lines.append("|------|-------|------|----------|")
            for story in interventions:
                if story.test_fail_count >= 3:
                    lines.append(f"| {datetime.now().strftime('%Y-%m-%d')} | {story.id} | 测试失败 {story.test_fail_count} 次 | Tech Lead 介入 |")
                if story.review_fail_count >= 3:
                    lines.append(f"| {datetime.now().strftime('%Y-%m-%d')} | {story.id} | 审查失败 {story.review_fail_count} 次 | Tech Lead 介入 |")
            lines.append("")
        
        review_file.write_text("\n".join(lines), encoding='utf-8')
        print(f"✅ 生成 Sprint 回顾: {review_file}")
        return True
    
    def update_memory_with_retrospective(self, sprint_name: str, retrospective: dict) -> bool:
        """更新 project-memory.md 包含 Sprint 回顾数据"""
        memory_file = self.docs_dir / "project-memory.md"
        if not memory_file.exists():
            print("❌ project-memory.md 不存在")
            return False
        
        content = memory_file.read_text(encoding='utf-8')
        
        content = re.sub(
            r'\*\*最后更新:\*\* .+',
            f'**最后更新:** {datetime.now().strftime("%Y-%m-%d")}',
            content
        )
        
        sprint_section = """

---

### Sprint 回顾 - {sprint_name}

**日期:** {datetime.now().strftime('%Y-%m-%d')}

**做得好的:**
"""
        for item in retrospective.get('went_well', []):
            sprint_section += f"- {item}\n"
        if not retrospective.get('went_well'):
            sprint_section += "- (待填写)\n"
        
        sprint_section += "\n**需要改进:**\n"
        for item in retrospective.get('improve', []):
            sprint_section += f"- {item}\n"
        if not retrospective.get('improve'):
            sprint_section += "- (待填写)\n"
        
        sprint_section += "\n**教训:**\n"
        for item in retrospective.get('lessons', []):
            sprint_section += f"- {item}\n"
        if not retrospective.get('lessons'):
            sprint_section += "- (待填写)\n"
        
        if "### Sprint 回顾" in content:
            content = re.sub(
                r'(### Sprint 回顾 - \w+\n\n\*\*日期:\*\* .+\n)',
                sprint_section + r'\1',
                content
            )
        else:
            content += sprint_section
        
        memory_file.write_text(content, encoding='utf-8')
        print(f"✅ 更新项目记忆: {memory_file}")
        return True





def main():
    parser = ArgumentParser(description="NFlow Tools")
    parser.add_argument("command", help="子命令")
    parser.add_argument("args", nargs="*", help="命令参数")
    
    args = parser.parse_args()
    tools = NFlowTools()
    
    cmd = args.command
    
    if cmd == "scan-sprints":
        include_hotfix = "--include-hotfix" in args.args or "--hotfix" in args.args
        result = tools.scan_sprints(include_hotfix=include_hotfix)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "get-next-story":
        story = tools.get_next_story()
        if story:
            print(json.dumps({"found": True, "story": asdict(story)}, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({"found": False}))
    
    elif cmd == "get-story":
        if len(args.args) < 1:
            print("❌ 需要 story_id")
            sys.exit(1)
        story = tools.get_story(args.args[0])
        if story:
            print(json.dumps({"found": True, "story": asdict(story)}, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({"found": False}))
    
    elif cmd == "update-state":
        if len(args.args) < 2:
            print("❌ 需要 story_id 和 state")
            sys.exit(1)
        success = tools.update_story_state(args.args[0], args.args[1])
        sys.exit(0 if success else 1)
    
    elif cmd == "increment-test-fail":
        if len(args.args) < 1:
            print("❌ 需要 story_id")
            sys.exit(1)
        count = tools.increment_test_fail(args.args[0])
        print(f"当前失败次数: {count}")
    
    elif cmd == "increment-review-fail":
        if len(args.args) < 1:
            print("❌ 需要 story_id")
            sys.exit(1)
        count = tools.increment_review_fail(args.args[0])
        print(f"当前失败次数: {count}")
    
    elif cmd == "check-blocked":
        blocked = tools.check_blocked()
        print(json.dumps({
            "count": len(blocked),
            "stories": [asdict(s) for s in blocked]
        }, indent=2, ensure_ascii=False))
    
    elif cmd == "check-3-strikes":
        if len(args.args) < 1:
            print("❌ 需要 story_id")
            sys.exit(1)
        result = tools.check_3_strikes(args.args[0])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "list-worktrees":
        worktrees = tools.list_worktrees()
        print(json.dumps(worktrees, indent=2, ensure_ascii=False))
    
    elif cmd == "show-backlog":
        result = tools.show_backlog()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "init-memory":
        project_name = args.args[0] if args.args else tools.project_root.name
        config = {}
        if len(args.args) > 1:
            config["complexity"] = args.args[1]
        if len(args.args) > 2:
            config["dev_mode"] = args.args[2]
        tools.init_memory(project_name, config)
    
    elif cmd == "update-memory":
        updates = {}
        for arg in args.args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                updates[key] = value
        tools.update_memory(updates)
    
    elif cmd == "log-decision":
        if len(args.args) < 3:
            print("❌ 需要: type decision reason [alternatives]")
            sys.exit(1)
        decision_type = args.args[0]
        decision = args.args[1]
        reason = args.args[2]
        alternatives = args.args[3] if len(args.args) > 3 else ""
        tools.log_decision(decision_type, decision, reason, alternatives)
    
    elif cmd == "generate-context":
        story_id = args.args[0] if args.args else None
        result = tools.generate_context(story_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "get-context":
        story_id = args.args[0] if args.args else None
        context_text = tools.get_context_for_spawn(story_id)
        print(context_text)
    
    elif cmd == "generate-review":
        if len(args.args) < 1:
            print("❌ 需要 sprint_name (如 sprint-01)")
            sys.exit(1)
        # 简单 retrospective 数据
        retrospective = {
            "went_well": ["TDD 流程顺利", "Code Review 及时"],
            "improve": ["预估误差大", "外部依赖需提前确认"],
            "next_sprint": ["提前确认第三方 API", "增加预估 buffer"]
        }
        tools.generate_sprint_review(args.args[0], retrospective)
    
    elif cmd == "update-retrospective":
        if len(args.args) < 2:
            print("❌ 需要: sprint-name \"json数据\"")
            sys.exit(1)
        sprint_name = args.args[0]
        import json
        try:
            retrospective = json.loads(" ".join(args.args[1:]))
        except:
            retrospective = {"went_well": [], "improve": [], "lessons": []}
        tools.update_memory_with_retrospective(sprint_name, retrospective)
    
    else:
        print(f"❌ 未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
