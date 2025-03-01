import os


def rename_files_in_directory(directory):
    # 遍历指定目录中的所有文件
    for filename in os.listdir(directory):
        # 检查文件名是否以数字开头
        if filename[0].isdigit():
            new_filename = f"CASE{filename}"  # 新文件名
            print(new_filename)
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)

            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f"已将 {old_file_path} 重命名为 {new_file_path}")


# 示例使用
if __name__ == "__main__":
    directory_path = "/mnt/data/lungCT/databasebak_center/1009/labels"  # 替换为您的目录路径
    rename_files_in_directory(directory_path)
