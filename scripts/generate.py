#!/usr/bin/env python3
"""
专利部分生成器 - 通过 GLM API 生成专利章节

用途：解决 Claude Code 等 code 工具中的文本压缩问题

安装依赖：
    pip install anthropic

配置 API Key：
    export GLM_API_KEY="your-api-key-here"
    # 或创建 .env 文件：GLM_API_KEY=your-key

使用示例：
    # 生成背景技术（仅需技术交底书）
    python scripts/generate.py \\
        --prompt references/01_背景技术.md \\
        --context outputs/case_20250129/00_技术交底书.md \\
        --output outputs/case_20250129/01_背景技术.md

    # 生成权利要求书（需要技术交底书 + 背景技术）
    python scripts/generate.py \\
        --prompt references/02_权要布局.md \\
        --context outputs/case_20250129/00_技术交底书.md \\
        --context outputs/case_20250129/01_背景技术.md \\
        --output outputs/case_20250129/02_权利要求书.md

    # 指定模型（默认 glm-4.7）
    python scripts/generate.py \\
        --model glm-4.7 \\
        --prompt references/01_背景技术.md \\
        --context outputs/case_20250129/00_技术交底书.md \\
        --output outputs/case_20250129/01_背景技术.md
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    print("错误: 未安装 anthropic 库")
    print("请运行: pip install anthropic")
    sys.exit(1)


# 默认模型配置
DEFAULT_MODEL = "glm-4.7"
MAX_TOKENS = 8192  # 足够生成详细的专利内容

# GLM API 端点
GLM_BASE_URL = "https://open.bigmodel.cn/api/anthropic"


def get_api_key():
    """获取 GLM API Key"""
    # 优先从环境变量读取
    api_key = os.environ.get("GLM_API_KEY")
    if api_key:
        return api_key

    # 尝试从 .env 文件读取
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        for line in env_file.read_text().strip().split("\n"):
            if line.startswith("GLM_API_KEY="):
                return line.split("=", 1)[1].strip()

    return None


def read_file_content(file_path: str) -> str:
    """读取文件内容，处理编码问题"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 尝试多种编码
    for encoding in ["utf-8", "gbk", "gb2312"]:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"无法读取文件: {file_path}")


def build_user_message(prompt_template: str, context_files: list[str]) -> str:
    """
    构建发送给 API 的用户消息

    格式：将 prompt 模板放在前面，然后附加上下文文件内容
    """
    parts = []

    # 首先添加 prompt 模板
    prompt_content = read_file_content(prompt_template)
    parts.append(prompt_content)

    # 然后添加上下文文件
    for ctx_file in context_files:
        ctx_content = read_file_content(ctx_file)
        filename = Path(ctx_file).name
        parts.append(f"\n\n## {filename}\n\n{ctx_content}")

    return "".join(parts)


def call_llm_api(prompt_template: str, context_files: list[str], model: str, temperature: float = 0.7) -> str:
    """
    调用 GLM API 生成内容

    Args:
        prompt_template: prompt 模板文件路径
        context_files: 上下文文件路径列表
        model: 模型名称
        temperature: 温度参数（0-1），控制输出随机性

    Returns:
        生成的文本内容
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "未找到 GLM_API_KEY\n"
            "请设置环境变量或创建 .env 文件\n"
            "格式: GLM_API_KEY=your-key"
        )

    # 使用自定义 base_url 连接 GLM API
    client = Anthropic(
        api_key=api_key,
        base_url=GLM_BASE_URL
    )

    # 构建消息
    user_message = build_user_message(prompt_template, context_files)

    print(f"📤 正在调用模型: {model}")
    print(f"🌐 API 端点: {GLM_BASE_URL}")
    print(f"📝 输入 token 数约: {len(user_message) // 3} (估算)")

    # 调用 API
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        temperature=temperature,
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    content = response.content[0].text
    if hasattr(response.usage, 'output_tokens'):
        print(f"✅ 生成完成，输出 token 数: {response.usage.output_tokens}")
    else:
        print(f"✅ 生成完成")

    return content


def post_process(content: str, output_path: str) -> None:
    """
    后处理生成内容

    1. 保存主输出文件
    2. 处理权利要求书的解释部分（如果有 --- 分隔符）
    """
    output_file = Path(output_path)

    # 保存主文件
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding="utf-8")
    print(f"💾 已保存: {output_file}")

    # 特殊处理：权利要求书的解释部分
    if "权利要求书" in output_file.name:
        if "---" in content:
            parts = content.split("---", 1)
            if len(parts) == 2:
                # 主文件只保留第一部分
                main_content = parts[0].strip()
                output_file.write_text(main_content, encoding="utf-8")

                # 解释部分保存到单独文件
                explanation_path = output_file.parent / (output_file.stem + "_解释.md")
                explanation_content = parts[1].strip()
                explanation_path.write_text(explanation_content, encoding="utf-8")
                print(f"💾 解释部分已分离: {explanation_path}")


def main():
    parser = argparse.ArgumentParser(
        description="专利部分生成器 - 通过 GLM API 生成专利章节",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 生成背景技术
  python scripts/generate.py \\
      --prompt references/01_背景技术.md \\
      --context outputs/case/00_技术交底书.md \\
      --output outputs/case/01_背景技术.md

  # 指定模型
  python scripts/generate.py --model glm-4.7 --prompt ...

  # 生成权利要求书（多个上下文）
  python scripts/generate.py \\
      --prompt references/02_权要布局.md \\
      --context outputs/case/00_技术交底书.md \\
      --context outputs/case/01_背景技术.md \\
      --output outputs/case/02_权利要求书.md

  # 较低温度（更确定性的输出）
  python scripts/generate.py --temperature 0.3 ...
        """
    )

    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Prompt 模板文件路径 (如 references/01_背景技术.md)"
    )
    parser.add_argument(
        "--context", "-c",
        action="append",
        default=[],
        help="上下文文件路径（可多次使用，按顺序添加）"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出文件路径"
    )
    parser.add_argument(
        "--model", "-m",
        default=DEFAULT_MODEL,
        help=f"模型名称（默认: {DEFAULT_MODEL}）"
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="温度参数 0-1，默认 0.7。较低值输出更确定性"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅显示将要发送的内容，不实际调用 API"
    )

    args = parser.parse_args()

    # 验证输入文件
    if not Path(args.prompt).exists():
        print(f"❌ 错误: Prompt 文件不存在: {args.prompt}")
        sys.exit(1)

    for ctx_file in args.context:
        if not Path(ctx_file).exists():
            print(f"❌ 错误: 上下文文件不存在: {ctx_file}")
            sys.exit(1)

    # Dry run 模式
    if args.dry_run:
        print("=== Dry Run 模式 ===")
        print(f"模型: {args.model}")
        print(f"API 端点: {GLM_BASE_URL}")
        print(f"温度: {args.temperature}")
        print(f"Prompt 模板: {args.prompt}")
        print(f"上下文文件: {args.context}")
        print(f"输出文件: {args.output}")
        print("\n=== 将发送的内容 ===")
        print(build_user_message(args.prompt, args.context)[:1000] + "...")
        return

    try:
        # 调用 API 生成内容
        content = call_llm_api(
            prompt_template=args.prompt,
            context_files=args.context,
            model=args.model,
            temperature=args.temperature
        )

        # 后处理和保存
        post_process(content, args.output)

        print("\n✨ 生成完成!")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
