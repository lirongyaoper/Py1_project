import os
import gzip
import shutil


def compress_nii_to_gz(root_directory):
    # 遍历根目录及其所有子目录
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            # 检查文件是否为 .nii 格式
            if filename.endswith('.nii') and filename.startswith('volume'):
                file_path = os.path.join(dirpath, filename)
                gz_file_path = os.path.join(dirpath, filename + '.gz')

                # 压缩文件
                with open(file_path, 'rb') as f_in:
                    with gzip.open(gz_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                print(f"已将 {file_path} 压缩为 {gz_file_path}")


# 示例使用
if __name__ == "__main__":
    root_directory_path = "/mnt/data/103/label"  # 替换为您的根目录路径
    compress_nii_to_gz(root_directory_path)
