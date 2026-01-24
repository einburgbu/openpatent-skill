#!/usr/bin/env python3
"""
合并生成的各部分为完整专利申请草案

用法：python merge_draft.py <outputs_dir>
"""

import sys
from pathlib import Path

SECTIONS = [
    ('01_背景技术.md', '背景技术'),
    ('02_权利要求书.md', '权利要求书'),
    ('03_有益效果.md', '有益效果'),
    ('04_具体实施方式.md', '具体实施方式'),
    ('05_摘要.md', '摘要'),
]

def merge_draft(outputs_dir: str) -> bool:
    dir_path = Path(outputs_dir)
    if not dir_path.exists():
        print(f"错误：目录不存在 - {outputs_dir}", file=sys.stderr)
        return False
    
    content_parts = ['# 专利申请文件\n']
    
    for filename, section_title in SECTIONS:
        file_path = dir_path / filename
        if file_path.exists():
            section_content = file_path.read_text(encoding='utf-8').strip()
            lines = section_content.split('\n')
            if lines and lines[0].startswith('# '):
                lines = lines[1:]
            section_content = '\n'.join(lines).strip()
            content_parts.append(f'\n## {section_title}\n\n{section_content}\n')
        else:
            print(f"警告：缺失 {filename}", file=sys.stderr)
    
    output_path = dir_path / '专利申请草案.md'
    output_path.write_text('\n'.join(content_parts), encoding='utf-8')
    print(f"✓ 已生成: {output_path}")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"用法: {sys.argv[0]} <outputs_dir>")
        sys.exit(1)
    sys.exit(0 if merge_draft(sys.argv[1]) else 1)
