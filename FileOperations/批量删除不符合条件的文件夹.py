import os
import shutil
def count_files_in_folders(root_dir):

    # 遍历根目录下的所有条目
    for entry in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, entry)

        # 确保是文件夹且不是符号链接
        if os.path.isdir(folder_path) and not os.path.islink(folder_path):

            # 统计文件数量（不包含子文件夹）
            files = [
                f for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f))
            ]
            # print(folder_path)

            if(len(files)!=2):
                # print(folder_path)
                shutil.rmtree(folder_path)  # 删除文件夹及其内容
                print(f"已删除文件夹: {folder_path}")






def delete_folders(directory):
    """
    删除指定目录下的所有子文件夹
    :param directory: 目标目录
    """
    # 确保目标目录存在
    if not os.path.exists(directory):
        print(f"目录不存在: {directory}")
        return

    # 遍历目录
    for foldername in os.listdir(directory):
        folder_path = os.path.join(directory, foldername)

        # 判断是否为文件夹
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)  # 删除文件夹及其内容
            print(f"已删除文件夹: {folder_path}")

if __name__ == "__main__":
    # # 设置要删除文件夹的目标目录
    # target_directory = "./target_directory"  # 替换为实际的目标目录路径
    #
    # # 调用函数删除文件夹
    # delete_folders(target_directory)



    path11 = r"/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/257/images/case97nii"
    count_files_in_folders(path11)