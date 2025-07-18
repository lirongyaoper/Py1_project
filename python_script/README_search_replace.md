# 文件查找和替换工具

这是一个功能强大的Python脚本，可以在指定目录中精确查找和替换字符串，支持多种过滤和配置选项。

## 主要功能

1. **灵活目录搜索**: 可以在任意指定目录中进行搜索，不局限于项目
2. **精确查找**: 精确查找给定字符串，支持大小写敏感/不敏感
3. **批量替换**: 支持字符串替换，可选择试运行模式
4. **智能过滤**: 自动排除二进制文件，支持自定义文件类型过滤
5. **递归搜索**: 支持递归搜索子目录或仅在当前目录搜索
6. **详细输出**: 显示文件路径、行号和内容，结果保存为txt文件
7. **编码支持**: 支持UTF-8编码，自动处理编码错误

## 安装要求

- Python 3.6+
- 无需额外依赖包

## 基本用法

### 搜索功能

```bash
# 在当前目录搜索字符串
python file_search_replace.py "要搜索的字符串"

# 在指定目录搜索
python file_search_replace.py "要搜索的字符串" -p /path/to/directory

# 忽略大小写搜索
python file_search_replace.py "要搜索的字符串" -i

# 仅在当前目录搜索（不递归子目录）
python file_search_replace.py "要搜索的字符串" --no-recursive

# 指定输出文件
python file_search_replace.py "要搜索的字符串" -o results.txt
```

### 替换功能

```bash
# 试运行替换（显示结果但不修改文件）
python file_search_replace.py "旧字符串" -r "新字符串" --dry-run

# 实际执行替换
python file_search_replace.py "旧字符串" -r "新字符串"

# 忽略大小写替换
python file_search_replace.py "旧字符串" -r "新字符串" -i

# 仅在指定目录替换（不递归）
python file_search_replace.py "旧字符串" -r "新字符串" -p /path/to/directory --no-recursive
```

## 高级用法

### 文件类型过滤

```bash
# 只搜索Python文件
python file_search_replace.py "import" --include-ext .py

# 只搜索多种类型的文件
python file_search_replace.py "TODO" --include-ext .py .js .html .css

# 排除特定扩展名
python file_search_replace.py "example" --exclude-ext .log .tmp

# 排除特定目录
python file_search_replace.py "test" --exclude-dir node_modules vendor
```

### 组合使用示例

```bash
# 在src目录中搜索Python文件中的"debug"字符串，忽略大小写
python file_search_replace.py "debug" -p src --include-ext .py -i

# 在项目根目录替换所有JavaScript文件中的"old_api"为"new_api"
python file_search_replace.py "old_api" -r "new_api" --include-ext .js --dry-run

# 在文档目录中搜索，排除临时文件和日志文件
python file_search_replace.py "重要信息" -p docs --exclude-ext .tmp .log --exclude-dir temp
```

## 命令行参数详解

### 必需参数
- `search_str`: 要搜索的字符串

### 可选参数
- `-r, --replace`: 替换字符串（如果提供则执行替换）
- `-p, --path`: 搜索目录路径（默认为当前目录）
- `-o, --output`: 输出文件路径（默认为search_results.txt）
- `-i, --ignore-case`: 忽略大小写
- `--dry-run`: 试运行模式（仅显示替换结果，不实际修改文件）
- `--no-recursive`: 不递归搜索子目录
- `--include-ext`: 只包含指定扩展名的文件（可指定多个）
- `--exclude-dir`: 额外排除的目录名（可指定多个）
- `--exclude-ext`: 额外排除的文件扩展名（可指定多个）

## 输出格式

### 搜索结果输出示例

```
搜索路径: /home/user/project
================================================================================

搜索字符串: TODO
找到 5 个匹配项

文件: src/main.py
行号: 15
内容: # TODO: 实现这个功能
--------------------------------------------------------------------------------

文件: docs/README.md
行号: 25
内容: - TODO: 添加更多示例
--------------------------------------------------------------------------------
```

### 替换结果输出示例

```
搜索路径: /home/user/project
================================================================================

搜索字符串: old_api
替换字符串: new_api
替换统计: 共 3 处被替换

文件: src/api.py
行号: 10
原内容: from old_api import Client
新内容: from new_api import Client
--------------------------------------------------------------------------------
```

## 默认排除规则

### 自动排除的目录
- `.git`, `__pycache__`, `node_modules`, `.vscode`, `.idea`
- `cache`, `uploads`, `vendor`, `composer`
- `bin`, `obj`, `build`, `dist`, `target`, `out`

### 自动排除的文件类型
- **图片**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.svg`, `.ico`, `.webp`
- **字体**: `.ttf`, `.otf`, `.woff`, `.woff2`, `.eot`, `.fnt`
- **音频**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a`
- **视频**: `.mp4`, `.avi`, `.mov`, `.wmv`, `.flv`, `.mkv`, `.webm`, `.m4v`
- **压缩**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`
- **可执行**: `.exe`, `.dll`, `.so`, `.dylib`, `.bin`, `.app`
- **数据库**: `.db`, `.sqlite`, `.sqlite3`, `.mdb`, `.accdb`
- **文档**: `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`

## 实际使用场景

### 场景1: 查找项目中的TODO注释
```bash
python file_search_replace.py "TODO" -p /path/to/project --include-ext .py .js .java
```

### 场景2: 批量替换API端点
```bash
# 先试运行查看替换结果
python file_search_replace.py "/api/v1" -r "/api/v2" --include-ext .py .js --dry-run

# 确认无误后执行实际替换
python file_search_replace.py "/api/v1" -r "/api/v2" --include-ext .py .js
```

### 场景3: 查找配置文件中的特定设置
```bash
python file_search_replace.py "database_url" -p /path/to/config --include-ext .json .yaml .yml .ini
```

### 场景4: 清理临时文件和日志中的敏感信息
```bash
python file_search_replace.py "password=secret" -r "password=***" --exclude-ext .log .tmp
```

## 安全建议

1. **备份重要文件**: 在执行替换操作前，建议备份重要文件
2. **使用试运行模式**: 首次使用替换功能时，建议先使用 `--dry-run` 参数
3. **检查权限**: 确保对目标文件有读写权限
4. **版本控制**: 在版本控制的代码库中使用时，建议先提交当前更改

## 错误处理

脚本包含完善的错误处理机制：

- **路径验证**: 自动检查搜索路径是否存在
- **文件访问**: 处理文件权限和访问错误
- **编码处理**: 自动处理不同编码的文件
- **用户中断**: 支持Ctrl+C中断操作
- **详细错误信息**: 提供清晰的错误提示

## 性能优化

- **智能文件过滤**: 自动跳过二进制文件，提高搜索效率
- **内存优化**: 逐行处理大文件，避免内存溢出
- **编码检测**: 快速检测文件编码，避免不必要的处理

## 扩展功能

如需添加更多功能，可以修改脚本中的相关方法：

- 添加新的文件类型过滤规则
- 支持正则表达式搜索
- 添加并行处理支持
- 支持更多输出格式（JSON、CSV等）