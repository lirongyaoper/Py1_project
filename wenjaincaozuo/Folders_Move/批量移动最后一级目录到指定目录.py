import os
import shutil


def move_last_level_dirs(src_directory, dest_directory):
    """
    移动源目录下的所有最后一级目录到目标目录
    :param src_directory: 源目录
    :param dest_directory: 目标目录
    """
    # 确保目标目录存在
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    # 遍历源目录
    for root, dirs, _ in os.walk(src_directory):
        # 如果当前目录是最后一级目录且不为空
        if not dirs:
            # 获取最后一级目录
            last_level_dir = os.path.basename(root)
            source_path = root

            # 构造目标路径
            destination_path = os.path.join(dest_directory, last_level_dir)

            # 移动目录
            shutil.move(source_path, destination_path)
            print(f"已移动目录: {source_path} 到 {destination_path}")


if __name__ == "__main__":
    # 设置源目录和目标目录
    source_dir = "/mnt/data/103/STL_NII"  # 替换为实际的源目录路径
    destination_dir = "/mnt/data/103/label"  # 替换为实际的目标目录路径

    # 调用函数移动最后一级目录
    move_last_level_dirs(source_dir, destination_dir)
