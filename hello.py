#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
随机名言打印脚本

每次运行时从预设列表中随机选择一句名言并打印到控制台。
"""

import random
import sys
import io

# 设置标准输出编码为 UTF-8，解决 Windows 控制台中文显示问题
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    """主函数：随机选择并打印一句名言"""

    # 名言列表（包含中文和英文经典名言）
    quote_list = [
        "学而时习之，不亦说乎？ - 孔子",
        "知之者不如好之者，好之者不如乐之者。 - 孔子",
        "路漫漫其修远兮，吾将上下而求索。 - 屈原",
        "不积跬步，无以至千里。 - 荀子",
        "天行健，君子以自强不息。 - 周易",
        "Stay hungry, stay foolish. - Steve Jobs",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "In the middle of difficulty lies opportunity. - Albert Einstein",
        "Life is what happens when you're busy making other plans. - John Lennon",
        "Be the change you want to see in the world. - Mahatma Gandhi"
    ]

    # 检查名言列表是否为空
    if not quote_list:
        print("错误：名言列表为空")
        return

    # 随机选择一句名言
    random_quote = random.choice(quote_list)

    # 打印名言
    print(random_quote)


if __name__ == "__main__":
    main()