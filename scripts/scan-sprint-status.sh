#!/bin/bash
# scan-sprint-status.sh
# 扫描所有 Sprint 的 user-stories-tracker.md，汇总状态
# 用法: ./scripts/scan-sprint-status.sh [sprints目录]

set -e

SPRINTS_DIR="${1:-sprints}"

echo "============================================"
echo "  Sprint 状态扫描"
echo "============================================"
echo ""

if [[ ! -d "$SPRINTS_DIR" ]]; then
    echo "❌ 目录不存在: $SPRINTS_DIR"
    exit 1
fi

# 统计变量
total_sprints=0
total_stories=0
done_stories=0
in_progress_stories=0
review_stories=0
testing_stories=0
todo_stories=0
blocked_stories=0

# 遍历所有 sprint 目录
for sprint_dir in "$SPRINTS_DIR"/sprint-*; do
    if [[ ! -d "$sprint_dir" ]]; then
        continue
    fi
    
    sprint_name=$(basename "$sprint_dir")
    tracker_file="$sprint_dir/user-stories-tracker.md"
    
    if [[ ! -f "$tracker_file" ]]; then
        echo "⚠️ 跳过 $sprint_name (无 tracker 文件)"
        continue
    fi
    
    total_sprints=$((total_sprints + 1))
    echo "📋 $sprint_name"
    echo "   文件: $tracker_file"
    
    # 统计该 sprint 的 stories
    sprint_total=0
    sprint_done=0
    sprint_in_progress=0
    sprint_review=0
    sprint_testing=0
    sprint_todo=0
    sprint_blocked=0
    
    # 解析 markdown 表格（跳过表头和分隔线）
    while IFS= read -r line; do
        # 匹配状态 emoji
        if [[ "$line" =~ \|.*✅\ DONE ]]; then
            sprint_done=$((sprint_done + 1))
            total_stories=$((total_stories + 1))
            done_stories=$((done_stories + 1))
            sprint_total=$((sprint_total + 1))
        elif [[ "$line" =~ \|.*🔄\ IN_PROGRESS ]]; then
            sprint_in_progress=$((sprint_in_progress + 1))
            total_stories=$((total_stories + 1))
            in_progress_stories=$((in_progress_stories + 1))
            sprint_total=$((sprint_total + 1))
        elif [[ "$line" =~ \|.*🔍\ CODE_REVIEW ]]; then
            sprint_review=$((sprint_review + 1))
            total_stories=$((total_stories + 1))
            review_stories=$((review_stories + 1))
            sprint_total=$((sprint_total + 1))
        elif [[ "$line" =~ \|.*🧪\ TESTING ]]; then
            sprint_testing=$((sprint_testing + 1))
            total_stories=$((total_stories + 1))
            testing_stories=$((testing_stories + 1))
            sprint_total=$((sprint_total + 1))
        elif [[ "$line" =~ \|.*⏳\ TODO ]]; then
            sprint_todo=$((sprint_todo + 1))
            total_stories=$((total_stories + 1))
            todo_stories=$((todo_stories + 1))
            sprint_total=$((sprint_total + 1))
        elif [[ "$line" =~ \|.*🚫\ BLOCKED ]]; then
            sprint_blocked=$((sprint_blocked + 1))
            total_stories=$((total_stories + 1))
            blocked_stories=$((blocked_stories + 1))
            sprint_total=$((sprint_total + 1))
        fi
    done < <(grep -E "✅ DONE|🔄 IN_PROGRESS|🔍 CODE_REVIEW|🧪 TESTING|⏳ TODO|🚫 BLOCKED" "$tracker_file")
    
    # 计算完成率
    if [[ $sprint_total -gt 0 ]]; then
        percent=$((sprint_done * 100 / sprint_total))
        echo "   进度: $sprint_done/$sprint_total ($percent%)"
        echo "   详情: 🔄$sprint_in_progress | 🔍$sprint_review | 🧪$sprint_testing | ⏳$sprint_todo | 🚫$sprint_blocked"
    else
        echo "   进度: 无 Stories"
    fi
    echo ""
done

# 输出汇总
echo "============================================"
echo "  汇总"
echo "============================================"
echo "  Sprint 总数: $total_sprints"
echo "  Story 总数: $total_stories"
echo ""
echo "  状态分布:"
echo "    ✅ DONE:        $done_stories"
echo "    🔄 IN_PROGRESS: $in_progress_stories"
echo "    🔍 CODE_REVIEW: $review_stories"
echo "    🧪 TESTING:     $testing_stories"
echo "    ⏳ TODO:        $todo_stories"
echo "    🚫 BLOCKED:     $blocked_stories"
echo ""

# 计算总完成率
if [[ $total_stories -gt 0 ]]; then
    total_percent=$((done_stories * 100 / total_stories))
    echo "  总体完成率: $total_percent% ($done_stories/$total_stories)"
fi

echo ""

# 检查是否有需要人工干预的情况
if [[ $blocked_stories -gt 0 ]]; then
    echo "⚠️  有 $blocked_stories 个 Story 被阻塞，需要人工干预"
fi

if [[ $review_stories -gt 2 ]]; then
    echo "⚠️  有 $review_stories 个 Story 在审查中，注意跟踪"
fi

# 找出最新有未完成 stories 的 sprint
echo ""
echo "============================================"
echo "  下一步建议"
echo "============================================"

next_sprint=""
for sprint_dir in "$SPRINTS_DIR"/sprint-*; do
    if [[ ! -d "$sprint_dir" ]]; then
        continue
    fi
    
    sprint_name=$(basename "$sprint_dir")
    tracker_file="$sprint_dir/user-stories-tracker.md"
    
    if [[ ! -f "$tracker_file" ]]; then
        continue
    fi
    
    # 检查是否有未完成的 story
    remaining=$(grep -cE "🔄 IN_PROGRESS|🔍 CODE_REVIEW|🧪 TESTING|⏳ TODO|🚫 BLOCKED" "$tracker_file" 2>/dev/null || echo "0")
    
    if [[ $remaining -gt 0 ]]; then
        next_sprint="$sprint_name"
        # 继续检查后续 sprint
        for later_sprint_dir in "$SPRINTS_DIR"/sprint-*; do
            later_name=$(basename "$later_sprint_dir")
            if [[ "$later_sprint_dir" > "$sprint_dir" ]]; then
                later_tracker="$later_sprint_dir/user-stories-tracker.md"
                later_remaining=$(grep -cE "🔄 IN_PROGRESS|🔍 CODE_REVIEW|🧪 TESTING|⏳ TODO|🚫 BLOCKED" "$later_tracker" 2>/dev/null || echo "0")
                if [[ $later_remaining -gt 0 ]]; then
                    next_sprint="$later_name (更新)"
                fi
            fi
        done
        break
    fi
done

if [[ -n "$next_sprint" ]]; then
    echo "  继续 Sprint: $next_sprint"
    echo "  命令: /nflow-dev"
elif [[ $todo_stories -gt 0 ]]; then
    echo "  需要规划新 Sprint"
    echo "  命令: /nflow-plan"
else
    echo "  ✅ 所有 Sprint 已完成！"
fi

echo ""
