import os
import argparse
import chardet
from pathlib import Path

def detect_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        raw_data = f.read(1024)
        result = chardet.detect(raw_data)
        return result['encoding'] or 'utf-8'

def replace_in_file(file_path, old_str, new_str):
    """替换单个文件中的字符串"""
    try:
        # 检测文件编码
        encoding = detect_encoding(file_path)
        
        # 读取文件内容
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()
        
        # 替换字符串
        if old_str in content:
            new_content = content.replace(old_str, new_str)
            
            # 写回文件
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(new_content)
            
            print(f"已替换: {file_path}")
            return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
    return False

def main():
    parser = argparse.ArgumentParser(description='递归替换目录中所有文件的特定字符串')
    parser.add_argument('--directory', '-d', required=True, help='要处理的目录路径')
    parser.add_argument('--old', '-o', required=True, help='要替换的旧字符串')
    parser.add_argument('--new', '-n', required=True, help='替换为的新字符串')
    parser.add_argument('--extensions', '-e', nargs='+', default=['.php', '.html', '.js', '.css', '.txt'], 
                        help='要处理的文件扩展名列表 (默认: .php .html .js .css .txt)')
    parser.add_argument('--dry-run', '-dr', action='store_true', help='执行预演，不实际修改文件')
    
    args = parser.parse_args()
    
    # 转换为绝对路径
    directory = Path(args.directory).resolve()
    
    if not directory.is_dir():
        print(f"错误: 指定的路径 '{directory}' 不是一个目录")
        return
    
    print(f"开始处理目录: {directory}")
    print(f"将 '{args.old}' 替换为 '{args.new}'")
    print(f"处理的文件扩展名: {', '.join(args.extensions)}")
    
    total_files = 0
    modified_files = 0
    
    # 递归遍历目录
    for root, _, files in os.walk(directory):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in args.extensions:
                file_path = os.path.join(root, file)
                total_files += 1
                
                if args.dry_run:
                    try:
                        # 检测文件编码
                        encoding = detect_encoding(file_path)
                        
                        # 读取文件内容
                        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                            content = f.read()
                        
                        if args.old in content:
                            print(f"预演: 会替换 {file_path}")
                            modified_files += 1
                    except Exception as e:
                        print(f"预演时处理文件 {file_path} 出错: {e}")
                else:
                    if replace_in_file(file_path, args.old, args.new):
                        modified_files += 1
    
    print(f"\n处理完成!")
    print(f"总共处理了 {total_files} 个文件")
    print(f"成功替换了 {modified_files} 个文件")
#python batch_replace.py -d /home/lirongyao0916/Projects/lryper -o lirongyaoper.com -n lryper.com
#python batch_replace.py -d /home/lirongyao0916/Projects/lryper -o lirongyaoper.com -n lryper.com --dry-run
#python batch_replace.py -d /home/lirongyao0916/Documents/lry -o lirongyaoper.com -n lryper.com -e .php .html .js .css .txt .xml

if __name__ == "__main__":
    main()

