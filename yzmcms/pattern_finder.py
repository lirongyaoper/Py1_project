#!/usr/bin/env python
import os
import re
import argparse
from mimetypes import guess_type
import sys
import chardet

def supports_color():
    """检查终端是否支持颜色（适配 Conda）"""
    if sys.platform == "win32":
        return False
    is_terminal = os.isatty(sys.stdout.fileno())
    no_color = os.getenv("NO_COLOR", "").lower() in ("1", "true")
    return is_terminal and not no_color

class Colors:
    RED = '\033[91m' if supports_color() else ''
    GREEN = '\033[92m' if supports_color() else ''
    YELLOW = '\033[93m' if supports_color() else ''
    BLUE = '\033[94m' if supports_color() else ''
    END = '\033[0m' if supports_color() else ''

def is_image_file(filepath):
    mime_type, _ = guess_type(filepath)
    return mime_type is not None and mime_type.startswith('image/')

def find_pattern_in_file(filepath, pattern, case_sensitive=True):
    matches = []
    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        with open(filepath, 'rb') as f:
            rawdata = f.read(1024)
            encoding = chardet.detect(rawdata)['encoding'] or 'utf-8'
        with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip()
                if re.search(pattern, line, flags):
                    highlighted = re.sub(
                        pattern,
                        lambda m: f"{Colors.RED}{m.group()}{Colors.END}",
                        line,
                        flags=flags
                    )
                    matches.append((line_num, highlighted, line))
    except Exception as e:
        if args.verbose:
            print(f"{Colors.RED}无法读取文件 {filepath}: {str(e)}{Colors.END}")
    return matches
#cd /home/lirongyao0916/Projects/Py1_project/yzmcms && ./pattern_finder.py /home/lirongyao0916/Projects/lryper.com/forumV22 'bbs' -o results_bbs.txt
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='递归查找文件')
    parser.add_argument('directory', help='要搜索的目录')
    parser.add_argument('pattern', help='正则表达式模式')
    parser.add_argument('-o', '--output', required=True, help='输出文件')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='忽略大小写')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"{Colors.RED}错误: 目录不存在{Colors.END}")
        sys.exit(1)

    total, matched = 0, 0
    with open(args.output, 'w', encoding='utf-8') as out_f:
        for root, _, files in os.walk(args.directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                total += 1
                if is_image_file(filepath):
                    continue
                matches = find_pattern_in_file(filepath, args.pattern, not args.ignore_case)
                if matches:
                    matched += 1
                    print(f"{Colors.BLUE}文件: {filepath}{Colors.END}")
                    out_f.write(f"文件: {filepath}\n")
                    for line_num, colored, plain in matches:
                        print(f"  {Colors.YELLOW}行 {line_num}:{Colors.END} {colored}")
                        out_f.write(f"  行 {line_num}: {plain}\n")
                    out_f.write("\n")
    print(f"\n扫描完成！匹配文件: {matched}/{total}")