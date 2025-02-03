import os
import zipfile


def unzip_files(src_directory, dest_directory):
    """
    批量解压指定目录下的所有.zip文件
    :param src_directory: 源目录，包含.zip文件
    :param dest_directory: 目标目录，解压后的文件存放位置
    """
    # 确保目标目录存在
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    # 遍历源目录中的所有.zip文件
    for filename in os.listdir(src_directory):
        if filename.endswith('.zip'):
            zip_file_path = os.path.join(src_directory, filename)
            # 构造解压缩后的存储路径
            extract_path = os.path.join(dest_directory, os.path.splitext(filename)[0])  # 不带扩展名的文件夹

            # 确保解压路径存在
            if not os.path.exists(extract_path):
                os.makedirs(extract_path)

            # 解压缩文件
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                print(f"已解压: {zip_file_path} 到 {extract_path}")


if __name__ == "__main__":
    # 设置源目录和目标目录
    source_dir = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/257/images/case97zip"  # 替换为实际的源目录路径
    destination_dir = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/257/images/case97"  # 替换为实际的目标目录路径

    # 调用函数解压缩文件
    unzip_files(source_dir, destination_dir)
