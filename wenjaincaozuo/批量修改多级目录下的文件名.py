import os


def rename_files_in_directory(root_dir, old_str, new_str):
    # 遍历根目录及其所有子目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # 检查文件名中是否包含指定的字符串
            if old_str in filename:
                # 构建新的文件名
                new_filename = filename.replace(old_str, new_str)
                # 生成完整的旧路径和新路径
                old_file_path = os.path.join(dirpath, filename)
                new_file_path = os.path.join(dirpath, new_filename)

                # 重命名文件
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} to {new_file_path}')


# 使用示例
if __name__ == "__main__":
    root_directory = '/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/shuju500/300labels'  # 替换为目标目录路径
    string_to_replace = '支气管.nii.gz'  # 替换为要修改的字符串
    replacement_string = 'bronchus.nii.gz'  # 替换为新的字符串

    rename_files_in_directory(root_directory, string_to_replace, replacement_string)
