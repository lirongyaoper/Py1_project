import os


def add_prefix_to_files(directory, prefix):
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        # 构建原文件路径
        old_file_path = os.path.join(directory, filename)

        # 确保是文件而不是目录
        if os.path.isfile(old_file_path):
            # 创建新的文件名
            new_filename = prefix + filename
            new_file_path = os.path.join(directory, new_filename)

            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f"已将文件 {old_file_path} 重命名为 {new_file_path}")


# 示例使用
if __name__ == "__main__":
    directory_path = "/mnt/data/103/imagesniia/"  # 替换为您要处理的目录路径
    prefix_to_add = "lry_"  # 替换为您希望添加的前缀

    add_prefix_to_files(directory_path, prefix_to_add)
