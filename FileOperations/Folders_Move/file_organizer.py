import os
import shutil
import argparse
from datetime import datetime
from tqdm import tqdm


def organize_files(source_dir, dest_dir, mode='flat', overwrite=False):
    """
    批量移动文件并支持多种组织模式

    参数：
    source_dir : 源目录路径
    dest_dir   : 目标目录路径
    mode       : 组织模式 (flat/flat_rename/preserve)
    overwrite  : 是否覆盖已存在文件
    """
    moved_files = 0
    skipped_files = 0
    log_file = os.path.join(dest_dir, f"file_move_log_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

    # 创建目标目录
    os.makedirs(dest_dir, exist_ok=True)

    # 获取文件总数用于进度条
    file_count = sum([len(files) for _, _, files in os.walk(source_dir)])

    with open(log_file, 'w') as log, tqdm(total=file_count, desc="处理进度") as pbar:
        for root, _, files in os.walk(source_dir):
            for filename in files:
                src_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, source_dir)

                # 构建目标路径
                if mode == 'preserve':
                    dest_path = os.path.join(dest_dir, relative_path, filename)
                elif mode == 'flat_rename':
                    new_filename = f"{relative_path.replace(os.sep, '_')}_{filename}"
                    dest_path = os.path.join(dest_dir, new_filename)
                else:  # flat模式
                    dest_path = os.path.join(dest_dir, filename)

                # 处理文件冲突
                final_dest = handle_conflict(dest_path, overwrite)

                # 执行移动操作
                try:
                    os.makedirs(os.path.dirname(final_dest), exist_ok=True)
                    shutil.move(src_path, final_dest)
                    log.write(f"[SUCCESS] {src_path} -> {final_dest}\n")
                    moved_files += 1
                except Exception as e:
                    log.write(f"[ERROR] {src_path} -> {str(e)}\n")
                    skipped_files += 1

                pbar.update(1)

    print(f"\n操作完成: 成功移动 {moved_files} 个文件，跳过 {skipped_files} 个文件")
    print(f"日志文件保存至: {log_file}")


def handle_conflict(dest_path, overwrite):
    """处理文件冲突，返回最终目标路径"""
    if not os.path.exists(dest_path):
        return dest_path

    if overwrite:
        return dest_path

    # 自动重命名 (filename_001.ext)
    base, ext = os.path.splitext(dest_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter:03d}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量文件整理工具")
    parser.add_argument("-s", "--source", required=True, help="源目录路径")
    parser.add_argument("-d", "--dest", required=True, help="目标目录路径")
    parser.add_argument("-m", "--mode", choices=['flat', 'flat_rename', 'preserve'],
                        default='flat', help="组织模式 (默认: flat)")
    parser.add_argument("-f", "--force", action="store_true", help="强制覆盖已存在文件")

    args = parser.parse_args()

    organize_files(
        source_dir=args.source,
        dest_dir=args.dest,
        mode=args.mode,
        overwrite=args.force
    )