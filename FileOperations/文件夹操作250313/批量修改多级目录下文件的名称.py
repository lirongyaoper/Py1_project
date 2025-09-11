import os
""""
将多级目录下的A.nii.gz文件修改为pulmonary artery.nii.gz，
将B.nii.gz文件修改为bronchus.nii.gz ，
将V.nii.gz文件修改为pulmonary veins.nii.gz 
同时该脚本具有批量处理多个子文件夹的能力
"""
def rename_nifti_files_in_subfolders(parent_folder):
    # 遍历 parent_folder 中的所有子文件夹和文件
    for root, dirs, files in os.walk(parent_folder):
        for file_name in files:
            old_file_path = os.path.join(root, file_name)
            new_file_name = ""

            # 检查文件名并设置新的文件名
            if file_name == 'A.nii.gz':
                new_file_name = 'pulmonary artery.nii.gz'
            elif file_name == 'B.nii.gz':
                new_file_name = 'bronchus.nii.gz'
            elif file_name == 'V.nii.gz':
                new_file_name = 'pulmonary veins.nii.gz'

            # 如果新文件名不为空，则进行重命名
            if new_file_name:
                new_file_path = os.path.join(root, new_file_name)

                # 确保新文件名不同于旧文件名
                if old_file_path != new_file_path:
                    os.rename(old_file_path, new_file_path)
                    print(f'Renamed: {old_file_path} -> {new_file_path}')
                else:
                    print(f'File already has the desired name: {new_file_path}')
if __name__ == "__main__":
    parent_folder_path = "/mnt/data/n500last/297/nii"  # 替换为目标父文件夹路径
    rename_nifti_files_in_subfolders(parent_folder_path)
