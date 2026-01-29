# Execution Workflows

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
- **始终从项目根目录执行命令**

---

## Single Case Processing

### Step 1: Configure API

Set up GLM API key:

```bash
# Option 1: Environment variable
export GLM_API_KEY="your-api-key-here"

# Option 2: .env file (in project root)
echo "GLM_API_KEY=your-api-key-here" > .env
```

Get API key from: https://open.bigmodel.cn/

### Step 2: Extract Technical Disclosure

1. Locate the `.docx` file in `input/[case_name]/`
2. Create output directory in `output/[case_name]_$(date +%Y%m%d_%H%M)/`
3. Extract technical disclosure using clean.py:

```bash
# 从项目根目录执行
CASE_NAME="0060"
TIMESTAMP=$(date +%Y%m%d_%H%M)
INPUT_FILE="input/${CASE_NAME}/技术交底书-xxx.docx"
OUTPUT_DIR="output/${CASE_NAME}_${TIMESTAMP}"

.claude/skills/openpatent-skill/scripts/clean.py "$INPUT_FILE" -o "${OUTPUT_DIR}/00_技术交底书.md"
```

### Step 3: Generate Sections Sequentially

Generate each section in order using `generate.py`:

| Order | Output File | Prompt File | Context Files |
|-------|-------------|-------------|---------------|
| 1 | 01_背景技术.md | references/01_背景技术.md | 00_技术交底书.md |
| 2 | 02_权利要求书.md | references/02_权要布局.md | 00 + 01 |
| 3 | 03_有益效果.md | references/03_有益效果.md | 00 + 02 |
| 4 | 04_具体实施方式.md | references/04_具体实施方式.md | 00 + 02 |
| 5 | 05_摘要.md | references/05_摘要.md | 00 + 01 + 02 + 03 + 04 |

**Generation commands:**

```bash
# 从项目根目录执行
# Step 3.1: Background
.claude/skills/openpatent-skill/scripts/generate.py \
    -p .claude/skills/openpatent-skill/references/01_背景技术.md \
    -c "${OUTPUT_DIR}/00_技术交底书.md" \
    -o "${OUTPUT_DIR}/01_背景技术.md"

# Step 3.2: Claims
.claude/skills/openpatent-skill/scripts/generate.py \
    -p .claude/skills/openpatent-skill/references/02_权要布局.md \
    -c "${OUTPUT_DIR}/00_技术交底书.md" \
    -c "${OUTPUT_DIR}/01_背景技术.md" \
    -o "${OUTPUT_DIR}/02_权利要求书.md"

# Step 3.3: Benefits
.claude/skills/openpatent-skill/scripts/generate.py \
    -p .claude/skills/openpatent-skill/references/03_有益效果.md \
    -c "${OUTPUT_DIR}/00_技术交底书.md" \
    -c "${OUTPUT_DIR}/02_权利要求书.md" \
    -o "${OUTPUT_DIR}/03_有益效果.md"

# Step 3.4: Embodiments
.claude/skills/openpatent-skill/scripts/generate.py \
    -p .claude/skills/openpatent-skill/references/04_具体实施方式.md \
    -c "${OUTPUT_DIR}/00_技术交底书.md" \
    -c "${OUTPUT_DIR}/02_权利要求书.md" \
    -o "${OUTPUT_DIR}/04_具体实施方式.md"

# Step 3.5: Abstract
.claude/skills/openpatent-skill/scripts/generate.py \
    -p .claude/skills/openpatent-skill/references/05_摘要.md \
    -c "${OUTPUT_DIR}/00_技术交底书.md" \
    -c "${OUTPUT_DIR}/01_背景技术.md" \
    -c "${OUTPUT_DIR}/02_权利要求书.md" \
    -c "${OUTPUT_DIR}/03_有益效果.md" \
    -c "${OUTPUT_DIR}/04_具体实施方式.md" \
    -o "${OUTPUT_DIR}/05_摘要.md"
```

**Special handling for claims section (02_权利要求书.md):**
If the output contains a `---` separator, `generate.py` will automatically extract the content after `---` to `02_权利要求书_解释.md`.

### Step 4: Merge Output

```bash
# 从项目根目录执行
.claude/skills/openpatent-skill/scripts/render.py "${OUTPUT_DIR}/" -o "${OUTPUT_DIR}/专利申请草案.md"
```

This generates `专利申请草案.md` by merging sections in the correct order.

### Step 5: Copy to Input and Mark as Completed

After patent application file generation is complete:

```bash
# 从项目根目录执行
# Copy final document to input folder
cp "${OUTPUT_DIR}/专利申请草案.md" "input/${CASE_NAME}/"

# Mark case as completed
mv "input/${CASE_NAME}" "input/${CASE_NAME}_已完成"
```

---

## Progress Feedback Format

```
[案件: 0060]
✓ 技术交底书已提取
✓ 背景技术已生成 (395 tokens)
✓ 权利要求书已生成（9条，1185 tokens）
✓ 有益效果已生成
✓ 具体实施方式已生成
✓ 摘要已生成（198字）
✓ 专利申请草案已合并
✓ 输出已保存到: output/0060_20260129_1030/
✓ input 案件已标记: input/0060 → input/0060_已完成
```

**检查清单（完成前必须确认）：**
- [ ] output 目录位于项目根目录，命名包含时间戳：`[case_name]_YYYYMMDD_HHMM`
- [ ] input 已完成案件已标记 `_已完成` 后缀
- [ ] 权利要求书至少 8 条
- [ ] 摘要字数 180-220 字

---

## Important Notes

- **Section order is critical** - Each section depends on previously generated content
- **GLM API required** - Configure `GLM_API_KEY` before generation
- **Claims must have at least 8 items** - Per 02_权要布局.md requirements
- **Abstract word count** - Must be 180-220 characters (200 ± 20)
- **No fabricated data** - Especially in embodiments section
- **Always execute from project root directory** - Paths are relative to project root

---

## Troubleshooting

### API Key Not Found

```
错误: 未找到 GLM_API_KEY
```

Solution:
```bash
export GLM_API_KEY="your-key"
# or create .env file in project root
```

### SOCKS Proxy Error

If you see "socksio" package error, unset the `all_proxy` variable:

```bash
unset all_proxy
```

The HTTP/HTTPS proxies will still work for API calls.

### File Not Found Errors

If you get "file not found" errors:
1. Make sure you are executing from the **project root directory**
2. Check that paths use correct forward slashes: `.claude/skills/openpatent-skill/`
3. Verify `input/` and `output/` directories exist in project root
