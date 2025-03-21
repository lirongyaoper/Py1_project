import os
import shutil
"""
批量将最后一级名为images的文件夹修改为其父文件夹的名称，并将修改后的文件移动到指定的目录下
"""

def rename_and_move_images(parent_folder, destination_folder):
    # 确保目标目录存在
    os.makedirs(destination_folder, exist_ok=True)

    # 遍历 parent_folder 中的所有内容
    for root, dirs, files in os.walk(parent_folder):
        for dir_name in dirs:
            # 检查文件夹名是否为 'images'
            if dir_name == 'nii':
                # 获取父文件夹名称
                parent_folder_name = os.path.basename(os.path.dirname(os.path.join(root, dir_name)))

                # 创建新的文件夹名称
                new_folder_name = parent_folder_name

                # 构建原始和新文件夹路径
                old_folder_path = os.path.join(root, dir_name)
                new_folder_path = os.path.join(root, new_folder_name)

                # 重命名文件夹
                os.rename(old_folder_path, new_folder_path)
                print(f"Renamed: {old_folder_path} -> {new_folder_path}")

                # 移动重命名后的文件夹到目标目录
                shutil.move(new_folder_path, destination_folder)
                print(f"Moved: {new_folder_path} -> {destination_folder}")


if __name__=="__main__":
    # 使用示例
    parent_folder_path = "/mnt/data/n500last/297"  # 替换为目标文件夹路径
    destination_folder_path = "/mnt/data/n500last/297_bak/nii/"  # 替换为指定的目标路径
    rename_and_move_images(parent_folder_path, destination_folder_path)
