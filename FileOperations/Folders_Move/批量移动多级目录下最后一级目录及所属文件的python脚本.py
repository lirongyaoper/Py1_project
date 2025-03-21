import os
import shutil

def move_last_level_directories(root_dir, destination):
    # 遍历根目录下面的所有目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 检查当前目录是否为最后一级目录
        if not dirnames:  # 如果 dirnames 为空，说明是最后一级目录
            try:
                # 构建目标路径
                target_path = os.path.join(destination, os.path.basename(dirpath))
                # 移动目录及其内容
                shutil.move(dirpath, target_path)
                print(f"已移动目录: {dirpath} 到 {target_path}")
            except Exception as e:
                print(f"移动目录 {dirpath} 时出错: {e}")

# 示例使用
if __name__ == "__main__":
    root_directory = "/mnt/data/new500/labelnii"  # 替换为您要搜索的根目录路径
    destination_directory = "/mnt/data/new500/labelniinew"  # 替换为目标路径

    move_last_level_directories(root_directory, destination_directory)
