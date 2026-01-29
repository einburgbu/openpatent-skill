# Output Directory Structure

## Working Directory Layout

```
工作目录/
├── input/                         ← Input case directories
│   ├── DI26-0059-P/
│   │   └── 技术交底书.docx
│   └── DI26-0060-P/
│       └── 技术交底书.docx
└── output/                        ← Output directory
    ├── DI26-0059-P_20250124_1030/  ← CaseName_YYYYMMDD_HHMM
    │   ├── 00_技术交底书.md
    │   ├── 01_背景技术.md
    │   ├── 02_权利要求书.md
    │   ├── 02_权利要求书_解释.md
    │   ├── 03_有益效果.md
    │   ├── 04_具体实施方式.md
    │   ├── 05_摘要.md
    │   └── 专利申请草案.md
    └── DI26-0060-P_20250124_1031/
        └── ...
```

## File Naming Convention

Output directories follow the pattern: `[案件名]_YYYYMMDD_HHMM/`

**Example**: `DI26-0059-P_20250124_1030/`

- **案件名**: Original case identifier
- **YYYYMMDD**: Date stamp
- **HHMM**: Time stamp

## Section Files

| File | Content | Required |
|------|---------|----------|
| 00_技术交底书.md | Extracted technical disclosure | Yes |
| 01_背景技术.md | Background technology section | Yes |
| 02_权利要求书.md | Claims section | Yes |
| 02_权利要求书_解释.md | Claims explanation (optional) | No |
| 03_有益效果.md | Beneficial effects section | Yes |
| 04_具体实施方式.md | Detailed embodiment section | Yes |
| 05_摘要.md | Abstract section | Yes |
| 专利申请草案.md | Merged final document | Yes |

## Final Output

The `专利申请草案.md` file is the complete patent application draft ready for review and submission.
