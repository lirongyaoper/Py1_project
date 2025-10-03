import os

def add_suffix_to_files(dir1, dir2):
    # 获取目录1和目录2中的文件列表
    files_dir1 = os.listdir(dir1)
    files_dir2 = os.listdir(dir2)

    # 创建一个集合，找出两个目录中同名的文件
    common_files = set(files_dir1) & set(files_dir2)

    # 初始化递增数字，从 1029 开始
    increment = 1029

    for file_name in common_files:
        # 只处理 .nii.gz 后缀文件
        if file_name.endswith('.nii.gz'):
            # 获取文件的完整路径
            file_path_1 = os.path.join(dir1, file_name)
            file_path_2 = os.path.join(dir2, file_name)

            # 生成新的文件名
            base_name = file_name[:-len('.nii.gz')]  # 去掉扩展名
            new_suffix = f'_{increment:04d}'  # 以四位数格式生成后缀
            new_file_name = f'{base_name}{new_suffix}.nii.gz'

            # 添加后缀到第一个目录的文件
            new_file_path_1 = os.path.join(dir1, new_file_name)
            os.rename(file_path_1, new_file_path_1)

            # 添加后缀到第二个目录的文件
            new_file_path_2 = os.path.join(dir2, new_file_name)
            os.rename(file_path_2, new_file_path_2)

            print(f'Renamed: {file_path_1} -> {new_file_path_1}')
            print(f'Renamed: {file_path_2} -> {new_file_path_2}')

            # 递增数字
            increment += 1

if __name__=="__main__":
    # 使用示例
    dir1 = "/mnt/data/n500last/493/images"  # 替换为第一个目录路径
    dir2 = "/mnt/data/n500last/493/labels"  # 替换为第二个目录路径

    add_suffix_to_files(dir1, dir2)
