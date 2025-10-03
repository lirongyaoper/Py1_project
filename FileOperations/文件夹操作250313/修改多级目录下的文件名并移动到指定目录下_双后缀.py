import os
import shutil

def rename_and_move_files(source_folder, target_folder):
    # 如果目标文件夹不存在，则创建它
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 遍历 source_folder 中的所有子文件夹和文件
    for root, dirs, files in os.walk(source_folder):
        # 获取当前目录的名称
        dir_name = os.path.basename(root)

        for file_name in files:
            # 确保文件是双后缀格式，如果您需要处理特定格式请根据需求调整
            if len(file_name.split('.')) >= 2:
                # 生成新文件名，保持双后缀
                new_file_name = f"{dir_name}.{file_name.split('.')[-2]}.{file_name.split('.')[-1]}"
                old_file_path = os.path.join(root, file_name)
                new_file_path = os.path.join(target_folder, new_file_name)

                # 移动并重命名文件
                shutil.move(old_file_path, new_file_path)
                print(f'Moved and renamed: {old_file_path} -> {new_file_path}')
if __name__ == "__main__":
    # 使用示例
    source_folder_path = "/mnt/data/origin20"  # 替换为源文件夹路径
    target_folder_path = "/mnt/data/orign20image/"   # 替换为目标文件夹路径

    rename_and_move_files(source_folder_path, target_folder_path)
