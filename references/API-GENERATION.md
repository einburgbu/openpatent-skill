# 使用 GLM API 生成专利章节

## 概述

为解决 Claude Code 等 code 工具中的文本压缩问题，项目提供了 `generate.py` 脚本，直接调用 GLM API 生成高质量专利内容。

**API 端点**: `https://open.bigmodel.cn/api/anthropic`
**默认模型**: `glm-4.7`

## 优势

| 对比项 | Code 工具生成 | GLM API 直接生成 |
|--------|--------------|-----------------|
| 输出质量 | 可能有压缩倾向 | 完整详细 |
| 参数控制 | 有限 | 完全控制 |
| 可重复性 | 较低 | 高 |
| 成本透明 | 不确定 | 按实际使用计费 |

## 快速开始

### 1. 安装依赖

```bash
pip install anthropic
```

### 2. 配置 API Key

```bash
# 方式一: 环境变量
export GLM_API_KEY="your-api-key-here"

# 方式二: .env 文件
cp .env.example .env
# 编辑 .env 文件，填入真实 API Key
```

获取 API Key: https://open.bigmodel.cn/

### 3. 生成章节

```bash
# 创建输出目录（带时间戳）
OUTPUT_DIR="outputs/案例名_$(date +%Y%m%d_%H%M)"
mkdir -p "$OUTPUT_DIR"

# 步骤 1: 生成背景技术
python scripts/generate.py \
    --prompt references/01_背景技术.md \
    --context "$OUTPUT_DIR/00_技术交底书.md" \
    --output "$OUTPUT_DIR/01_背景技术.md"

# 步骤 2: 生成权利要求书
python scripts/generate.py \
    --prompt references/02_权要布局.md \
    --context "$OUTPUT_DIR/00_技术交底书.md" \
    --context "$OUTPUT_DIR/01_背景技术.md" \
    --output "$OUTPUT_DIR/02_权利要求书.md"

# 步骤 3: 生成有益效果
python scripts/generate.py \
    --prompt references/03_有益效果.md \
    --context "$OUTPUT_DIR/00_技术交底书.md" \
    --context "$OUTPUT_DIR/02_权利要求书.md" \
    --output "$OUTPUT_DIR/03_有益效果.md"

# 步骤 4: 生成具体实施方式
python scripts/generate.py \
    --prompt references/04_具体实施方式.md \
    --context "$OUTPUT_DIR/00_技术交底书.md" \
    --context "$OUTPUT_DIR/02_权利要求书.md" \
    --output "$OUTPUT_DIR/04_具体实施方式.md"

# 步骤 5: 生成摘要
python scripts/generate.py \
    --prompt references/05_摘要.md \
    --context "$OUTPUT_DIR/00_技术交底书.md" \
    --context "$OUTPUT_DIR/01_背景技术.md" \
    --context "$OUTPUT_DIR/02_权利要求书.md" \
    --context "$OUTPUT_DIR/03_有益效果.md" \
    --context "$OUTPUT_DIR/04_具体实施方式.md" \
    --output "$OUTPUT_DIR/05_摘要.md"

# 步骤 6: 合并最终文档
python scripts/render.py "$OUTPUT_DIR"
```

## 高级用法

### 调整温度参数

```bash
# 较低温度（0.3）- 更确定性，适合需要严格格式的章节
python scripts/generate.py --temperature 0.3 --prompt references/05_摘要.md ...

# 较高温度（0.9）- 更创造性，适合具体实施方式
python scripts/generate.py --temperature 0.9 --prompt references/04_具体实施方式.md ...
```

### Dry Run 模式

预览将要发送的内容，不实际调用 API：

```bash
python scripts/generate.py \
    --prompt references/01_背景技术.md \
    --context outputs/case/00_技术交底书.md \
    --output outputs/case/01_背景技术.md \
    --dry-run
```

## 完整工作流示例

```bash
#!/bin/bash
# 专利生成完整流程

CASE_NAME="DI26-0059-P"
TIMESTAMP=$(date +%Y%m%d_%H%M)
OUTPUT_DIR="outputs/${CASE_NAME}_${TIMESTAMP}"

# 1. 转换技术交底书
python scripts/clean.py "input/${CASE_NAME}.docx" -o "${OUTPUT_DIR}/00_技术交底书.md"

# 2. 生成各部分（按依赖顺序）
python scripts/generate.py -p references/01_背景技术.md -c "${OUTPUT_DIR}/00_技术交底书.md" -o "${OUTPUT_DIR}/01_背景技术.md"

python scripts/generate.py -p references/02_权要布局.md -c "${OUTPUT_DIR}/00_技术交底书.md" -c "${OUTPUT_DIR}/01_背景技术.md" -o "${OUTPUT_DIR}/02_权利要求书.md"

python scripts/generate.py -p references/03_有益效果.md -c "${OUTPUT_DIR}/00_技术交底书.md" -c "${OUTPUT_DIR}/02_权利要求书.md" -o "${OUTPUT_DIR}/03_有益效果.md"

python scripts/generate.py -p references/04_具体实施方式.md -c "${OUTPUT_DIR}/00_技术交底书.md" -c "${OUTPUT_DIR}/02_权利要求书.md" -o "${OUTPUT_DIR}/04_具体实施方式.md"

python scripts/generate.py -p references/05_摘要.md -c "${OUTPUT_DIR}/00_技术交底书.md" -c "${OUTPUT_DIR}/01_背景技术.md" -c "${OUTPUT_DIR}/02_权利要求书.md" -c "${OUTPUT_DIR}/03_有益效果.md" -c "${OUTPUT_DIR}/04_具体实施方式.md" -o "${OUTPUT_DIR}/05_摘要.md"

# 3. 合并最终文档
python scripts/render.py "${OUTPUT_DIR}"

# 4. 标记完成
mv "input/${CASE_NAME}.docx" "input/${CASE_NAME}_已完成.docx"

echo "✅ 专利生成完成: ${OUTPUT_DIR}/专利申请草案.md"
```

## 故障排查

### API Key 未找到

```
错误: 未找到 GLM_API_KEY
```

解决：
```bash
export GLM_API_KEY="your-key"
# 或创建 .env 文件
```

### SOCKS 代理错误

```
Using SOCKS proxy, but the 'socksio' package is not installed
```

解决（临时禁用 SOCKS 代理，HTTP 代理仍可用）：
```bash
unset all_proxy
```

### 文件编码错误

如果技术交底书是 GBK 编码，脚本会自动尝试多种编码。如仍有问题：

```bash
# 转换编码
iconv -f GBK -t UTF-8 input.docx > input_utf8.docx
```

### 输出 token 过多

如果某个章节生成内容过长，可以调整 `MAX_TOKENS` 参数（编辑 generate.py）。

## GLM API 配置

| 配置项 | 值 |
|--------|-----|
| 端点 | `https://open.bigmodel.cn/api/anthropic` |
| 默认模型 | `glm-4.7` |
| 最大 tokens | 8192 |
| 默认温度 | 0.7 |

## 生成质量参考

实际测试数据（智能温控杯垫案例）：

| 章节 | 输入 tokens | 输出 tokens | 质量 |
|------|-------------|-------------|------|
| 背景技术 | ~434 | 395 | 结构清晰，问题突出 |
| 权利要求书 | ~854 | 1185 | 9 条权要，层次分明 |

**注意**: GLM API 生成的内容避免了 code 工具中的文本压缩倾向，质量更高。
