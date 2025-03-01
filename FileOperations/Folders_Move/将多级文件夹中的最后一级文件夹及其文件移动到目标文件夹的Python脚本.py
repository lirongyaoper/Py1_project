import os
import shutil
import sys


def move_leaf_dirs(source, target):
    """移动所有末端文件夹到目标目录"""
    # 创建目标目录（如果不存在）
    os.makedirs(target, exist_ok=True)

    # 收集所有末端文件夹路径
    leaf_dirs = []
    for root, dirs, _ in os.walk(source):
        if not dirs:  # 没有子目录即为末端文件夹
            leaf_dirs.append(root)

    # 移动每个末端文件夹并处理重名
    for leaf in leaf_dirs:
        base_name = os.path.basename(leaf)
        target_path = os.path.join(target, base_name)

        # 处理目标路径冲突
        counter = 1
        while os.path.exists(target_path):
            new_name = f"{base_name}_{counter}"
            target_path = os.path.join(target, new_name)
            counter += 1

        # 执行移动操作
        try:
            shutil.move(leaf, target_path)
            print(f"成功移动：'{leaf}' -> '{target_path}'")
        except Exception as e:
            print(f"移动失败：'{leaf}'\n错误信息：{str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python move_leaves.py 源目录 目标目录")
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2]

    if not os.path.isdir(source_dir):
        print(f"错误：源目录 '{source_dir}' 不存在")
        sys.exit(1)

    move_leaf_dirs(source_dir, target_dir)

    #bash脚本 python move_leaves.py /path/to/source /path/to/target