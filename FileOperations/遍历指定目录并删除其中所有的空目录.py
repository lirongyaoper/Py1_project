import os

def remove_empty_dirs(directory):
    """
    删除指定目录下的所有空目录
    :param directory: 目标目录
    """
    # 遍历目录
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        # 遍历当前目录中的所有子目录
        for dirname in dirnames:
            dir_to_check = os.path.join(dirpath, dirname)
            # 如果目录为空，则删除它
            if not os.listdir(dir_to_check):
                os.rmdir(dir_to_check)
                print(f"已删除空目录: {dir_to_check}")

if __name__ == "__main__":
    # 设置要检查的目录
    target_directory = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/257/images/di160nii/"  # 替换为实际的目标目录路径

    # 调用函数删除空目录
    remove_empty_dirs(target_directory)
