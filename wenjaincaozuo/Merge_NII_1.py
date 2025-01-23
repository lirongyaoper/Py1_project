import nibabel as nib
import numpy as np
import os
import shutil
import gzip
import SimpleITK as sitk
import time

# 合并标签
def merge_labels(input_folder, output_file):
    """
    合并多个标签文件，保证在重叠区域不合并，不重叠的地方才合并，且每个标签文件的标签值不同。
    :param input_folder: 包含多个标签 NIfTI 文件的文件夹路径
    :param output_file: 合并后保存的输出文件路径
    """
    nii_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.nii') or f.lower().endswith('.nii.gz')]

    nii_path = os.path.join(input_folder, nii_files[0])
    image = sitk.ReadImage(nii_path)  # 读取nii文件
    imageArray = sitk.GetArrayFromImage(image) # 转成数组

    allArray = np.zeros_like(imageArray, dtype=np.uint8)  # 创建空的全0数组

    i = 1
    for nii in nii_files:
        a = nii[:-4]
        if a == "pulmonary_artery" or a == "pulmonary_veins" or a == "pulmonary_nodules" or a == "left_lung" or a == "right_lung" or a == "bronchus": # 合并指定器官
            file_path = os.path.join(input_folder, nii)
            image1 = sitk.ReadImage(file_path)
            imageArray = sitk.GetArrayFromImage(image1)
            # allArray[imageArray != 0] = 1   # 所有标签全部设为1
            # 如果需要不同器官不同颜色，就取消下面两行注释
            allArray[imageArray != 0 ] = i
            i+=1

    allImage = sitk.GetImageFromArray(allArray)  # 从数组转为图像
    allImage.CopyInformation(image)
    sitk.WriteImage(allImage, output_file)


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


folder_path = '/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/300label'   # nii 文件所在位置
subfolder_names = get_subfolder_names(folder_path)  # 所有文件夹名

for folderPath in subfolder_names:
    slices_folder = os.path.join(folder_path, folderPath, "nii/stlNii")
    nii_gz_names = get_subfolder_names(slices_folder)

    for nii in nii_gz_names:
        # a = nii[:4]
        if nii[-3:] == ".gz":
            decompress_nifti_gz(os.path.join(slices_folder, nii))
            os.remove(os.path.join(slices_folder, nii))
        if nii[:5] == "merge":
            os.remove(os.path.join(slices_folder, nii))
    merge_nii = os.path.join(slices_folder, "merge.nii.gz")
    merge_labels(slices_folder, merge_nii)

