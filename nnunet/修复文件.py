import SimpleITK as sitk
import numpy as np
import os


def compare_metadata(image, label, tol=1e-3):
    """
    比较两个图像的元数据（原点、间距、方向）
    返回比较结果和差异详情
    """
    mismatch = []
    details = {}

    # 比较原点（Origin）
    origin_diff = np.subtract(image.GetOrigin(), label.GetOrigin())
    if not np.allclose(image.GetOrigin(), label.GetOrigin(), atol=tol):
        mismatch.append("Origin")
        details['origin'] = {
            'image': image.GetOrigin(),
            'label': label.GetOrigin(),
            'diff': origin_diff.tolist()
        }

    # 比较间距（Spacing）
    spacing_diff = np.subtract(image.GetSpacing(), label.GetSpacing())
    if not np.allclose(image.GetSpacing(), label.GetSpacing(), atol=tol):
        mismatch.append("Spacing")
        details['spacing'] = {
            'image': image.GetSpacing(),
            'label': label.GetSpacing(),
            'diff': spacing_diff.tolist()
        }

    # 比较方向矩阵（Direction）
    if not np.allclose(image.GetDirection(), label.GetDirection(), atol=tol):
        mismatch.append("Direction")
        details['direction'] = {
            'image': image.GetDirection(),
            'label': label.GetDirection()
        }

    return len(mismatch) == 0, mismatch, details


def resample_label(label_img, reference_img):
    """
    使用参考图像的几何信息重新采样标签图像
    使用最近邻插值保持标签值不变
    """
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(reference_img)
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    resampler.SetDefaultPixelValue(0)
    resampler.SetOutputPixelType(label_img.GetPixelID())
    resampler.SetTransform(sitk.Transform())
    return resampler.Execute(label_img)


def process_image_pair(image_path, label_path, output_dir):
    """
    处理单个图像-标签对
    """
    try:
        # 读取图像
        image = sitk.ReadImage(image_path)
        label = sitk.ReadImage(label_path)

        # 比较元数据
        is_match, mismatch, details = compare_metadata(image, label)

        if not is_match:
            print(f"\nMismatch detected in: {os.path.basename(image_path)}")
            print("差异类型:", ", ".join(mismatch))

            # 重新采样标签
            fixed_label = resample_label(label, image)

            # 保存修复后的标签
            filename = os.path.basename(label_path)
            output_path = os.path.join(output_dir, filename)
            sitk.WriteImage(fixed_label, output_path)

            return {
                'status': 'fixed',
                'file': filename,
                'mismatch': mismatch,
                'details': details,
                'output_path': output_path
            }
        else:
            return {
                'status': 'ok',
                'file': os.path.basename(image_path),
                'details': details
            }

    except Exception as e:
        return {
            'status': 'error',
            'file': os.path.basename(image_path),
            'message': str(e)
        }


# def batch_process(image_dir, label_dir, output_dir):
#     """
#     批量处理目录中的图像和标签
#     """
#     # 创建输出目录
#     os.makedirs(output_dir, exist_ok=True)
#
#     # 获取图像文件列表
#     image_files = [f for f in os.listdir(image_dir) if f.endswith(('.nii', '.nii.gz', '.mha', '.nrrd'))]
#
#     results = []
#     for img_file in image_files:
#         # 构建路径
#         image_path = os.path.join(image_dir, img_file)
#         label_path = os.path.join(label_dir, img_file)  # 假设同名
#
#         if not os.path.exists(label_path):
#             results.append({
#                 'status': 'error',
#                 'file': img_file,
#                 'message': '对应的标签文件不存在'
#             })
#             continue
#
#         # 处理单个文件对
#         result = process_image_pair(image_path, label_path, output_dir)
#         results.append(result)
#
#     return results


def batch_process(image_dir, label_dir, output_dir):
    """
    批量处理目录中的图像和标签
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 获取图像文件列表
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.nii', '.nii.gz', '.mha', '.nrrd'))]

    results = []
    for img_file in image_files:
        # 构建标签文件名：移除图像文件名中的_0000后缀
        if "_0000" in img_file:
            # 分离文件名和扩展名
            base_name, ext = os.path.splitext(img_file)
            # 处理双扩展名（如.nii.gz）
            if ext == ".gz" and base_name.endswith(".nii"):
                base_name = os.path.splitext(base_name)[0]
                ext = ".nii.gz"
            # 去除最后的_0000部分
            label_base = base_name.rsplit("_0000", 1)[0]
            label_file = f"{label_base}{ext}"
        else:
            label_file = img_file  # 如果未找到_0000则保持原名

        # 构建路径
        image_path = os.path.join(image_dir, img_file)
        label_path = os.path.join(label_dir, label_file)  # 修正后的标签路径

        if not os.path.exists(label_path):
            results.append({
                'status': 'error',
                'file': img_file,
                'message': f'对应的标签文件不存在: {label_file}'
            })
            continue

        # 处理单个文件对
        result = process_image_pair(image_path, label_path, output_dir)
        results.append(result)

    return results

if __name__ == "__main__":
    # 配置路径
    IMAGE_DIR = "/home/lirongyaoper/Documents/1122image/"
    LABEL_DIR = "/home/lirongyaoper/Documents/1122label/"
    OUTPUT_DIR = "/home/lirongyaoper/Documents/1122/"

    # 执行批量处理
    results = batch_process(IMAGE_DIR, LABEL_DIR, OUTPUT_DIR)

    # 打印摘要报告
    total = len(results)
    ok_count = len([r for r in results if r['status'] == 'ok'])
    fixed_count = len([r for r in results if r['status'] == 'fixed'])
    error_count = len([r for r in results if r['status'] == 'error'])

    print("\n处理结果摘要:")
    print(f"总处理文件: {total}")
    print(f"元数据一致: {ok_count}")
    print(f"已修复文件: {fixed_count}")
    print(f"错误数量: {error_count}")