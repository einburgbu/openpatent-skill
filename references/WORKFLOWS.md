# Execution Workflows

## Single Case Processing

### Step 1: Extract Technical Disclosure

1. Locate the `.docx` file in the working directory
2. Create output directory: `outputs/[case_name]_$(date +%Y%m%d_%H%M)/`
3. Extract technical disclosure using clean.py:
   ```bash
   python scripts/clean.py "技术交底书.docx" -o "outputs/[case_name]_$(date +%Y%m%d_%H%M)/00_技术交底书.md"
   ```

### Step 2: Generate Sections Sequentially

Generate each section in order. Each section requires reading the corresponding prompt file from `references/`:

| Order | Output File | Prompt File | Context Required |
|-------|-------------|-------------|------------------|
| 1 | 01_背景技术.md | references/01_背景技术.md | 00_技术交底书.md |
| 2 | 02_权利要求书.md | references/02_权要布局.md | 00 + 01 |
| 3 | 03_有益效果.md | references/03_有益效果.md | 00 + 02 |
| 4 | 04_具体实施方式.md | references/04_具体实施方式.md | 00 + 02 |
| 5 | 05_摘要.md | references/05_摘要.md | All previous |

**Generation steps for each section**:
1. Read the corresponding prompt file (e.g., `references/01_背景技术.md`)
2. Read required context files
3. Generate content according to prompt requirements
4. Save to output file

**Special handling for claims section (02_权利要求书.md)**:
If the output contains a `---` separator with explanation content, extract the content after `---` to `02_权利要求书_解释.md`.

### Step 3: Merge Output

```bash
python scripts/render.py outputs/[case_name]_$(date +%Y%m%d_%H%M)/
```

This generates `专利申请草案.md` by merging sections in the correct order.

### Step 4: Output to Final Directory

After patent application file generation is complete:
1. Move results to `output/` directory at the same level as `input/`
2. Rename completed case directories in `input/` by adding `_已完成` suffix

## Progress Feedback Format

```
[案件: DI26-0059-P]
✓ 技术交底书已提取
✓ 背景技术已生成
✓ 权利要求书已生成（10条）
✓ 有益效果已生成
✓ 具体实施方式已生成
✓ 摘要已生成（198字）
✓ 专利申请草案已合并
✓ 输出已保存到: output/DI26-0059-P_20250124_1030/
✓ input 案件已标记: input/DI26-0059-P → input/DI26-0059-P_已完成
```

**检查清单（完成前必须确认）：**
- [ ] output 目录命名包含时间戳：`[case_name]_YYYYMMDD_HHMM`
- [ ] input 已完成案件已标记 `_已完成` 后缀

## Important Notes

- **Section order is critical** - Each section depends on previously generated content
- **Claims must have at least 8 items** - Per 02_权要布局.md requirements
- **Abstract word count** - Must be 180-220 characters (200 ± 20)
- **No fabricated data** - Especially in embodiments section
