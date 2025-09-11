import os
import shutil
""""
批量将多级目录下后缀为gz的文件移动到指定到目录的python脚本
"""
def move_gz_files(source_folder, target_folder):
    # 如果目标文件夹不存在，则创建它
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 遍历 source_folder 中的所有子文件夹和文件
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            if file_name.endswith('.gz'):
                old_file_path = os.path.join(root, file_name)
                new_file_path = os.path.join(target_folder, file_name)

                # 移动文件到目标文件夹
                shutil.move(old_file_path, new_file_path)
                print(f'Moved: {old_file_path} -> {new_file_path}')
if __name__=="__main__":
    # 使用示例
    source_folder_path = "/mnt/data/new500/50_1_bak/labelnii_yijieya"  # 替换为源文件夹路径
    target_folder_path = "/mnt/data/new500/50_1/labelniigz"   # 替换为目标文件夹路径

    move_gz_files(source_folder_path, target_folder_path)
