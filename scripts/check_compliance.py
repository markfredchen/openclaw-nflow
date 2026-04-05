#!/usr/bin/env python3
"""
NFlow 合规检查脚本
检查项目是否符合 NFlow 工作流规范

用法:
    python3 scripts/nflow_tools.py check-compliance
    python3 scripts/check-compliance.py [项目目录]
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ComplianceResult:
    passed: bool
    file_path: str
    message: str

class NFlowComplianceChecker:
    """NFlow 合规性检查器"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.results: list[ComplianceResult] = []
        self.warnings: list[str] = []
        self.errors: list[str] = []
    
    def check_nflow_marker(self) -> bool:
        """检查 .nflow-phase 文件是否存在"""
        marker = self.project_root / ".nflow-phase"
        if marker.exists():
            self.results.append(ComplianceResult(
                True, ".nflow-phase", "存在"
            ))
            # 读取 PHASE
            content = marker.read_text()
            for line in content.splitlines():
                if line.startswith("PHASE="):
                    phase = line.split("=")[1].strip()
                    self.results.append(ComplianceResult(
                        True, ".nflow-phase", f"当前 Phase: {phase}"
                    ))
                    break
            return True
        else:
            self.results.append(ComplianceResult(
                False, ".nflow-phase", "不存在 - 项目未使用 NFlow"
            ))
            return False
    
    def check_sprint_plan(self) -> bool:
        """检查当前 Sprint plan 是否存在"""
        # 读取 .nflow-phase 获取当前 Sprint
        marker = self.project_root / ".nflow-phase"
        sprint_name = "sprint-01"  # 默认
        
        if marker.exists():
            for line in marker.read_text().splitlines():
                if line.startswith("SPRINT="):
                    sprint_name = line.split("=")[1].strip()
                    break
        
        sprint_plan = self.project_root / "sprints" / sprint_name / "plan.md"
        if sprint_plan.exists():
            self.results.append(ComplianceResult(
                True, f"sprints/{sprint_name}/plan.md", "存在"
            ))
            return True
        else:
            self.results.append(ComplianceResult(
                False, f"sprints/{sprint_name}/plan.md", "不存在"
            ))
            return False
    
    def check_backlog(self) -> bool:
        """检查 Backlog 是否存在"""
        backlog = self.project_root / "sprints" / "backlog" / "stories.md"
        if backlog.exists():
            self.results.append(ComplianceResult(
                True, "sprints/backlog/stories.md", "存在"
            ))
            return True
        else:
            self.results.append(ComplianceResult(
                False, "sprints/backlog/stories.md", "不存在"
            ))
            return False
    
    def check_e2e_setup(self) -> bool:
        """检查 E2E 测试框架是否设置"""
        # 检查常见 E2E 目录
        e2e_dirs = [
            self.project_root / "e2e",
            self.project_root / "tests" / "e2e",
            self.project_root / "cypress",
            self.project_root / "playwright.config",
        ]
        
        for e2e_dir in e2e_dirs:
            if e2e_dir.exists() or e2e_dir.with_suffix(".ts").exists():
                self.results.append(ComplianceResult(
                    True, str(e2e_dir), "存在"
                ))
                return True
        
        self.results.append(ComplianceResult(
            False, "e2e/", "不存在"
        ))
        return False
    
    def check_sprint_review(self) -> bool:
        """检查已完成的 Sprint 是否有 Review"""
        sprints_dir = self.project_root / "sprints"
        if not sprints_dir.exists():
            return True  # 跳过
        
        has_issues = False
        for sprint_dir in sprints_dir.glob("sprint-*"):
            if not sprint_dir.is_dir():
                continue
            tracker = sprint_dir / "user-stories-tracker.md"
            if tracker.exists():
                content = tracker.read_text()
                if "✅" in content or "DONE" in content.upper():
                    # Sprint 已完成，检查是否有 review
                    review = sprint_dir / "review.md"
                    if not review.exists():
                        self.warnings.append(
                            f"⚠️ {sprint_dir.name}/review.md 缺失"
                        )
                        has_issues = True
        
        if not has_issues:
            self.results.append(ComplianceResult(
                True, "sprint reviews", "所有完成的 Sprint 都有 Review"
            ))
        return not has_issues
    
    def check_gitignore(self) -> bool:
        """检查 .gitignore 是否存在"""
        gitignore = self.project_root / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            # 检查是否忽略 node_modules, dist 等
            needed = ["node_modules", "dist", ".env"]
            missing = [x for x in needed if x not in content]
            if missing:
                self.warnings.append(
                    f"⚠️ .gitignore 缺少: {', '.join(missing)}"
                )
                return False
            self.results.append(ComplianceResult(
                True, ".gitignore", "存在且完整"
            ))
            return True
        else:
            self.results.append(ComplianceResult(
                False, ".gitignore", "不存在"
            ))
            return False
    
    def run_all_checks(self) -> bool:
        """运行所有检查"""
        print("=" * 60)
        print(f"NFlow 合规检查 - {self.project_root.name}")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        
        print("📋 检查结果:")
        print("-" * 60)
        
        self.check_nflow_marker()
        self.check_backlog()
        self.check_sprint_plan()
        self.check_gitignore()
        self.check_e2e_setup()
        self.check_sprint_review()
        
        for result in self.results:
            status = "✅" if result.passed else "❌"
            print(f"  {status} {result.file_path}: {result.message}")
        
        if self.warnings:
            print()
            print("⚠️ 警告:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        print()
        print("-" * 60)
        
        # 判断是否通过
        all_passed = all(r.passed for r in self.results)
        if all_passed and not self.warnings:
            print("✅ 项目完全符合 NFlow 规范")
            return True
        elif all_passed and self.warnings:
            print("⚠️ 项目基本符合 NFlow 规范，但有警告")
            return True
        else:
            print("❌ 项目不符合 NFlow 规范，必须修复后才能继续")
            return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="NFlow 合规检查")
    parser.add_argument("project_root", nargs="?", default=None,
                        help="项目根目录路径")
    args = parser.parse_args()
    
    checker = NFlowComplianceChecker(args.project_root)
    passed = checker.run_all_checks()
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
