"""命令行入口：审查代码文件。用法: python main.py <代码文件>"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from reviewer import LLMClient, review_file  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print("用法：python main.py <代码文件>")
        return
    try:
        print("=== AI 代码审查报告 ===")
        print(review_file(sys.argv[1], LLMClient()))
    except RuntimeError as e:
        print(f"[错误] {e}")


if __name__ == "__main__":
    main()
