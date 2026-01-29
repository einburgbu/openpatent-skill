# Section Order and Merging

## Final Document Order

When `render.py` merges sections, it follows this specific order (defined in SECTIONS constant):

1. **摘要 (Abstract)** - First section
2. **权利要求书 (Claims)** - Core legal protection
3. **背景技术 (Background)** - Includes "技术领域" placeholder
4. **有益效果 (Beneficial Effects)** - Includes "技术问题/技术方案" placeholders
5. **具体实施方式 (Embodiment)** - Detailed implementation

## Why This Order Matters

The final patent application document must follow Chinese patent office formatting requirements:

- **Abstract comes first** - For quick reference
- **Claims follow** - Most important legal content
- **Background** - Provides context
- **Beneficial Effects** - Explains advantages
- **Embodiments** - Detailed description

## Render.py Section Configuration

```python
SECTIONS = [
    {"file": "05_摘要.md", "title": "摘要", "required": True},
    {"file": "02_权利要求书.md", "title": "权利要求书", "required": True},
    {"file": "01_背景技术.md", "title": "技术领域\n\n[待补充]\n\n## 背景技术", "required": True},
    {"file": "03_有益效果.md", "title": "发明内容\n\n[技术问题待补充]\n\n[技术方案待补充]\n\n### 有益效果", "required": True},
    {"file": "04_具体实施方式.md", "title": "具体实施方式", "required": True}
]
```

## Placeholders

Some sections include placeholder text for missing subsections:
- **Background**: "技术领域" section needs manual completion
- **Benefits**: "技术问题" and "技术方案" sections need manual completion
