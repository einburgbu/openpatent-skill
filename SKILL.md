---
name: patent-generator
description: 'Chinese patent application document generator that converts technical disclosure documents (.docx) into complete patent application files in Markdown. Supports single case processing and batch processing. Generates background, claims, beneficial effects, embodiments, and abstract sections using GLM API. Trigger phrases: "专利生成器", "处理技术交底书", "批量生成专利". Use when user needs to generate patent documents from technical disclosures.'
---

# Patent Application Generator

Convert technical disclosure documents (.docx) into complete patent application files in Chinese.

## Directory Structure

```
项目根目录/
├── input/                    # 输入：待处理的技术交底书 (.docx)
│   ├── 0060/
│   │   └── 技术交底书-xxx.docx
│   └── 0060_已完成/          # 处理完成后添加 "_已完成" 后缀
│       └── 专利申请草案.md   # 最终生成的专利文件
├── output/                   # 输出：生成的专利章节和最终文档
│   └── 0060_20260129_0000/
│       ├── 00_技术交底书.md
│       ├── 01_背景技术.md
│       ├── 02_权利要求书.md
│       ├── 03_有益效果.md
│       ├── 04_具体实施方式.md
│       ├── 05_摘要.md
│       └── 专利申请草案.md   # 合并后的完整文档
└── .claude/
    └── skills/
        └── openpatent-skill/ # 本技能目录
            ├── scripts/       # 执行脚本
            └── references/    # 提示词模板和参考文档
```

**重要说明**：
- `input/` 和 `output/` 位于**项目根目录**，与 `.claude/` 同级
- `scripts/` 和 `references/` 位于 `.claude/skills/openpatent-skill/` 下
- 始终从**项目根目录**执行命令

## Quick Start

```bash
# Step 0: Install dependencies
pip install mammoth markdownify anthropic

# Step 1: Configure GLM API Key
export GLM_API_KEY="your-api-key-here"
# Or create .env file with: GLM_API_KEY=your-key

# Step 2: Set paths (从项目根目录执行)
CASE_NAME="0060"
TIMESTAMP=$(date +%Y%m%d_%H%M)
INPUT_FILE="input/${CASE_NAME}/技术交底书-xxx.docx"
OUTPUT_DIR="output/${CASE_NAME}_${TIMESTAMP}"

# Step 3: Extract disclosure
.claude/skills/openpatent-skill/scripts/clean.py "$INPUT_FILE" -o "${OUTPUT_DIR}/00_技术交底书.md"

# Step 4: Generate sections sequentially using GLM API
.claude/skills/openpatent-skill/scripts/generate.py -p .claude/skills/openpatent-skill/references/01_背景技术.md -c "${OUTPUT_DIR}/00_技术交底书.md" -o "${OUTPUT_DIR}/01_背景技术.md"

.claude/skills/openpatent-skill/scripts/generate.py -p .claude/skills/openpatent-skill/references/02_权要布局.md -c "${OUTPUT_DIR}/00_技术交底书.md" -c "${OUTPUT_DIR}/01_背景技术.md" -o "${OUTPUT_DIR}/02_权利要求书.md"

.claude/skills/openpatent-skill/scripts/generate.py -p .claude/skills/openpatent-skill/references/03_有益效果.md -c "${OUTPUT_DIR}/00_技术交底书.md" -c "${OUTPUT_DIR}/02_权利要求书.md" -o "${OUTPUT_DIR}/03_有益效果.md"

.claude/skills/openpatent-skill/scripts/generate.py -p .claude/skills/openpatent-skill/references/04_具体实施方式.md -c "${OUTPUT_DIR}/00_技术交底书.md" -c "${OUTPUT_DIR}/02_权利要求书.md" -o "${OUTPUT_DIR}/04_具体实施方式.md"

.claude/skills/openpatent-skill/scripts/generate.py -p .claude/skills/openpatent-skill/references/05_摘要.md -c "${OUTPUT_DIR}/00_技术交底书.md" -c "${OUTPUT_DIR}/01_背景技术.md" -c "${OUTPUT_DIR}/02_权利要求书.md" -c "${OUTPUT_DIR}/03_有益效果.md" -c "${OUTPUT_DIR}/04_具体实施方式.md" -o "${OUTPUT_DIR}/05_摘要.md"

# Step 5: Merge into final document
.claude/skills/openpatent-skill/scripts/render.py "${OUTPUT_DIR}/" -o "${OUTPUT_DIR}/专利申请草案.md"

# Step 6: Copy to input folder and mark as completed
cp "${OUTPUT_DIR}/专利申请草案.md" "input/${CASE_NAME}/"
mv "input/${CASE_NAME}" "input/${CASE_NAME}_已完成"
```

## Dependencies

```bash
pip install mammoth markdownify anthropic
```

## Configuration

Create `.env` file in project root:
```
GLM_API_KEY=your-api-key-here
```

Get API key from: https://open.bigmodel.cn/

## Reference Materials

Detailed guides for each aspect of the workflow:

| Topic | Reference |
|-------|-----------|
| Complete execution workflow | [references/WORKFLOWS.md](references/WORKFLOWS.md) |
| GLM API generation guide | [references/API-GENERATION.md](references/API-GENERATION.md) |
| Section order and merging | [references/SECTION-ORDER.md](references/SECTION-ORDER.md) |
| Output directory structure | [references/OUTPUT-STRUCTURE.md](references/OUTPUT-STRUCTURE.md) |
| Batch processing guide | [references/BATCH-PROCESSING.md](references/BATCH-PROCESSING.md) |

## Scripts

- **`clean.py`** - Convert DOCX to Markdown (extracts technical disclosure)
- **`generate.py`** - Generate patent sections using GLM API
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

- **Claims section**: May contain `---` separator. Content after separator goes to `02_权利要求书_解释.md` (automatically handled by `generate.py`)
- **Claims requirement**: At least 8 claims required
- **Abstract word count**: 180-220 characters (200 ± 20)
- **Embodiments**: No fabricated data or examples
