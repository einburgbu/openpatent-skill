---
name: patent-generator
description: 'Chinese patent application document generator that converts technical disclosure documents (.docx) into complete patent application files in Markdown. Supports single case processing and batch processing. Generates background, claims, beneficial effects, embodiments, and abstract sections. Trigger phrases: "专利生成器", "处理技术交底书", "批量生成专利". Use when user needs to generate patent documents from technical disclosures.'
---

# Patent Application Generator

Convert technical disclosure documents (.docx) into complete patent application files in Chinese.

## Quick Start

```bash
# Step 1: Extract disclosure (output dir MUST include timestamp: YYYYMMDD_HHMM)
python scripts/clean.py "技术交底书.docx" -o "outputs/[case_name]_$(date +%Y%m%d_%H%M)/00_技术交底书.md"

# Step 2: Generate sections sequentially (see references below)
# - 01_背景技术.md
# - 02_权利要求书.md
# - 03_有益效果.md
# - 04_具体实施方式.md
# - 05_摘要.md

# Step 3: Merge into final document
python scripts/render.py outputs/[case_name]_$(date +%Y%m%d_%H%M)/

# Step 4: Mark input case as completed (add "_已完成" suffix)
mv input/[case_name] input/[case_name]_已完成
```

## Dependencies

```bash
pip install mammoth markdownify
```

## Reference Materials

Detailed guides for each aspect of the workflow:

| Topic | Reference |
|-------|-----------|
| Complete execution workflow | [references/WORKFLOWS.md](references/WORKFLOWS.md) |
| Section order and merging | [references/SECTION-ORDER.md](references/SECTION-ORDER.md) |
| Output directory structure | [references/OUTPUT-STRUCTURE.md](references/OUTPUT-STRUCTURE.md) |
| Batch processing guide | [references/BATCH-PROCESSING.md](references/BATCH-PROCESSING.md) |

## Scripts

- **`clean.py`** - Convert DOCX to Markdown (extracts technical disclosure)
- **`render.py`** - Merge sections into final patent application document

## Section Generation

Generate sections in order using prompt files from `references/`:

1. Background → [references/01_背景技术.md](references/01_背景技术.md)
2. Claims → [references/02_权要布局.md](references/02_权要布局.md)
3. Benefits → [references/03_有益效果.md](references/03_有益效果.md)
4. Embodiments → [references/04_具体实施方式.md](references/04_具体实施方式.md)
5. Abstract → [references/05_摘要.md](references/05_摘要.md)

**Important**: Each section depends on previously generated content. Follow the order above.

## Special Handling

- **Claims section**: May contain `---` separator. Content after separator goes to `02_权利要求书_解释.md`
- **Claims requirement**: At least 8 claims required
- **Abstract word count**: 180-220 characters (200 ± 20)
- **Embodiments**: No fabricated data or examples
