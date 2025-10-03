import os
import gzip
import shutil


def compress_nifti_files(root_directory):
    # 遍历 root_directory 下的所有子目录
    for root, dirs, files in os.walk(root_directory):
        for file_name in files:
            if file_name == "volume.nii":
                file_path = os.path.join(root, file_name)
                compressed_file_path = f"{file_path}.gz"

                # 压缩文件
                with open(file_path, 'rb') as f_in:
                    with gzip.open(compressed_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                print(f'Compressed: {file_path} -> {compressed_file_path}')

                # 可选：压缩完成后删除原始文件
                os.remove(file_path)
                print(f'Deleted original file: {file_path}')

if __name__=="__main__":
    # 使用示例
    root_directory_path = "/mnt/data/origin20"  # 替换为根目录路径
    compress_nifti_files(root_directory_path)
