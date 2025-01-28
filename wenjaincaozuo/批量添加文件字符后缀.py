import os
def get_double_extension(filename):
    # 首先获取第一个后缀
    root, ext1 = os.path.splitext(filename)

    # 再尝试获取第二个后缀
    root, ext2 = os.path.splitext(root)

    if ext2:
        # 如果存在第二个后缀，说明这是双后缀
        return root ,ext2 + ext1
    else:
        # 如果不存在第二个后缀，返回单一后缀
        return root,ext1
def add_suffix_to_filenames(folder_path, suffix):
    """
    批量为文件名添加后缀
    :param folder_path: 文件所在的目录
    :param suffix: 要添加的后缀
    """
    # 获取指定目录下的所有文件
    for filename in os.listdir(folder_path):
        # 检查是否为文件（忽略文件夹）
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)
            filename_split = get_double_extension(filename)

            # 构建新的文件名
            new_filename = f"{filename_split[0]}{suffix}{filename_split[1]}"
            print(new_filename)
            new_file_path = os.path.join(folder_path, new_filename)
            # # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"已将文件 '{filename}' 重命名为 '{new_filename}'")

# 示例使用
folder_path = r'/home/lirongyaoper/Documents/300labelnii/'  # 替换为实际的文件夹路径
suffix = '_'                 # 要添加的后缀
add_suffix_to_filenames(folder_path, suffix)
