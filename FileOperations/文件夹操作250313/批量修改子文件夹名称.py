import os
"""
批量修改子文件夹的名称，子文件夹的名称按照事先约定的格式进行命名，如  CASE_101y, CASE_102y, ...
"""

import os


def rename_subfolders(root_directory):
    # 获取根目录下的所有子文件夹
    subfolders = [f.path for f in os.scandir(root_directory) if f.is_dir()]

    # 遍历每个子文件夹并重命名
    for index, subfolder in enumerate(subfolders, start=203):
        # 生成新的文件夹名称
        new_name = f"C_CASE{index:03d}y"  # 格式化编号为3位数字
        new_folder_path = os.path.join(root_directory, new_name)

        # 确保新的文件夹名称不重复
        if not os.path.exists(new_folder_path):
            os.rename(subfolder, new_folder_path)
            print(f'Renamed: {subfolder} -> {new_folder_path}')
        else:
            print(f'Folder already exists, skipping: {new_folder_path}')

if __name__ =="__main__":
    # 使用示例
    parent_folder_path = "/mnt/data/n500last/297"  # 替换为目标文件夹路径
    rename_subfolders(parent_folder_path)
