import os
import shutil

def move_last_level_folders(src_directory, dest_directory):
    """
    移动源目录中最后一级文件夹及其文件到目标目录
    :param src_directory: 源目录
    :param dest_directory: 目标目录
    """
    # 确保目标目录存在
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    # 遍历源目录
    for root, dirs, files in os.walk(src_directory):
        # 确保找到最后一级文件夹
        if not dirs:  # 如果没有子文件夹，则为最后一级
            folder_name = os.path.basename(root)
            # 创建新的目标路径
            dest_folder_path = os.path.join(dest_directory, folder_name)

            # 移动最后一级文件夹及其内容
            shutil.move(root, dest_folder_path)
            print(f"已移动文件夹及其内容: {root} 到 {dest_folder_path}")

if __name__ == "__main__":
    # 设置源目录和目标目录
    source_dir = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/shuju500/300标注数据"  # 替换为实际的源目录路径
    destination_dir = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/shuju500/300labels"  # 替换为实际的目标目录路径

    # 调用函数移动文件夹及其文件
    move_last_level_folders(source_dir, destination_dir)
