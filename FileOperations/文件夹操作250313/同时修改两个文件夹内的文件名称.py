import os

"""
    同时按照指定格式修改两个文件夹内同名的文件名，
    使修改后的文件名仍保持一致。
    指定格式如下 CS_CASE_001y,其中001为递增的数值，每次递增1
"""

def rename_matching_files(dir1, dir2):
    # 获取两个目录下的所有文件，并筛选出 .nii.gz 后缀的文件
    files1 = {file_name: os.path.join(dir1, file_name) for file_name in os.listdir(dir1) if
              file_name.endswith('.nii.gz')}
    files2 = {file_name: os.path.join(dir2, file_name) for file_name in os.listdir(dir2) if
              file_name.endswith('.nii.gz')}

    # 查找两个目录中相同的文件名（不包括后缀）
    common_files = set(f[:-7] for f in files1.keys()).intersection(set(f[:-7] for f in files2.keys()))

    # 进行重命名
    for index, file_name in enumerate(common_files, start=1):
        new_name = f'CASE{index:04d}y.nii.gz'  # 生成新的文件名
        new_path1 = os.path.join(dir1, new_name)
        new_path2 = os.path.join(dir2, new_name)

        # 重命名文件
        os.rename(files1[file_name + '.nii.gz'], new_path1)
        os.rename(files2[file_name + '.nii.gz'], new_path2)

        print(f'Renamed: {files1[file_name + ".nii.gz"]} -> {new_path1}')
        print(f'Renamed: {files2[file_name + ".nii.gz"]} -> {new_path2}')


if __name__ =="__main__":
    # 使用示例
    directory1 = "/mnt/data/lungCT/databasebak_center/1522/imagesTr"  # 替换为第一个目录路径
    directory2 = "/mnt/data/lungCT/databasebak_center/1522/labelsTr"  # 替换为第二个目录路径

    rename_matching_files(directory1, directory2)
