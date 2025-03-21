import os

def rename_gz_to_nifti(folder_path):
    # 遍历 folder_path 中的所有子文件夹和文件
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.gz'):
                old_file_path = os.path.join(root, file_name)
                new_file_name = file_name[:-3] + '.nii.gz'  # 修改后缀
                new_file_path = os.path.join(root, new_file_name)

                # 重命名文件
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} -> {new_file_path}')

if __name__ =="__main__":
    # 使用示例
    folder_path = "/mnt/data/new500/50/lung50imageniigz"  # 替换为目标文件夹路径
    rename_gz_to_nifti(folder_path)
