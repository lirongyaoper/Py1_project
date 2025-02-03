import os
import shutil


def move_files_with_extension(src_directory, dest_directory, file_extension):
    # 确保目标目录存在
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    # 遍历源目录及其子目录
    for root, _, files in os.walk(src_directory):
        for filename in files:
            # 检查文件后缀
            if filename.endswith(file_extension):
                source_file_path = os.path.join(root, filename)
                destination_file_path = os.path.join(dest_directory, filename)

                # 移动文件
                shutil.move(source_file_path, destination_file_path)
                print(f"已移动文件: {source_file_path} 到 {destination_file_path}")


if __name__ == "__main__":
    # 设置源目录、目标目录和文件后缀
    source_dir = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/257/images/case97nii_1"  # 替换为实际的源目录路径
    destination_dir = "/home/lirongyaoper/Documents/case97nii"  # 替换为实际的目标目录路径
    file_ext = ".nii.gz"  # 替换为需要移动的文件后缀

    # 调用函数移动文件
    move_files_with_extension(source_dir, destination_dir, file_ext)
