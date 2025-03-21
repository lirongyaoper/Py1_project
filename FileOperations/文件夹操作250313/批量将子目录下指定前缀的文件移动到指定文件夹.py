import os
import shutil


def move_files_with_prefix(root_directory, target_directory, prefix):
    # 检查目标目录是否存在，如果不存在，创建它
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # 遍历 root_directory 下的所有子目录
    for root, dirs, files in os.walk(root_directory):
        for file_name in files:
            # 检查文件名是否以指定前缀开头
            if file_name.startswith(prefix):
                source_file_path = os.path.join(root, file_name)
                target_file_path = os.path.join(target_directory, file_name)

                # 移动文件
                shutil.move(source_file_path, target_file_path)
                print(f'Moved: {source_file_path} -> {target_file_path}')

if __name__ =="__main__":
    # 使用示例
    root_directory_path = "/mnt/data/n500last/297/nii"  # 替换为源目录路径
    target_directory_path = "/mnt/data/n500last/297/labels"  # 替换为目标目录路径
    file_prefix = "C_"  # 替换为您要查找的前缀

    move_files_with_prefix(root_directory_path, target_directory_path, file_prefix)
