#!/usr/bin/env python3
"""
clean.py - 将 docx 文件转换为 markdown 格式

用法：
    python clean.py input.docx -o output.md
    python clean.py input.docx  # 输出到 stdout
"""

import argparse
import sys
from pathlib import Path

try:
    import mammoth
except ImportError:
    print("错误：请先安装 mammoth 库")
    print("运行：pip install mammoth")
    sys.exit(1)

try:
    from markdownify import markdownify as md
except ImportError:
    print("错误：请先安装 markdownify 库")
    print("运行：pip install markdownify")
    sys.exit(1)


def docx_to_markdown(docx_path: Path) -> str:
    """将 docx 文件转换为 markdown 格式"""
    with open(docx_path, "rb") as f:
        result = mammoth.convert_to_html(f)
        html = result.value
    
    markdown = md(html, heading_style="ATX", strip=['a'])
    
    # 清理多余空行
    lines = markdown.split('\n')
    cleaned = []
    prev_empty = False
    for line in lines:
        is_empty = line.strip() == ''
        if is_empty and prev_empty:
            continue
        cleaned.append(line)
        prev_empty = is_empty
    
    return '\n'.join(cleaned).strip()


def main():
    parser = argparse.ArgumentParser(description='将 docx 转换为 markdown')
    parser.add_argument('input', type=Path, help='输入的 docx 文件路径')
    parser.add_argument('-o', '--output', type=Path, help='输出的 md 文件路径（不指定则输出到 stdout）')
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"错误：文件不存在 - {args.input}", file=sys.stderr)
        sys.exit(1)
    
    if args.input.suffix.lower() != '.docx':
        print(f"错误：不支持的文件格式 - {args.input.suffix}", file=sys.stderr)
        sys.exit(1)
    
    markdown = docx_to_markdown(args.input)
    
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding='utf-8')
        print(f"已保存到：{args.output}")
    else:
        print(markdown)


if __name__ == '__main__':
    main()
