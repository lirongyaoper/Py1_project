import os
import shutil
"""
批量将子目录中名为ref_image.nii.gz的文件修改为和所在目录同名的文件名，
注意保留.nii.gz双后缀格式，然后把修改后文件移动到指定目录
"""
def rename_and_move_files(source_directory, target_directory):
    # 遍历源目录中的所有子目录
    for root, dirs, files in os.walk(source_directory):
        for file_name in files:
            # 检查文件名是否为 ref_image.nii.gz
            if file_name == 'ref_image.nii.gz':
                # 获取当前目录的名称
                dir_name = os.path.basename(root)
                # 构造新的文件名
                new_file_name = f'{dir_name}.nii.gz'
                new_file_path = os.path.join(root, file_name)
                target_file_path = os.path.join(target_directory, new_file_name)

                # 重命名并移动文件
                shutil.move(new_file_path, target_file_path)
                print(f'Moved: {new_file_path} -> {target_file_path}')

# 使用示例
source_directory = "/mnt/data/n500last/297"  # 替换为源目录路径
target_directory = "/mnt/data/n500last/297_bak"   # 替换为目标目录路径
if __name__=="__main__":

    # 创建目标目录（如果不存在）
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    rename_and_move_files(source_directory, target_directory)
