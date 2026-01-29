# Batch Processing

## Processing Multiple Cases

To process multiple cases in batch, iterate through all subdirectories containing `.docx` files:

```bash
for dir in */; do
    if ls "$dir"/*.docx 1>/dev/null 2>&1; then
        # Process this directory
        case_name=$(basename "$dir" .docx)
        timestamp=$(date +%Y%m%d_%H%M)
        output_dir="outputs/${case_name}_${timestamp}"

        # Step 1: Extract
        python scripts/clean.py "$dir"/*.docx -o "${output_dir}/00_技术交底书.md"

        # Step 2-5: Generate sections (manual or via script)
        # ...

        # Step 6: Merge
        python scripts/render.py "${output_dir}/"

        # Step 7: Move to output/
        mv "${output_dir}" "../output/${case_name}_${timestamp}/"

        # Step 8: Mark input as complete
        mv "$dir" "${dir}_已完成"
    fi
done
```

## Batch Processing Workflow

For each case directory:
1. Extract technical disclosure from `.docx`
2. Generate all 5 sections sequentially
3. Merge into final document
4. Move to `output/` directory
5. Mark input directory as completed

## Automation Considerations

- **Error handling**: Check for missing required files before proceeding
- **Progress tracking**: Print status for each case
- **Parallel processing**: Cases can be processed independently (if resources allow)

## Completed Input Handling

After successful processing, rename the input directory by appending `_已完成`:

```bash
input/DI26-0059-P/ → input/DI26-0059-P_已完成/
```

This distinguishes processed from unprocessed cases.
