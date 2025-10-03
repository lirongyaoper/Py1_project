import os


def add_suffix_to_files(directory):
    # 遍历目录中的所有文件
    for file_name in os.listdir(directory):
        # 构造文件的完整路径
        file_path = os.path.join(directory, file_name)

        # 检查是否为文件，而不是目录
        if os.path.isfile(file_path):
            # 检查文件名是否已经包含 .nii.gz 后缀
            if not file_name.endswith('.nii.gz'):
                # 新的文件名
                new_file_name = file_name + '.nii.gz'
                new_file_path = os.path.join(directory, new_file_name)

                # 重命名文件
                os.rename(file_path, new_file_path)
                print(f'Renamed: {file_path} -> {new_file_path}')

if __name__=="__main__":
    # 使用示例
    directory_path = "/mnt/data/new500/labelniigz"  # 替换为您的目标目录路径

    add_suffix_to_files(directory_path)
