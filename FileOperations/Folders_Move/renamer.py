import os
import re
import argparse
from datetime import datetime
from tqdm import tqdm


def batch_rename(root_dir, patterns=None, dry_run=False, recursive=True,
                 case='keep', conflict='auto', keep_ext=1):
    """
    增强版批量重命名工具（支持多扩展名）

    参数：
    keep_ext : 保留的扩展名数量（例如2表示保留.tar.gz）
    """
    rename_plan = []
    log_file = os.path.join(root_dir, f"rename_log_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
    counter = {'success': 0, 'skipped': 0, 'errors': 0}

    for dirpath, _, filenames in os.walk(root_dir) if recursive else [next(os.walk(root_dir))]:
        for filename in filenames:
            original_path = os.path.join(dirpath, filename)

            # 应用命名规则（保留指定数量的扩展名）
            new_name = apply_naming_rules(filename, patterns, case, keep_ext)
            if new_name == filename:
                continue

            # 生成新路径并处理冲突
            new_path = os.path.join(dirpath, new_name)
            resolved_path = handle_conflict(new_path, conflict, keep_ext)

            if resolved_path:
                rename_plan.append((original_path, resolved_path))

    # 执行重命名操作
    with open(log_file, 'w') as log, tqdm(rename_plan, desc="处理进度") as pbar:
        for src, dest in pbar:
            try:
                if not dry_run:
                    os.rename(src, dest)
                    log.write(f"[SUCCESS] {src} → {dest}\n")
                    counter['success'] += 1
                else:
                    log.write(f"[DRY RUN] {src} → {dest}\n")
                    counter['success'] += 1
            except Exception as e:
                log.write(f"[ERROR] {src} → {str(e)}\n")
                counter['errors'] += 1
            pbar.set_postfix_str(f"成功: {counter['success']} 错误: {counter['errors']}")

    print(f"\n操作完成: 成功 {counter['success']} 项，错误 {counter['errors']} 项")
    print(f"日志文件: {log_file}")
    if dry_run:
        print("(试运行模式，未实际修改文件)")


def apply_naming_rules(filename, patterns, case, keep_ext):
    """处理多扩展名文件的核心逻辑"""
    name_part, ext_part = split_extension(filename, keep_ext)

    # 应用正则替换规则
    if patterns:
        for pattern, replacement in patterns:
            name_part = re.sub(pattern, replacement, name_part)

    # 处理大小写
    name_part = name_part.lower() if case == 'lower' else \
        name_part.upper() if case == 'upper' else name_part

    return f"{name_part}{ext_part}"


def split_extension(filename, keep_ext):
    """
    智能分割文件名与扩展名
    ("example.tar.gz", 2) → ("example", ".tar.gz")
    ("README", 1) → ("README", "")
    """
    parts = filename.rsplit('.', keep_ext)
    if len(parts) == 1:
        return filename, ''
    return '.'.join(parts[:-1]), '.' + parts[-1]


def handle_conflict(new_path, strategy, keep_ext):
    """改进的冲突处理（自动编号保留扩展名）"""
    if not os.path.exists(new_path) or strategy == 'overwrite':
        return new_path
    if strategy == 'skip':
        return None

    dirpath = os.path.dirname(new_path)
    filename = os.path.basename(new_path)
    name_part, ext_part = split_extension(filename, keep_ext)

    counter = 1
    while True:
        numbered_name = f"{name_part}_{counter:03d}{ext_part}"
        numbered_path = os.path.join(dirpath, numbered_name)
        if not os.path.exists(numbered_path):
            return numbered_path
        counter += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="多扩展名文件批量重命名工具")
    parser.add_argument("directory", help="目标目录路径")
    parser.add_argument("-r", "--recursive", action="store_true", help="递归处理子目录")
    parser.add_argument("-n", "--dry-run", action="store_true", help="试运行模式")
    parser.add_argument("--case", choices=['lower', 'upper', 'keep'], default='keep',
                        help="文件名大小写转换（不影响扩展名）")
    parser.add_argument("--conflict", choices=['auto', 'skip', 'overwrite'], default='auto',
                        help="冲突处理策略（默认：自动编号）")
    parser.add_argument("--keep-ext", type=int, default=1,
                        help="保留的扩展名数量（如2表示保留.tar.gz）")
    parser.add_argument("-p", "--pattern", nargs=2, action="append",
                        metavar=("REGEX", "REPLACE"), help="替换规则，可多次使用")

    args = parser.parse_args()

    batch_rename(
        root_dir=args.directory,
        patterns=args.pattern or [('\s+', '_')],
        dry_run=args.dry_run,
        recursive=args.recursive,
        case=args.case,
        conflict=args.conflict,
        keep_ext=args.keep_ext
    )