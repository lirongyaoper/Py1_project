import os

def delete_specific_files(root_directory, file_names):
    # 检查根目录是否存在
    if not os.path.exists(root_directory):
        print(f"Directory does not exist: {root_directory}")
        return

    # 遍历根目录及其子目录
    for root, dirs, files in os.walk(root_directory):
        for file_name in files:
            if file_name in file_names:
                file_path = os.path.join(root, file_name)

                # 删除文件
                os.remove(file_path)
                print(f'Deleted: {file_path}')

if __name__=="__main__":
    # 使用示例
    root_directory_path = "/mnt/data/n500last/297/nii/"  # 替换为根目录路径
    files_to_delete = [
        "lung_nodules.nii.gz",
        "up_main.nii.gz",
        "lung.nii.gz",
        "T3.nii.gz",
        "T4.nii.gz",
        "T5.nii.gz",
        "L.nii.gz",
        "T1.nii.gz",
        "T2.nii.gz",
        "T6.nii.gz",
        "T7.nii.gz",
        "T8.nii.gz",
        "T9.nii.gz",
        "T10.nii.gz",
        "T.nii.gz",
        "TT.nii.gz",
    ]

    delete_specific_files(root_directory_path, files_to_delete)
