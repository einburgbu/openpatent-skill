#!/usr/bin/env python3
"""
render.py - 将各部分 md 文件合并为完整的专利申请草案

用法：
    python render.py output/case-001_20250123_1430/ -o 专利申请草案.md
    python render.py output/case-001_20250123_1430/  # 输出到 stdout
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


# 文档结构定义
SECTIONS = [
    {
        "file": "05_摘要.md",
        "title": "摘要",
        "required": True
    },
    {
        "file": "02_权利要求书.md",
        "title": "权利要求书",
        "required": True
    },
    {
        "file": "01_背景技术.md",
        "title": "技术领域\n\n[待补充]\n\n## 背景技术",
        "required": True
    },
    {
        "file": "03_有益效果.md",
        "title": "发明内容\n\n[技术问题待补充]\n\n[技术方案待补充]\n\n### 有益效果",
        "required": True
    },
    {
        "file": "04_具体实施方式.md",
        "title": "具体实施方式",
        "required": True
    }
]


def render_patent_document(input_dir: Path) -> str:
    """将各部分文件合并为完整文档"""
    
    parts = []
    
    # 文档头
    case_name = input_dir.name.rsplit('_', 2)[0] if '_' in input_dir.name else input_dir.name
    parts.append(f"# 专利申请文件\n")
    parts.append(f"**案件编号：** {case_name}\n")
    parts.append(f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    parts.append("---\n")
    
    # 逐个部分读取并合并
    for section in SECTIONS:
        file_path = input_dir / section["file"]
        
        if not file_path.exists():
            if section["required"]:
                parts.append(f"## {section['title']}\n")
                parts.append(f"**[错误：缺少文件 {section['file']}]**\n")
            continue
        
        content = file_path.read_text(encoding='utf-8').strip()
        
        # 添加章节标题（如果内容中没有）
        if not content.startswith('#'):
            parts.append(f"## {section['title']}\n")
        
        parts.append(content)
        parts.append("\n\n---\n")
    
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description='合并专利申请文件各部分')
    parser.add_argument('input_dir', type=Path, help='包含各部分 md 文件的目录')
    parser.add_argument('-o', '--output', type=Path, help='输出文件路径（不指定则输出到 stdout）')
    
    args = parser.parse_args()
    
    if not args.input_dir.exists():
        print(f"错误：目录不存在 - {args.input_dir}", file=sys.stderr)
        sys.exit(1)
    
    if not args.input_dir.is_dir():
        print(f"错误：不是目录 - {args.input_dir}", file=sys.stderr)
        sys.exit(1)
    
    document = render_patent_document(args.input_dir)
    
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(document, encoding='utf-8')
        print(f"已保存到：{args.output}")
    else:
        print(document)


if __name__ == '__main__':
    main()
