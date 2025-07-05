import os
import re
import argparse
from pathlib import Path

def search_text_in_file(file_path, search_text):
    """搜索文件中包含指定文本的行，并返回行号和内容"""
    results = []
    try:
        # 尝试使用 UTF-8 编码打开文件
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                if search_text in line:
                    results.append((line_num, line.strip()))
    except UnicodeDecodeError:
        try:
            # 尝试使用 GBK 编码打开文件
            with open(file_path, 'r', encoding='gbk') as file:
                for line_num, line in enumerate(file, 1):
                    if search_text in line:
                        results.append((line_num, line.strip()))
        except Exception as e:
            print(f"无法读取文件 {file_path}: {str(e)}")
    return results

def search_directory(directory, search_text, exclude_dirs=None, exclude_exts=None):
    """递归搜索目录中的所有文件"""
    if exclude_dirs is None:
        exclude_dirs = set()
    if exclude_exts is None:
        exclude_exts = set()
    
    results = []
    for root, dirs, files in os.walk(directory):
        # 跳过排除的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_ext = Path(file).suffix.lower()
            # 跳过排除的文件扩展名
            if file_ext in exclude_exts:
                continue
                
            file_path = os.path.join(root, file)
            file_results = search_text_in_file(file_path, search_text)
            
            if file_results:
                results.append((file_path, file_results))
    
    return results

def main():
    parser = argparse.ArgumentParser(description='递归搜索目录中包含指定文本的文件和行号')
    parser.add_argument('directory', help='要搜索的目录路径')
    parser.add_argument('--text', default='lry_admin_center', help='要搜索的文本，默认为 lry_admin_center')
    parser.add_argument('--output', help='输出结果的文件路径，默认为控制台输出')
    parser.add_argument('--exclude-dirs', nargs='+', default=['.git', 'node_modules'], help='要排除的目录列表')
    parser.add_argument('--exclude-exts', nargs='+', default=['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.pdf', '.zip', '.gz', '.tar'], help='要排除的文件扩展名列表')
    
    args = parser.parse_args()
    
    # 检查目录是否存在
    if not os.path.isdir(args.directory):
        print(f"错误: 指定的目录 '{args.directory}' 不存在")
        return
    
    # 执行搜索
    search_results = search_directory(
        args.directory,
        args.text,
        set(args.exclude_dirs),
        set(args.exclude_exts)
    )
    
    # 输出结果
    output = []
    if search_results:
        output.append(f"在 {len(search_results)} 个文件中找到匹配项：\n")
        for file_path, matches in search_results:
            output.append(f"文件: {file_path}")
            for line_num, line_content in matches:
                output.append(f"  行号: {line_num}, 内容: {line_content}")
            output.append("")  # 空行分隔不同文件
    else:
        output.append("未找到匹配的文本。")
    
    # 输出到文件或控制台
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output))
        print(f"结果已保存到文件: {args.output}")
    else:
        print('\n'.join(output))



#  python search_admin_text.py /var/www/lryper.com --output results.txt




if __name__ == "__main__":
    main()