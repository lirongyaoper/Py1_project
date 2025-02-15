import nibabel as nib
import numpy as np
import os
import shutil
import gzip
import SimpleITK as sitk
import time

def split_labels(input_file, output_folder):
    """
    将包含标签 1 和 2 的 NIfTI 标签文件拆分成两个单独的标签文件，
    其中一个只有标签 1，另外一个只有标签 2。

    :param input_file: 输入的 NIfTI 标签文件路径
    :param output_folder: 拆分后文件保存的输出文件夹路径
    """
    # 读取 NIfTI 文件
    image = sitk.ReadImage(input_file)
    # 将图像转换为 NumPy 数组
    image_array = sitk.GetArrayFromImage(image)

    # 创建只包含标签 1 的数组
    label_1_array = np.zeros_like(image_array, dtype=np.uint8)
    label_1_array[image_array == 1] = 1

    # 创建只包含标签 2 的数组
    label_2_array = np.zeros_like(image_array, dtype=np.uint8)
    label_2_array[image_array == 2] = 2

    # 将数组转换为 SimpleITK 图像
    label_1_image = sitk.GetImageFromArray(label_1_array)
    label_1_image.CopyInformation(image)

    label_2_image = sitk.GetImageFromArray(label_2_array)
    label_2_image.CopyInformation(image)

    # 构建输出文件路径
    output_file_1 = os.path.join(output_folder, "Artery.nii.gz") # 动脉
    output_file_2 = os.path.join(output_folder, "vein.nii.gz") # 静脉

    # 保存拆分后的文件
    sitk.WriteImage(label_1_image, output_file_1)
    sitk.WriteImage(label_2_image, output_file_2)


def get_subfolder_names(dir):
    # 获取指定路径下的所有内容
    subfolders = [f.name for f in os.scandir(dir) if f.is_dir() or f.is_file()]
    return subfolders

# 解压 nii.gz
def decompress_nifti_gz(input_file):
    """
    解压 .nii.gz 文件为 .nii 文件
    :param input_file: 输入的 .nii.gz 文件路径
    :return: 解压后的 .nii 文件路径
    """
    output_file = input_file[:-3]  # 删除 .gz 后缀，获得输出路径
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"文件已解压为: {output_file}")
    return output_file


folder_path = r'/mnt/data/103/label/'   # nii_gz 文件夹位置
subfolder_names = get_subfolder_names(folder_path) # 获取所有nii_gz文件

for folderPath in subfolder_names:
    slices_folder = os.path.join(folder_path, folderPath)
    # print(slices_folder)
    nii_gz_names = get_subfolder_names(slices_folder)
    # print(nii_gz_names)
    for nii_gz in nii_gz_names:
        a = nii_gz[:-7]
        if a == "lung_vessel":   # 只拆分这个nii.gz
            nii_gz_path = os.path.join(slices_folder, nii_gz)
            # print(nii_gz_path)
            decompress_nifti_gz(nii_gz_path)  # 解压nii.gz为nii
            os.remove(nii_gz_path)  # 删除nii.gz
            split_labels(nii_gz_path, slices_folder)  # 拆分

