# Batch Processing

## Directory Structure

```
项目根目录/
├── input/                    # 输入：待处理的技术交底书 (.docx)
│   ├── 0060/
│   │   └── 技术交底书-xxx.docx
│   └── 0061/
│       └── 技术交底书-yyy.docx
├── output/                   # 输出：生成的专利章节和最终文档
│   ├── 0060_20260129_0000/
│   └── 0061_20260129_0100/
└── .claude/
    └── skills/
        └── openpatent-skill/ # 本技能目录
            ├── scripts/       # 执行脚本
            └── references/    # 提示词模板和参考文档
```

**重要说明**：
- `input/` 和 `output/` 位于**项目根目录**，与 `.claude/` 同级
- **始终从项目根目录执行命令**

---

## Processing Multiple Cases

To process multiple cases in batch, iterate through all subdirectories in `input/` containing `.docx` files:

```bash
# 从项目根目录执行
for dir in input/*/; do
    # Skip completed directories
    if [[ "$dir" == *"_已完成"* ]]; then
        continue
    fi

    # Check if directory contains .docx files
    if ls "$dir"*.docx 1>/dev/null 2>&1; then
        # Extract case name from directory path
        case_name=$(basename "$dir")
        timestamp=$(date +%Y%m%d_%H%M)
        output_dir="output/${case_name}_${timestamp}"

        echo "Processing: $case_name"

        # Step 1: Extract
        .claude/skills/openpatent-skill/scripts/clean.py "$dir"*.docx -o "${output_dir}/00_技术交底书.md"

        # Step 2-5: Generate sections
        .claude/skills/openpatent-skill/scripts/generate.py \
            -p .claude/skills/openpatent-skill/references/01_背景技术.md \
            -c "${output_dir}/00_技术交底书.md" \
            -o "${output_dir}/01_背景技术.md"

        .claude/skills/openpatent-skill/scripts/generate.py \
            -p .claude/skills/openpatent-skill/references/02_权要布局.md \
            -c "${output_dir}/00_技术交底书.md" \
            -c "${output_dir}/01_背景技术.md" \
            -o "${output_dir}/02_权利要求书.md"

        .claude/skills/openpatent-skill/scripts/generate.py \
            -p .claude/skills/openpatent-skill/references/03_有益效果.md \
            -c "${output_dir}/00_技术交底书.md" \
            -c "${output_dir}/02_权利要求书.md" \
            -o "${output_dir}/03_有益效果.md"

        .claude/skills/openpatent-skill/scripts/generate.py \
            -p .claude/skills/openpatent-skill/references/04_具体实施方式.md \
            -c "${output_dir}/00_技术交底书.md" \
            -c "${output_dir}/02_权利要求书.md" \
            -o "${output_dir}/04_具体实施方式.md"

        .claude/skills/openpatent-skill/scripts/generate.py \
            -p .claude/skills/openpatent-skill/references/05_摘要.md \
            -c "${output_dir}/00_技术交底书.md" \
            -c "${output_dir}/01_背景技术.md" \
            -c "${output_dir}/02_权利要求书.md" \
            -c "${output_dir}/03_有益效果.md" \
            -c "${output_dir}/04_具体实施方式.md" \
            -o "${output_dir}/05_摘要.md"

        # Step 6: Merge
        .claude/skills/openpatent-skill/scripts/render.py "${output_dir}/" -o "${output_dir}/专利申请草案.md"

        # Step 7: Copy to input and mark as complete
        cp "${output_dir}/专利申请草案.md" "$dir"
        mv "$dir" "${dir}_已完成"

        echo "Completed: $case_name -> ${output_dir}"
    fi
done
```

---

## Batch Processing Workflow

For each case directory in `input/`:
1. Extract technical disclosure from `.docx`
2. Generate all 5 sections sequentially
3. Merge into final document
4. Copy final document to input directory
5. Mark input directory as completed (add `_已完成` suffix)

**Output location**: Files are generated directly to `output/[case_name]_YYYYMMDD_HHMM/` in the project root directory.

---

## Automation Considerations

- **Error handling**: Check for missing required files before proceeding
- **Progress tracking**: Print status for each case
- **Parallel processing**: Cases can be processed independently (if API rate limits allow)
- **Skip completed**: The script automatically skips directories ending with `_已完成`

---

## Completed Input Handling

After successful processing, rename the input directory by appending `_已完成`:

```bash
input/0060/ → input/0060_已完成/
input/0061/ → input/0061_已完成/
```

This distinguishes processed from unprocessed cases.
