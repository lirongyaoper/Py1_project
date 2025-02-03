import os


def count_files_in_folders(root_dir):
    """
    统计指定目录下所有子文件夹中的文件数量
    :param root_dir: 要扫描的根目录路径
    """
    print(f"\n{' 文件夹路径 ':^40} | {' 文件数量 ':^10}")
    print('-' * 55)

    # 遍历根目录下的所有条目
    for entry in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, entry)

        # 确保是文件夹且不是符号链接
        if os.path.isdir(folder_path) and not os.path.islink(folder_path):
            try:
                # 统计文件数量（不包含子文件夹）
                files = [
                    f for f in os.listdir(folder_path)
                    if os.path.isfile(os.path.join(folder_path, f))
                ]
                if(len(files)!=2):
                    print(f"{folder_path:<40} | {len(files):>10}")

            except PermissionError:
                print(f"{folder_path:<40} | {'权限不足':>10}")
            except Exception as e:
                print(f"{folder_path:<40} | 错误: {str(e)}")


if __name__ == "__main__":
    # 使用示例
    target_dir = r"/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/databasebak_center/500/images_yuanshi/300nii"

    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        count_files_in_folders(target_dir)
    else:
        print("错误：指定的路径不存在或不是目录")