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
def delete_part_of_filename(folder_path, start_index, end_index):
    """
    批量删除文件名中的部分字符
    :param folder_path: 文件所在的目录
    :param start_index: 开始索引（包含）
    :param end_index: 结束索引（不包含）
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            filename_split = get_double_extension(filename)
            modified_name = filename_split[0][:start_index] + filename_split[0][end_index:]
            new_file_path = os.path.join(folder_path, f"{modified_name}{filename_split[1]}")
            # print(new_file_path)
            os.rename(file_path, new_file_path)
            print(f"已将文件 '{filename}' 重命名为 '{modified_name}{filename_split[1]}'")

# 示例使用
folder_path = r'/home/lirongyaoper/Documents/300labelnii'  # 替换为实际的文件夹路径
start_index = 0 # 开始索引，包含在内
end_index = 3  # 结束索引，不包含在内
delete_part_of_filename(folder_path, start_index, end_index)
