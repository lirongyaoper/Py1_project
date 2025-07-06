import os
import re
import argparse


def is_valid_admin_match(match_obj, line):
    """检查找到的admin匹配是否有效，排除不需要的情况"""
    start, end = match_obj.span()

    # 检查前面不能有字母、数字或下划线
    if start > 0:
        prev_char = line[start - 1]
        if prev_char.isalnum() or prev_char == '_' or prev_char == '$':
            return False

    # 检查后面不能有字母、数字或下划线
    if end < len(line):
        next_char = line[end]
        if next_char.isalnum() or next_char == '_':
            return False

    # 排除 D('admin') 样式
    if start >= 2 and line[start - 2:start] == "D(":
        return False

    return True


def find_admin_in_file(filepath):
    """在单个文件中查找符合条件的admin字符串"""
    matches = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # 使用正则表达式查找所有admin出现的位置
                for match in re.finditer(r'admin', line):
                    if is_valid_admin_match(match, line):
                        matches.append((line_num, line.strip()))
                        break  # 每行只记录一次
    except (UnicodeDecodeError, PermissionError):
        # 忽略无法读取的文件（二进制文件或无权限文件）
        pass
    return matches


def find_admin_in_directory(directory, output_file):
    """递归查找目录中所有文件中的admin字符串"""
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                matches = find_admin_in_file(filepath)

                if matches:
                    out_f.write(f"文件: {filepath}\n")
                    print(f"文件: {filepath}")

                    for line_num, line in matches:
                        out_f.write(f"  行 {line_num}: {line}\n")
                        print(f"  行 {line_num}: {line}")

                    out_f.write("\n")
                    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='查找目录中包含admin字符串的文件')
    parser.add_argument('directory', help='要搜索的目录路径')
    parser.add_argument('-o', '--output', required=True, help='输出文件路径')

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"错误: {args.directory} 不是一个有效的目录")
        sys.exit(1)

    print(f"开始在目录 {args.directory} 中查找admin字符串...")
    find_admin_in_directory(args.directory, args.output)
    print(f"查找完成，结果已保存到 {args.output}")