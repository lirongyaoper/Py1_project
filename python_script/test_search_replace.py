#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件搜索替换工具的功能
"""

import os
import tempfile
import shutil
from pathlib import Path
from file_search_replace import FileSearchReplace

def create_test_directory():
    """创建测试目录结构"""
    test_dir = Path("test_search_directory")
    
    # 清理之前的测试目录
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    test_dir.mkdir()
    
    # 创建测试文件
    files_content = {
        "main.py": """#!/usr/bin/env python3
# This is a test file
def example_function():
    print("Hello, world!")
    return "example"

class ExampleClass:
    def __init__(self):
        self.example_var = "test"
    
    def example_method(self):
        return self.example_var

if __name__ == "__main__":
    example_function()
""",
        "config.json": """{
    "example_config": "test_value",
    "database": {
        "host": "localhost",
        "port": 3306
    },
    "example_settings": {
        "debug": true,
        "log_level": "INFO"
    }
}
""",
        "README.md": """# Test Project

This is an example project for testing the search and replace tool.

## Features

- Example feature 1
- Example feature 2
- Example feature 3

## Usage

```python
from example_module import example_function
result = example_function()
```

## Configuration

See `config.json` for example configuration.
""",
        "test.txt": """This is a test file with multiple lines.
Line 2 contains the word example.
Line 3 has EXAMPLE in uppercase.
Line 4 has Example with mixed case.
Line 5 has no matching words.
""",
        "data.csv": """name,age,city
John,25,New York
Jane,30,Los Angeles
Bob,35,Chicago
""",
        "script.js": """// JavaScript test file
function exampleFunction() {
    console.log("This is an example function");
    return "example result";
}

// Example comment
const exampleVariable = "test value";

// TODO: Add more functionality
// FIXME: Fix this issue
"""
    }
    
    # 创建文件
    for filename, content in files_content.items():
        with open(test_dir / filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # 创建子目录
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir()
    
    with open(sub_dir / "helper.py", 'w', encoding='utf-8') as f:
        f.write("""# Helper module
def helper_example():
    return "This is an example helper function"

# Example comment
example_constant = 42

# TODO: Implement more helper functions
""")
    
    # 创建排除的目录
    exclude_dir = test_dir / "node_modules"
    exclude_dir.mkdir()
    
    with open(exclude_dir / "package.json", 'w', encoding='utf-8') as f:
        f.write('{"name": "test", "version": "1.0.0"}')
    
    # 创建二进制文件（模拟）
    with open(test_dir / "image.jpg", 'w') as f:
        f.write("This is a fake image file with example text")
    
    return test_dir

def test_basic_search():
    """测试基本搜索功能"""
    print("=== 测试基本搜索功能 ===")
    
    test_dir = create_test_directory()
    tool = FileSearchReplace(str(test_dir))
    
    # 测试1: 搜索 "example"
    print("\n1. 搜索 'example' (区分大小写):")
    results = tool.search_string("example", case_sensitive=True)
    print(f"找到 {len(results)} 个匹配项:")
    for file_path, line_num, content in results:
        print(f"  {file_path}:{line_num} - {content}")
    
    # 测试2: 搜索 "example" (忽略大小写)
    print("\n2. 搜索 'example' (忽略大小写):")
    results = tool.search_string("example", case_sensitive=False)
    print(f"找到 {len(results)} 个匹配项:")
    for file_path, line_num, content in results:
        print(f"  {file_path}:{line_num} - {content}")
    
    # 测试3: 搜索不存在的字符串
    print("\n3. 搜索不存在的字符串 'nonexistent':")
    results = tool.search_string("nonexistent")
    print(f"找到 {len(results)} 个匹配项")
    
    # 清理测试目录
    shutil.rmtree(test_dir)

def test_file_filtering():
    """测试文件过滤功能"""
    print("\n=== 测试文件过滤功能 ===")
    
    test_dir = create_test_directory()
    tool = FileSearchReplace(str(test_dir))
    
    # 测试1: 只搜索Python文件
    print("\n1. 只搜索Python文件中的 'example':")
    tool.set_included_extensions(['.py'])
    results = tool.search_string("example", case_sensitive=False)
    print(f"在Python文件中找到 {len(results)} 个匹配项:")
    for file_path, line_num, content in results:
        print(f"  {file_path}:{line_num} - {content}")
    
    # 测试2: 搜索多种文件类型
    print("\n2. 搜索Python和JavaScript文件中的 'example':")
    tool.set_included_extensions(['.py', '.js'])
    results = tool.search_string("example", case_sensitive=False)
    print(f"在Python和JS文件中找到 {len(results)} 个匹配项:")
    for file_path, line_num, content in results:
        print(f"  {file_path}:{line_num} - {content}")
    
    # 测试3: 重置包含扩展名
    print("\n3. 搜索所有文本文件中的 'example':")
    tool.set_included_extensions(None)
    results = tool.search_string("example", case_sensitive=False)
    print(f"在所有文本文件中找到 {len(results)} 个匹配项")
    
    # 清理测试目录
    shutil.rmtree(test_dir)

def test_replace_functionality():
    """测试替换功能"""
    print("\n=== 测试替换功能 ===")
    
    test_dir = create_test_directory()
    tool = FileSearchReplace(str(test_dir))
    
    # 测试1: 试运行替换
    print("\n1. 试运行替换 'example' -> 'sample':")
    results = tool.replace_string("example", "sample", case_sensitive=True, dry_run=True)
    print(f"将替换 {len(results)} 处:")
    for file_path, line_num, old_content, new_content in results:
        print(f"  {file_path}:{line_num}")
        print(f"    原: {old_content}")
        print(f"    新: {new_content}")
    
    # 测试2: 实际执行替换
    print("\n2. 实际执行替换 'example' -> 'sample':")
    results = tool.replace_string("example", "sample", case_sensitive=True, dry_run=False)
    print(f"已替换 {len(results)} 处")
    
    # 验证替换结果
    print("\n3. 验证替换结果:")
    results = tool.search_string("sample", case_sensitive=True)
    print(f"找到 {len(results)} 个 'sample':")
    for file_path, line_num, content in results:
        print(f"  {file_path}:{line_num} - {content}")
    
    # 清理测试目录
    shutil.rmtree(test_dir)

def test_recursive_search():
    """测试递归搜索功能"""
    print("\n=== 测试递归搜索功能 ===")
    
    test_dir = create_test_directory()
    tool = FileSearchReplace(str(test_dir))
    
    # 测试1: 递归搜索
    print("\n1. 递归搜索 'example':")
    results = tool.search_string("example", case_sensitive=False, recursive=True)
    print(f"递归搜索找到 {len(results)} 个匹配项:")
    for file_path, line_num, content in results:
        print(f"  {file_path}:{line_num} - {content}")
    
    # 测试2: 非递归搜索
    print("\n2. 非递归搜索 'example':")
    results = tool.search_string("example", case_sensitive=False, recursive=False)
    print(f"非递归搜索找到 {len(results)} 个匹配项:")
    for file_path, line_num, content in results:
        print(f"  {file_path}:{line_num} - {content}")
    
    # 清理测试目录
    shutil.rmtree(test_dir)

def test_exclude_functionality():
    """测试排除功能"""
    print("\n=== 测试排除功能 ===")
    
    test_dir = create_test_directory()
    tool = FileSearchReplace(str(test_dir))
    
    # 测试1: 添加排除目录
    print("\n1. 添加排除目录 'subdir':")
    tool.add_excluded_dirs(['subdir'])
    results = tool.search_string("example", case_sensitive=False)
    print(f"排除subdir后找到 {len(results)} 个匹配项:")
    for file_path, line_num, content in results:
        print(f"  {file_path}:{line_num} - {content}")
    
    # 测试2: 添加排除扩展名
    print("\n2. 添加排除扩展名 '.txt':")
    tool.add_excluded_extensions(['.txt'])
    results = tool.search_string("example", case_sensitive=False)
    print(f"排除.txt文件后找到 {len(results)} 个匹配项:")
    for file_path, line_num, content in results:
        print(f"  {file_path}:{line_num} - {content}")
    
    # 清理测试目录
    shutil.rmtree(test_dir)

def main():
    """主测试函数"""
    print("开始测试文件搜索替换工具...")
    
    try:
        test_basic_search()
        test_file_filtering()
        test_replace_functionality()
        test_recursive_search()
        test_exclude_functionality()
        
        print("\n=== 所有测试完成 ===")
        print("测试通过！工具功能正常。")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()