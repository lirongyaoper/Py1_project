#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目文件查找和替换工具
功能：
1. 在整个项目中精确查找给定字符串
2. 输出查找结果到指定路径的txt文件
3. 支持字符串替换功能
"""

import os
import re
import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import mimetypes

class ProjectSearchReplace:
    def __init__(self, project_path: str = "."):
        """
        初始化搜索替换工具
        
        Args:
            project_path: 项目根目录路径，默认为当前目录
        """
        self.project_path = Path(project_path).resolve()
        self.excluded_dirs = {
            '.git', '__pycache__', 'node_modules', '.vscode', 
            '.idea', 'cache', 'uploads', 'vendor', 'composer'
        }
        self.excluded_extensions = {
            # 图片文件
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.ico', '.webp',
            # 字体文件
            '.ttf', '.otf', '.woff', '.woff2', '.eot',
            # 其他二进制文件
            '.pdf', '.zip', '.rar', '.tar', '.gz', '.7z', '.exe', '.dll', '.so',
            '.dylib', '.bin', '.dat', '.db', '.sqlite', '.sqlite3'
        }
        
    def is_text_file(self, file_path: Path) -> bool:
        """
        判断文件是否为文本文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否为文本文件
        """
        # 检查文件扩展名
        if file_path.suffix.lower() in self.excluded_extensions:
            return False
            
        # 检查MIME类型
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and not mime_type.startswith('text/'):
            return False
            
        # 尝试读取文件前1024字节检查是否为二进制
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\x00' in chunk:  # 包含null字节，可能是二进制文件
                    return False
        except (IOError, OSError):
            return False
            
        return True
    
    def should_skip_directory(self, dir_path: Path) -> bool:
        """
        判断是否应该跳过某个目录
        
        Args:
            dir_path: 目录路径
            
        Returns:
            bool: 是否应该跳过
        """
        return dir_path.name in self.excluded_dirs
    
    def search_string(self, search_str: str, case_sensitive: bool = True) -> List[Tuple[str, int, str]]:
        """
        在项目中搜索字符串
        
        Args:
            search_str: 要搜索的字符串
            case_sensitive: 是否区分大小写
            
        Returns:
            List[Tuple[str, int, str]]: 搜索结果列表，每个元素为(文件路径, 行号, 行内容)
        """
        results = []
        
        if not case_sensitive:
            search_pattern = re.compile(re.escape(search_str), re.IGNORECASE)
        else:
            search_pattern = re.compile(re.escape(search_str))
        
        for root, dirs, files in os.walk(self.project_path):
            # 过滤掉不需要的目录
            dirs[:] = [d for d in dirs if not self.should_skip_directory(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                # 检查是否为文本文件
                if not self.is_text_file(file_path):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if search_pattern.search(line):
                                # 获取相对路径
                                relative_path = file_path.relative_to(self.project_path)
                                results.append((str(relative_path), line_num, line.rstrip()))
                except (IOError, OSError, UnicodeDecodeError) as e:
                    print(f"警告: 无法读取文件 {file_path}: {e}")
                    continue
        
        return results
    
    def replace_string(self, search_str: str, replace_str: str, case_sensitive: bool = True, 
                      dry_run: bool = True) -> List[Tuple[str, int, str, str]]:
        """
        在项目中替换字符串
        
        Args:
            search_str: 要搜索的字符串
            replace_str: 替换字符串
            case_sensitive: 是否区分大小写
            dry_run: 是否为试运行模式（不实际修改文件）
            
        Returns:
            List[Tuple[str, int, str, str]]: 替换结果列表，每个元素为(文件路径, 行号, 原行内容, 新行内容)
        """
        results = []
        
        if not case_sensitive:
            search_pattern = re.compile(re.escape(search_str), re.IGNORECASE)
        else:
            search_pattern = re.compile(re.escape(search_str))
        
        for root, dirs, files in os.walk(self.project_path):
            # 过滤掉不需要的目录
            dirs[:] = [d for d in dirs if not self.should_skip_directory(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                # 检查是否为文本文件
                if not self.is_text_file(file_path):
                    continue
                
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    
                    file_modified = False
                    new_lines = []
                    
                    for line_num, line in enumerate(lines, 1):
                        if search_pattern.search(line):
                            # 执行替换
                            if case_sensitive:
                                new_line = line.replace(search_str, replace_str)
                            else:
                                # 不区分大小写的替换
                                new_line = re.sub(search_pattern, replace_str, line)
                            
                            if new_line != line:
                                relative_path = file_path.relative_to(self.project_path)
                                results.append((str(relative_path), line_num, line.rstrip(), new_line.rstrip()))
                                file_modified = True
                            
                            new_lines.append(new_line)
                        else:
                            new_lines.append(line)
                    
                    # 如果不是试运行模式且文件有修改，则写回文件
                    if not dry_run and file_modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)
                        print(f"已修改文件: {file_path}")
                        
                except (IOError, OSError, UnicodeDecodeError) as e:
                    print(f"警告: 无法处理文件 {file_path}: {e}")
                    continue
        
        return results
    
    def save_results_to_file(self, results: List, output_path: str, mode: str = "search"):
        """
        将搜索结果保存到文件
        
        Args:
            results: 搜索结果列表
            output_path: 输出文件路径
            mode: 模式，"search" 或 "replace"
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"项目路径: {self.project_path}\n")
                f.write("=" * 80 + "\n\n")
                
                if mode == "search":
                    f.write(f"搜索字符串: {results[0][2] if results else 'N/A'}\n")
                    f.write(f"找到 {len(results)} 个匹配项\n\n")
                    
                    for file_path, line_num, line_content in results:
                        f.write(f"文件: {file_path}\n")
                        f.write(f"行号: {line_num}\n")
                        f.write(f"内容: {line_content}\n")
                        f.write("-" * 60 + "\n")
                        
                elif mode == "replace":
                    f.write(f"替换统计: 共 {len(results)} 处被替换\n\n")
                    
                    for file_path, line_num, old_content, new_content in results:
                        f.write(f"文件: {file_path}\n")
                        f.write(f"行号: {line_num}\n")
                        f.write(f"原内容: {old_content}\n")
                        f.write(f"新内容: {new_content}\n")
                        f.write("-" * 60 + "\n")
                
            print(f"结果已保存到: {output_path}")
            
        except IOError as e:
            print(f"错误: 无法保存结果到文件 {output_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="项目文件查找和替换工具")
    parser.add_argument("search_str", help="要搜索的字符串")
    parser.add_argument("-r", "--replace", help="替换字符串（如果提供则执行替换）")
    parser.add_argument("-p", "--project", default=".", help="项目根目录路径（默认为当前目录）")
    parser.add_argument("-o", "--output", default="search_results.txt", help="输出文件路径（默认为search_results.txt）")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="忽略大小写")
    parser.add_argument("--dry-run", action="store_true", help="试运行模式（仅显示替换结果，不实际修改文件）")
    
    args = parser.parse_args()
    
    # 创建搜索替换工具实例
    tool = ProjectSearchReplace(args.project)
    
    if args.replace:
        # 执行替换操作
        print(f"正在搜索并替换字符串...")
        print(f"搜索字符串: {args.search_str}")
        print(f"替换字符串: {args.replace}")
        print(f"忽略大小写: {args.ignore_case}")
        print(f"试运行模式: {args.dry_run}")
        print("-" * 60)
        
        results = tool.replace_string(
            args.search_str, 
            args.replace, 
            case_sensitive=not args.ignore_case,
            dry_run=args.dry_run
        )
        
        if results:
            print(f"找到 {len(results)} 处匹配项")
            for file_path, line_num, old_content, new_content in results:
                print(f"文件: {file_path}, 行号: {line_num}")
                print(f"原内容: {old_content}")
                print(f"新内容: {new_content}")
                print("-" * 40)
        else:
            print("未找到匹配项")
        
        # 保存结果到文件
        tool.save_results_to_file(results, args.output, "replace")
        
    else:
        # 执行搜索操作
        print(f"正在搜索字符串: {args.search_str}")
        print(f"忽略大小写: {args.ignore_case}")
        print("-" * 60)
        
        results = tool.search_string(args.search_str, case_sensitive=not args.ignore_case)
        
        if results:
            print(f"找到 {len(results)} 个匹配项:")
            for file_path, line_num, line_content in results:
                print(f"文件: {file_path}, 行号: {line_num}")
                print(f"内容: {line_content}")
                print("-" * 40)
        else:
            print("未找到匹配项")
        
        # 保存结果到文件
        tool.save_results_to_file(results, args.output, "search")

if __name__ == "__main__":
    main()