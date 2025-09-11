import os
import shutil
from pathlib import Path


def extract_subdirs_and_remove_parent(root_dir):
    """
    提取子目录并删除父目录
    :param root_dir: 要处理的根目录
    """
    processed = 0
    errors = 0

    # 遍历根目录下的所有条目
    for entry in os.listdir(root_dir):
        parent_path = os.path.join(root_dir, entry)

        # 只处理目录
        if not os.path.isdir(parent_path):
            continue

        # 获取所有子目录
        subdirs = [d for d in os.listdir(parent_path)
                   if os.path.isdir(os.path.join(parent_path, d))]

        if not subdirs:
            continue

        print(f"\nProcessing parent directory: {parent_path}")
        print(f"Found {len(subdirs)} subdirectories")

        try:
            # 移动每个子目录到根目录
            for subdir in subdirs:
                src = os.path.join(parent_path, subdir)
                dst = os.path.join(root_dir, subdir)

                # 处理目标已存在的情况
                if os.path.exists(dst):
                    base, ext = os.path.splitext(subdir)
                    counter = 1
                    while os.path.exists(dst):
                        new_name = f"{base}_{counter}{ext}" if ext else f"{base}_{counter}"
                        dst = os.path.join(root_dir, new_name)
                        counter += 1

                print(f"Moving: {src} -> {dst}")
                shutil.move(src, dst)

            # 删除父目录
            print(f"Removing parent directory: {parent_path}")
            shutil.rmtree(parent_path)
            processed += 1

        except Exception as e:
            print(f"Error processing {parent_path}: {e}")
            errors += 1

    print(f"\nOperation complete:")
    print(f"- Successfully processed directories: {processed}")
    print(f"- Errors encountered: {errors}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python extract_subdirs.py <root_directory>")
        sys.exit(1)

    root_dir = sys.argv[1]

    if not os.path.isdir(root_dir):
        print(f"Error: {root_dir} is not a valid directory")
        sys.exit(1)

    print(f"Starting processing of directory: {root_dir}")
    extract_subdirs_and_remove_parent(root_dir)