# Output Directory Structure

## Project Root Layout

```
项目根目录/
├── input/                              ← Input: 待处理的技术交底书
│   ├── 0060/
│   │   └── 技术交底书-xxx.docx
│   ├── 0060_已完成/                     ← 完成后标记
│   │   └── 专利申请草案.md
│   └── 0061/
│       └── 技术交底书-yyy.docx
│
├── output/                             ← Output: 生成的专利文件
│   ├── 0060_20260129_1030/             ← 案件名_YYYYMMDD_HHMM
│   │   ├── 00_技术交底书.md
│   │   ├── 01_背景技术.md
│   │   ├── 02_权利要求书.md
│   │   ├── 02_权利要求书_解释.md        ← 可选
│   │   ├── 03_有益效果.md
│   │   ├── 04_具体实施方式.md
│   │   ├── 05_摘要.md
│   │   └── 专利申请草案.md             ← 最终完整文档
│   └── 0061_20260129_1031/
│       └── ...
│
└── .claude/
    └── skills/
        └── openpatent-skill/            ← 本技能目录
            ├── scripts/
            └── references/
```

## Important Notes

- `input/` 和 `output/` 位于**项目根目录**，与 `.claude/` 同级
- `scripts/` 和 `references/` 位于 `.claude/skills/openpatent-skill/` 下
- **始终从项目根目录执行命令**

---

## File Naming Convention

Output directories follow the pattern: `[案件名]_YYYYMMDD_HHMM/`

**Example**: `0060_20260129_1030/`

- **案件名**: Original case identifier (from input directory name)
- **YYYYMMDD**: Date stamp
- **HHMM**: Time stamp

---

## Section Files

| File | Content | Required |
|------|---------|----------|
| 00_技术交底书.md | Extracted technical disclosure (from .docx) | Yes |
| 01_背景技术.md | Background technology section | Yes |
| 02_权利要求书.md | Claims section (minimum 8 claims) | Yes |
| 02_权利要求书_解释.md | Claims explanation (optional, auto-split) | No |
| 03_有益效果.md | Beneficial effects section | Yes |
| 04_具体实施方式.md | Detailed embodiment section | Yes |
| 05_摘要.md | Abstract section (180-220 characters) | Yes |
| 专利申请草案.md | Merged final document | Yes |

---

## Final Output

The `专利申请草案.md` file is the complete patent application draft ready for review.

**Document structure** (merged by render.py):
1. 摘要 (Abstract)
2. 权利要求书 (Claims)
3. 技术领域 + 背景技术 (Technical Field + Background)
4. 发明内容：技术问题 + 技术方案 + 有益效果 (Invention Content)
5. 具体实施方式 (Embodiments)

---

## File Locations

| Location | Purpose |
|----------|---------|
| `input/[case_name]/` | Original .docx technical disclosure |
| `input/[case_name]_已完成/` | Completed case with final document |
| `output/[case_name]_YYYYMMDD_HHMM/` | Generated sections and working files |
| `.claude/skills/openpatent-skill/` | Skill scripts and templates |
