import nibabel as nib
import numpy as np

def split_nifti_file(merged_file, slice_index1, slice_index2, output_file1, output_file2):
    # 读取合并后的 NIfTI 文件
    merged_img = nib.load(merged_file)
    merged_data = merged_img.get_fdata()

    # 检查切片索引范围
    if slice_index1 < 0 or slice_index2 < 0 or slice_index1 >= merged_data.shape[-1] or slice_index2 >= merged_data.shape[-1]:
        raise ValueError("切片索引超出范围")

    # 提取两个切片
    slice1 = merged_data[..., slice_index1:slice_index1 + 1]  # 保持维度
    slice2 = merged_data[..., slice_index2:slice_index2 + 1]  # 保持维度

    # 创建 NIfTI 图像
    img1 = nib.Nifti1Image(slice1, merged_img.affine, merged_img.header)
    img2 = nib.Nifti1Image(slice2, merged_img.affine, merged_img.header)

    # 保存拆分后的文件
    nib.save(img1, output_file1)
    nib.save(img2, output_file2)
    print(f"已拆分文件并保存为: {output_file1} 和 {output_file2}")


if __name__=='__main__':
    # 示例使用
    split_nifti_file('/mnt/data/xin257/103/STL_NII/a7/lung_vessel.nii', 0, 1, '/mnt/data/xin257/103/STL_NII/a7/file1.nii', '/mnt/data/xin257/103/STL_NII/a7/file2.nii')
