#!/usr/bin/env python3
"""
spawn-dev-agent.py
通过 ACP 协议启动外部开发 Agent（如 Claude Code）执行开发任务

用法:
    python3 spawn-dev-agent.py --agent <agent-id> --task <task-type> --story-id <id>

示例:
    python3 spawn-dev-agent.py --agent claude-code --task dev --story-id STORY-001
    python3 spawn-dev-agent.py --agent codex --task review --story-id STORY-001
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 尝试导入 nflow_tools
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from nflow_tools import NFlowTools
    NFLOW_TOOLS_AVAILABLE = True
except ImportError:
    NFLOW_TOOLS_AVAILABLE = False


# Agent 职责描述模板
AGENT_TEMPLATES = {
    "developer": {
        "name": "Developer Agent",
        "persona_file": "agents/04-developer-agent.md",
        "responsibility": "TDD 开发、代码实现、RED→GREEN→REFACTOR 循环",
        "system_prompt_suffix": """
## 开发职责
- 遵循 TDD 方法：先写测试，再写实现
- RED: 编写一个失败的测试
- GREEN: 编写最少量代码让测试通过
- REFACTOR: 重构代码，消除重复
- 保持代码简洁，关注分离
- 所有新代码必须有测试覆盖
"""
    },
    "frontend": {
        "name": "Frontend Developer",
        "persona_file": "agents/00-frontend-developer-agent.md",
        "responsibility": "React/Vue/Angular 前端开发、组件实现、样式编写",
        "system_prompt_suffix": """
## 前端开发职责
- 遵循 design-pattern.json 中的设计规范
- 实现响应式 UI 组件
- 确保跨浏览器兼容性
- 组件需要有 Props 类型定义
- 编写组件单元测试
"""
    },
    "backend": {
        "name": "Backend Developer",
        "persona_file": "agents/00-backend-developer-agent.md",
        "responsibility": "Python/NestJS 后端开发、API 设计、数据库操作",
        "system_prompt_suffix": """
## 后端开发职责
- 遵循 architecture.md 中的 API 设计
- 实现 RESTful API
- 数据模型遵循 architecture.md
- 编写单元测试和集成测试
- 确保安全性（输入验证、SQL注入防护等）
"""
    },
    "qa": {
        "name": "QA Agent",
        "persona_file": "agents/06-qa-agent.md",
        "responsibility": "测试用例编写、E2E 测试、质量把关",
        "system_prompt_suffix": """
## QA 职责
- 编写 E2E 测试用例
- 执行测试并报告结果
- 验证所有 Acceptance Criteria
- 测试失败时详细描述问题
"""
    },
    "reviewer": {
        "name": "Code Reviewer",
        "persona_file": "agents/00-code-reviewer-agent.md",
        "responsibility": "代码审查、Blocker 发现、代码质量评估",
        "system_prompt_suffix": """
## Code Review 职责
- 检查代码正确性
- 发现 🔴 Blocker（必须修复）
- 发现 🟡 Suggestion（建议修复）
- 发现 💭 Nit（可选小问题）
- 提供可操作的审查反馈
"""
    },
    "git": {
        "name": "Git Workflow Master",
        "persona_file": "agents/00-git-workflow-master-agent.md",
        "responsibility": "Git 管理、worktree 操作、branch 策略",
        "system_prompt_suffix": """
## Git 职责
- 管理 Git worktree
- 创建 feat/story-{id} 分支
- 保持 commit 原子性
- 正确合并和冲突解决
"""
    }
}


def load_persona(agent_type: str, skill_root: Path) -> str:
    """加载 Agent persona 文件"""
    if agent_type not in AGENT_TEMPLATES:
        return ""
    
    persona_file = skill_root / AGENT_TEMPLATES[agent_type]["persona_file"]
    if persona_file.exists():
        return persona_file.read_text(encoding='utf-8')
    return ""


def get_project_context(project_root: Path, story_id: str = None, minimal: bool = True) -> str:
    """从项目记忆获取上下文
    
    Args:
        project_root: 项目根目录
        story_id: Story ID
        minimal: 是否使用最小化上下文（默认 True，仅传递当前 Story 信息）
    """
    if not NFLOW_TOOLS_AVAILABLE:
        return ""
    
    tools = NFlowTools(str(project_root))
    
    if minimal:
        # 最小化上下文：仅当前 Story，不泄露其他任务信息
        return tools.get_minimal_context_for_spawn(story_id)
    else:
        # 完整上下文：包含 Sprint 状态、已知问题、决策日志等
        return tools.get_context_for_spawn(story_id)


def build_spawn_command(agent_id: str, task_type: str, story_id: str, 
                        skill_root: Path, project_root: str,
                        minimal_context: bool = True,
                        use_context: bool = True) -> dict:
    """构建 ACP spawn 命令参数
    
    Args:
        agent_id: Agent ID (claude-code, codex, etc.)
        task_type: 任务类型 (developer, frontend, backend, qa, reviewer, git)
        story_id: Story ID
        skill_root: NFlow skill 根目录
        project_root: 项目根目录
        minimal_context: 是否使用最小化上下文（默认 True，仅传递当前 Story 信息）
        use_context: 是否加载项目上下文（默认 True）
    """
    
    agent_config = AGENT_TEMPLATES.get(task_type, AGENT_TEMPLATES["developer"])
    project_path = Path(project_root)
    
    # 加载 persona
    persona = load_persona(task_type, skill_root)
    
    # 获取项目上下文
    if use_context:
        project_context = get_project_context(project_path, story_id, minimal=minimal_context)
    else:
        project_context = ""
    
    # 获取 Story 详情
    story_info = ""
    if NFLOW_TOOLS_AVAILABLE and story_id:
        tools = NFlowTools(project_root)
        story = tools.get_story(story_id)
        if story:
            story_info = f"""
## Story 详情
- **ID:** {story.id}
- **名称:** {story.name}
- **优先级:** {story.priority}
- **故事点:** {story.points}
- **Sprint:** {story.sprint}
- **状态:** {story.state}
- **当前失败次数:** 测试失败 {story.test_fail_count} 次，审查失败 {story.review_fail_count} 次
"""
    
    # 构建任务描述
    task_description = f"""
## 任务
请执行 Story {story_id} 的开发任务

{project_context}

{story_info}

## 职责
{agent_config['responsibility']}

{agent_config['system_prompt_suffix']}

## 项目路径
{project_root}

## Story Tracker
{project_root}/sprints/*/user-stories-tracker.md

## 参考文档
- 架构: {project_root}/docs/architecture.md
- PRD: {project_root}/docs/prd.md
- 设计模式: {project_root}/design/design-pattern.json

## 注意事项
1. 开发前先读取 user-stories-tracker.md 了解 Story 详情
2. 使用 TDD 方法开发
3. 完成开发后更新 tracker 状态
4. 测试失败 3 次需要人工干预
5. 审查失败 3 次需要人工干预
6. 重要决策记录到 decision-log.md
"""
    
    # 根据 agent_id 确定运行时
    runtime_map = {
        "claude-code": "acp",
        "codex": "acp",
        "gemini": "acp",
        "cursor": "acp"
    }
    
    return {
        "runtime": runtime_map.get(agent_id, "acp"),
        "agentId": agent_id,
        "task": task_description,
        "mode": "session",
        "cwd": project_root
    }


def generate_acp_command(spawn_params: dict) -> str:
    """生成 ACP 调用命令"""
    cmd = [
        "openclaw",
        "sessions-spawn",
        f"--runtime {spawn_params['runtime']}",
        f"--agent-id {spawn_params['agentId']}",
        f"--mode {spawn_params['mode']}",
        f"--cwd {spawn_params['cwd']}",
        "--",
        f"task: {spawn_params['task'][:200]}..."
    ]
    return " ".join(cmd)


def main():
    parser = argparse.ArgumentParser(description="Spawn external dev agent via ACP")
    parser.add_argument("--agent", required=True, 
                       choices=["claude-code", "codex", "gemini", "cursor"],
                       help="目标 Agent ID")
    parser.add_argument("--task", required=True,
                       choices=["dev", "frontend", "backend", "qa", "reviewer", "git"],
                       help="任务类型")
    parser.add_argument("--story-id", required=True,
                       help="Story ID, e.g. STORY-001")
    parser.add_argument("--project", default=".",
                       help="项目根目录路径")
    parser.add_argument("--skill-root", 
                       default=str(Path(__file__).parent.parent),
                       help="NFlow skill 根目录")
    parser.add_argument("--print-only", action="store_true",
                       help="仅打印 JSON，不执行")
    parser.add_argument("--no-context", action="store_true",
                       help="不加载项目上下文")
    parser.add_argument("--full-context", action="store_true",
                       help="使用完整上下文（包含 Sprint 状态、已知问题等）")
    
    args = parser.parse_args()
    
    skill_root = Path(args.skill_root)
    project_root = Path(args.project).resolve()
    
    # 确定上下文模式
    use_context = not args.no_context
    minimal_context = not args.full_context  # 默认使用最小化上下文
    
    # 构建 spawn 参数
    spawn_params = build_spawn_command(
        agent_id=args.agent,
        task_type=args.task,
        story_id=args.story_id,
        skill_root=skill_root,
        project_root=str(project_root),
        minimal_context=minimal_context,
        use_context=use_context
    )
    
    # 输出命令
    print("=" * 60)
    print(f" Spawning {args.agent} for {args.task}")
    print(f" Story: {args.story_id}")
    print(f" Project: {project_root}")
    if use_context:
        if minimal_context:
            print(" Context: ✅ 最小化上下文（仅当前 Story）")
        else:
            print(" Context: ✅ 完整上下文")
    else:
        print(" Context: ❌ 未加载")
    print("=" * 60)
    print()
    
    # 如果是 print-only 模式，只输出 JSON
    if args.print_only:
        print(json.dumps({
            "action": "sessions_spawn",
            "runtime": spawn_params["runtime"],
            "agentId": spawn_params["agentId"],
            "mode": spawn_params["mode"],
            "cwd": spawn_params["cwd"],
            "task_preview": spawn_params["task"][:500] + "..."
        }, indent=2, ensure_ascii=False))
        return
    
    # 输出 JSON 格式（供 LLM 解析）
    print("sessions_spawn 参数：")
    print(json.dumps({
        "action": "sessions_spawn",
        "runtime": spawn_params["runtime"],
        "agentId": spawn_params["agentId"],
        "task": spawn_params["task"],
        "mode": spawn_params["mode"],
        "cwd": spawn_params["cwd"]
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
