# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenPatent is a Chinese patent application document generator that converts technical disclosure documents (技术交底书) from Microsoft Word (.docx) format into complete patent application files in Markdown format. It is designed for patent agents and attorneys working with Chinese patent applications.

**Language**: Primary content is in Chinese (Simplified). Code comments and documentation are mixed Chinese/English.

**Trigger phrases**: "专利生成器", "处理技术交底书", "批量生成专利"

## Directory Structure

```
openpatent/
├── scripts/
│   ├── clean.py      # DOCX → Markdown converter
│   └── render.py     # Merge patent sections into final document
├── references/       # Prompt templates and workflow guides
│   ├── 01_背景技术.md
│   ├── 02_权要布局.md
│   ├── 03_有益效果.md
│   ├── 04_具体实施方式.md
│   ├── 05_摘要.md
│   ├── WORKFLOWS.md
│   ├── SECTION-ORDER.md
│   ├── OUTPUT-STRUCTURE.md
│   └── BATCH-PROCESSING.md
├── SKILL.md          # Main skill definition (YAML frontmatter + concise guide)
└── CLAUDE.md         # This file - development guide
```

**Note**: The `prompts/` directory was renamed to `references/` to follow skill-creator best practices. Prompt templates are reference material that gets loaded as needed.

## Dependencies

```bash
pip install mammoth      # DOCX to HTML conversion
pip install markdownify  # HTML to Markdown conversion
```

**Note**: There is no requirements.txt, pyproject.toml, or package.json. Dependencies are documented in script docstrings.

## Core Workflow

The patent generation process follows a sequential pipeline:

1. **Extract**: Use `clean.py` to convert .docx to Markdown
2. **Generate**: Sequentially generate 5 patent sections using AI prompts
3. **Merge**: Use `render.py` to combine sections into final document

### Section Generation Order (Critical)

Each section depends on previously generated content. This order MUST be followed:

| Order | Output File | Prompt File | Context Required |
|-------|-------------|-------------|------------------|
| 1 | 01_背景技术.md | references/01_背景技术.md | 00_技术交底书.md |
| 2 | 02_权利要求书.md | references/02_权要布局.md | 00 + 01 |
| 3 | 03_有益效果.md | references/03_有益效果.md | 00 + 02 |
| 4 | 04_具体实施方式.md | references/04_具体实施方式.md | 00 + 02 |
| 5 | 05_摘要.md | references/05_摘要.md | All previous |

### Final Document Section Order

When `render.py` merges sections, it uses this specific order (defined in SECTIONS constant):

1. 摘要 (Abstract) - **First**
2. 权利要求书 (Claims)
3. 背景技术 (Background) - with "技术领域" placeholder
4. 有益效果 (Beneficial Effects) - with "技术问题/技术方案" placeholders
5. 具体实施方式 (Embodiment)

## Script Usage

### clean.py - Convert DOCX to Markdown

```bash
# Output to file
python scripts/clean.py "技术交底书.docx" -o "outputs/[case_name]_$(date +%Y%m%d_%H%M)/00_技术交底书.md"

# Output to stdout
python scripts/clean.py "技术交底书.docx"
```

**What it does**:
- Uses mammoth to convert DOCX → HTML
- Uses markdownify to convert HTML → Markdown
- Removes excessive blank lines (preserves single blank lines)
- Strips anchor tags (`<a>`) during conversion

### render.py - Merge Patent Sections

```bash
# Output to file (creates 专利申请草案.md in the input directory)
python scripts/render.py outputs/[case_name]_$(date +%Y%m%d_%H%M)/

# Custom output path
python scripts/render.py outputs/[case_name]_$(date +%Y%m%d_%H%M)/ -o custom/path.md
```

**What it does**:
- Reads numbered section files (01-05)
- Adds document header with case name and timestamp
- Merges in predefined order
- Handles missing required files with error messages

## Special Handling

### Claims Section (02_权利要求书.md)

The claims prompt output may contain a `---` separator. Content after the separator should be extracted to `02_权利要求书_解释.md` (explanation file).

### Claims Requirements (from references/02_权要布局.md)

- **Minimum 8 claims** required
- Claim 1 must be independent with broadest protection scope
- Dependent claims must form proper hierarchy
- Step-based claims use format: `S1：...；S2：...；S3：...。`
- No subheadings within claims

### Embodiment Requirements (from references/04_具体实施方式.md)

- **禁止编造案例，尤其禁止编造数据** (Do not fabricate examples/data)
- Use continuous paragraph form, no numbered lists
- No component/feature numbering

### Abstract Requirements (from references/05_摘要.md)

- **180-220 characters** (200 ± 20)

## Output Directory Convention

Output directories should be named: `[案件名]_YYYYMMDD_HHMM/`

Example: `DI26-0059-P_20250124_1030/`

## Development Notes

- **No test suite** - Manual testing with real patent documents
- **No CI/CD** configuration
- Scripts are self-contained with comprehensive docstrings
- Error messages are in Chinese for user-facing output

## Key Architectural Insight

The design separates concerns cleanly:
1. **clean.py** handles proprietary format conversion (DOCX → MD)
2. **references/** contain domain knowledge for patent writing (prompts and workflows)
3. **render.py** orchestrates final assembly with proper ordering

This allows prompts to be versioned alongside code and enables sequential AI generation where each step builds on previous outputs.

## Skill Structure Best Practices

This project follows the skill-creator best practices:
- **Progressive disclosure**: SKILL.md is concise (~70 lines), detailed content in references/
- **References directory**: Contains prompt templates (01-05_*.md) and workflow guides
- **No redundant documentation**: Only SKILL.md, CLAUDE.md (this file), scripts/, and references/
- **YAML frontmatter**: English description for clarity, includes trigger phrases
