import os
import zipfile


def unzip_files_in_directory(root_dir, output_dir):
    # 检查输出目录是否存在，若不存在则创建
    os.makedirs(output_dir, exist_ok=True)

    # 遍历根目录下的所有文件
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.zip'):
                zip_file_path = os.path.join(dirpath, filename)
                # 为解压后的文件构建输出路径
                output_path = os.path.join(output_dir, os.path.splitext(filename)[0])

                try:
                    # 创建文件夹以存放解压后的文件
                    os.makedirs(output_path, exist_ok=True)
                    # 解压 ZIP 文件
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        zip_ref.extractall(output_path)
                    print(f"已解压 ZIP 文件: {zip_file_path} 到 {output_path}")
                except Exception as e:
                    print(f"解压文件 {zip_file_path} 时出错: {e}")


# 示例使用
if __name__ == "__main__":
    root_directory = "/mnt/data/103/原始数据/"  # 替换为包含 ZIP 文件的目录
    output_directory = "/mnt/data/103/images/"  # 替换为解压后文件存放的目录

    unzip_files_in_directory(root_directory, output_directory)
