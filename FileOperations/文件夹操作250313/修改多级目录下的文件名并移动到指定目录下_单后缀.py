import os
import shutil
"""
批量将多级目录下文件的名称修改成与所在目录同名的文件，并将修改后的文件移动到指定的目录下
"""

def rename_and_move_files(parent_folder, destination_folder):
    # 确保目标目录存在
    os.makedirs(destination_folder, exist_ok=True)

    # 遍历 parent_folder 中的所有文件和文件夹
    for root, dirs, files in os.walk(parent_folder):
        # 获取当前目录的文件夹名称
        current_folder_name = os.path.basename(root)

        for file_name in files:
            # 构建原始文件的完整路径
            old_file_path = os.path.join(root, file_name)

            # 创建新的文件名，保留原文件扩展名
            file_extension = os.path.splitext(file_name)[1]
            new_file_name = f"{current_folder_name}{file_extension}"

            # 构建新文件的完整路径
            new_file_path = os.path.join(destination_folder, new_file_name)

            # 移动并重命名文件
            shutil.move(old_file_path, new_file_path)
            print(f"Moved: {old_file_path} -> {new_file_path}")

if __name__=="__main__":
# 使用示例
    parent_folder_path = "/mnt/data/new500/50_1"  # 替换为目标文件夹路径
    destination_folder_path = "/mnt/data/new500/50_1_bak/imageniigz"  # 替换为指定的目标路径
    rename_and_move_files(parent_folder_path, destination_folder_path)
