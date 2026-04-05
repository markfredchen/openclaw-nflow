#!/usr/bin/env python3
"""
generate_html_report.py
生成 HTML 报告

用法:
    python3 generate_html_report.py --template <template.html> --data <data.json> --output <output.html>

示例:
    python3 generate_html_report.py \
        --template templates/acceptance-report-template.html \
        --data '{"story_id": "STORY-001", "passed": 5, "failed": 1}' \
        --output sprints/sprint-01/acceptance-report-001.html
"""

import json
import sys
import re
from pathlib import Path
from typing import Any, Dict
from argparse import ArgumentParser


def load_template(template_path: str) -> str:
    """加载 HTML 模板"""
    path = Path(template_path)
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return path.read_text(encoding='utf-8')


def load_data(data_path: str) -> Dict[str, Any]:
    """加载数据（JSON 文件或 JSON 字符串）"""
    path = Path(data_path)
    
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    else:
        # Try as JSON string
        try:
            return json.loads(data_path)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON: {data_path}")


def flatten_dict(d: Dict, parent_key: str = '', sep: '.') -> Dict:
    """扁平化字典，用于替换占位符"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}.{i}", sep=sep).items())
                else:
                    items.append((f"{new_key}.{i}", item))
        else:
            items.append((new_key, v))
    return dict(items)


def replace_placeholders(template: str, data: Dict) -> str:
    """替换模板中的占位符"""
    # 支持多种占位符格式: {key}, {{key}}, ${key}
    result = template
    
    # 扁平化数据
    flat_data = flatten_dict(data)
    
    # 替换 {key} 格式
    for key, value in flat_data.items():
        # 跳过复杂类型，只处理字符串和数字
        if isinstance(value, (str, int, float)):
            result = result.replace(f"{{{key}}}", str(value))
            result = result.replace(f"{{{{{key}}}}}", str(value))
            result = result.replace(f"${{{key}}}", str(value))
    
    return result


def generate_list_section(template: str, items: list, item_key: str) -> str:
    """生成列表 sections"""
    # 找到 section 模板
    pattern = rf"{{#{item_key}}}(.*?){{/{item_key}}}"
    match = re.search(pattern, template, re.DOTALL)
    
    if not match:
        return template
    
    section_template = match.group(1)
    item_pattern = rf"{{#{item_key}_item}}(.*?){{/{item_key}_item}}"
    
    items_html = ""
    for i, item in enumerate(items):
        if isinstance(item, dict):
            item_html = item_pattern
            for k, v in flatten_dict(item).items():
                item_html = item_html.replace(f"{{{k}}}", str(v))
                item_html = item_html.replace(f"{{{{{k}}}}}", str(v))
            items_html += item_html
        else:
            items_html += f"<li>{item}</li>"
    
    # 替换整个 section
    section_pattern = rf"{{#{item_key}}}(.*?){{/{item_key}}}"
    result = re.sub(section_pattern, items_html, template, flags=re.DOTALL)
    
    return result


def process_template(template: str, data: Dict) -> str:
    """处理完整模板"""
    result = template
    
    # 处理列表 sections
    list_sections = ['test_cases', 'stories', 'quality_checks', 'issues', 'next_steps']
    for section in list_sections:
        if section in data:
            if isinstance(data[section], list):
                result = generate_list_section_with_items(result, data[section], section)
    
    # 替换简单占位符
    result = replace_placeholders(result, data)
    
    return result


def generate_list_section_with_items(template: str, items: list, section_key: str) -> str:
    """生成带 items 的列表 section"""
    # 匹配 {{#section}}...{{/section}} 块
    pattern = rf"{{#{section_key}}}(.*?){{/{section_key}}}"
    match = re.search(pattern, template, re.DOTALL)
    
    if not match:
        return template
    
    section_content = match.group(1)
    
    # 检查是否有 item 子模板 {{#item}}...{{/item}}
    item_pattern = rf"{{#{section_key}_item}}(.*?){{/{section_key}_item}}"
    item_match = re.search(item_pattern, section_content, re.DOTALL)
    
    if item_match:
        item_template = item_match.group(1)
        items_html = ""
        
        for item in items:
            if isinstance(item, dict):
                item_html = item_template
                for k, v in flatten_dict(item).items():
                    item_html = item_html.replace(f"{{{k}}}", str(v))
                    item_html = item_html.replace(f"{{{{{k}}}}}", str(v))
                items_html += item_html
            else:
                items_html += f"<div>{item}</div>"
        
        # 替换 item 块
        section_content = re.sub(item_pattern, items_html, section_content, flags=re.DOTALL)
    
    # 替换整个 section 块
    result = re.sub(pattern, section_content, template, flags=re.DOTALL)
    
    return result


def main():
    parser = ArgumentParser(description="Generate HTML report from template")
    parser.add_argument("--template", "-t", required=True, help="HTML template path")
    parser.add_argument("--data", "-d", required=True, help="JSON data file or JSON string")
    parser.add_argument("--output", "-o", required=True, help="Output HTML path")
    
    args = parser.parse_args()
    
    try:
        # 加载模板和数据
        template = load_template(args.template)
        data = load_data(args.data)
        
        # 处理模板
        result = process_template(template, data)
        
        # 输出结果
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding='utf-8')
        
        print(f"✅ Generated: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
