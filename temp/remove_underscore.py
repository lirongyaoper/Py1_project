import os


def remove_underscores_from_filenames(directory):
    # 确保目录存在
    if not os.path.isdir(directory):
        print(f"目录 '{directory}' 不存在!")
        return

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 创建新的文件名，去掉“_”字符
        new_filename = filename.replace("_", "")

        # 仅在文件名变化时进行重命名
        if new_filename != filename:
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            # print(old_file_path)
            # print(new_file_path)
            # print("#################################################################################")
            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f"已将 {old_file_path} 重命名为 {new_file_path}")


# 示例使用
if __name__ == "__main__":
    directory_path = "/mnt/data/lungCT/databasebak_center/1009/labels/"  # 替换为您的目录路径
    remove_underscores_from_filenames(directory_path)
