import os
"""
按照给定文件名（包含多个文件名）批量查找子目录内的文件，
若存在与给定文件名不同的文件，列出该文件所在的目录

"""

def find_different_files(base_directory, filenames):
    # 将文件名转换为集合，以便高效查找
    target_filenames = set(filenames)

    # 用于保存不同文件的目录
    different_files_dirs = []

    # 遍历目录及其所有子目录
    for root, dirs, files in os.walk(base_directory):
        # 找到当前目录下的文件
        current_files = set(files)

        # 检查是否存在与给定文件名不同的文件
        if current_files != target_filenames:
            # 存在不同的文件，保存该目录
            different_files_dirs.append(root)

    return different_files_dirs

if __name__=="__main__":
    # 使用示例
    base_directory = "/mnt/data/n500last/297/nii"  # 替换为目标主目录路径
    file_names_to_check = ["pulmonary artery.nii.gz", "bronchus.nii.gz","pulmonary veins.nii.gz"]  # 替换为要检查的文件名列表

    # 调用函数查找不同的文件所在目录
    different_dirs = find_different_files(base_directory, file_names_to_check)

    # 输出结果
    if different_dirs:
        print("以下目录包含与给定文件名不同的文件：")
        for dir in different_dirs:
            print(f" - {dir}")
    else:
        print("所有子目录包含的文件均与给定文件名一致。")
