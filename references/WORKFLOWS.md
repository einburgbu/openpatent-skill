# Execution Workflows

## Single Case Processing

### Step 1: Configure API

Set up GLM API key:

```bash
# Option 1: Environment variable
export GLM_API_KEY="your-api-key-here"

# Option 2: .env file
echo "GLM_API_KEY=your-api-key-here" > .env
```

Get API key from: https://open.bigmodel.cn/

### Step 2: Extract Technical Disclosure

1. Locate the `.docx` file in the working directory
2. Create output directory: `outputs/[case_name]_$(date +%Y%m%d_%H%M)/`
3. Extract technical disclosure using clean.py:
   ```bash
   python scripts/clean.py "技术交底书.docx" -o "outputs/[case_name]_$(date +%Y%m%d_%H%M)/00_技术交底书.md"
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
# Set output directory variable
OUT="outputs/[case_name]_$(date +%Y%m%d_%H%M)"

# Step 3.1: Background
python scripts/generate.py \
    --prompt references/01_背景技术.md \
    --context "$OUT/00_技术交底书.md" \
    --output "$OUT/01_背景技术.md"

# Step 3.2: Claims
python scripts/generate.py \
    --prompt references/02_权要布局.md \
    --context "$OUT/00_技术交底书.md" \
    --context "$OUT/01_背景技术.md" \
    --output "$OUT/02_权利要求书.md"

# Step 3.3: Benefits
python scripts/generate.py \
    --prompt references/03_有益效果.md \
    --context "$OUT/00_技术交底书.md" \
    --context "$OUT/02_权利要求书.md" \
    --output "$OUT/03_有益效果.md"

# Step 3.4: Embodiments
python scripts/generate.py \
    --prompt references/04_具体实施方式.md \
    --context "$OUT/00_技术交底书.md" \
    --context "$OUT/02_权利要求书.md" \
    --output "$OUT/04_具体实施方式.md"

# Step 3.5: Abstract
python scripts/generate.py \
    --prompt references/05_摘要.md \
    --context "$OUT/00_技术交底书.md" \
    --context "$OUT/01_背景技术.md" \
    --context "$OUT/02_权利要求书.md" \
    --context "$OUT/03_有益效果.md" \
    --context "$OUT/04_具体实施方式.md" \
    --output "$OUT/05_摘要.md"
```

**Special handling for claims section (02_权利要求书.md):**
If the output contains a `---` separator, `generate.py` will automatically extract the content after `---` to `02_权利要求书_解释.md`.

### Step 4: Merge Output

```bash
python scripts/render.py outputs/[case_name]_$(date +%Y%m%d_%H%M)/
```

This generates `专利申请草案.md` by merging sections in the correct order.

### Step 5: Mark as Completed

After patent application file generation is complete, rename the input case directory by adding `_已完成` suffix:

```bash
mv input/[case_name] input/[case_name]_已完成
```

## Progress Feedback Format

```
[案件: DI26-0059-P]
✓ 技术交底书已提取
✓ 背景技术已生成 (395 tokens)
✓ 权利要求书已生成（9条，1185 tokens）
✓ 有益效果已生成
✓ 具体实施方式已生成
✓ 摘要已生成（198字）
✓ 专利申请草案已合并
✓ 输出已保存到: outputs/DI26-0059-P_20250129_1030/
✓ input 案件已标记: input/DI26-0059-P → input/DI26-0059-P_已完成
```

**检查清单（完成前必须确认）：**
- [ ] output 目录命名包含时间戳：`[case_name]_YYYYMMDD_HHMM`
- [ ] input 已完成案件已标记 `_已完成` 后缀
- [ ] 权利要求书至少 8 条
- [ ] 摘要字数 180-220 字

## Important Notes

- **Section order is critical** - Each section depends on previously generated content
- **GLM API required** - Configure `GLM_API_KEY` before generation
- **Claims must have at least 8 items** - Per 02_权要布局.md requirements
- **Abstract word count** - Must be 180-220 characters (200 ± 20)
- **No fabricated data** - Especially in embodiments section

## Troubleshooting

### API Key Not Found

```
错误: 未找到 GLM_API_KEY
```

Solution:
```bash
export GLM_API_KEY="your-key"
# or create .env file
```

### SOCKS Proxy Error

If you see "socksio" package error, unset the `all_proxy` variable:

```bash
unset all_proxy
```

The HTTP/HTTPS proxies will still work for API calls.
